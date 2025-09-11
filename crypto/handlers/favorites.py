from aiogram import types, F, Router
from db import get_user, update_language, get_favorites, add_favorite, remove_favorite
from services.crypto_api import get_coin_data, get_multiple
from keyboards import get_main_inline, get_lang_keyboard, get_edit_favorites_keyboard
from locales import MESSAGES
from config import CRYPTOCURRENCIES

router = Router()

def format_coin(symbol, coin, lang):
    if not coin:
        return f"<b>{symbol}</b>: error"
    trend = "📈" if coin["change_24h"] and coin["change_24h"] > 0 else "📉"
    if lang == "ru":
        return (
            f"<b>{symbol}</b>\n"
            f"💵 Цена: <b>{coin['price']}</b> USD\n"
            f"📊 Изм. за 24ч: <b>{coin['change_24h']:.2f}%</b> {trend}\n"
            f"📉 Мин/Макс 24ч: {coin['low_24h']} / {coin['high_24h']} USD"
        )
    else:
        return (
            f"<b>{symbol}</b>\n"
            f"💵 Price: <b>{coin['price']}</b> USD\n"
            f"📊 24h Change: <b>{coin['change_24h']:.2f}%</b> {trend}\n"
            f"📉 Low/High 24h: {coin['low_24h']} / {coin['high_24h']} USD"
        )

@router.callback_query(F.data == "popular")
async def popular(callback: types.CallbackQuery):
    user = await get_user(callback.message.chat.id)
    lang = user["language"] if user else "ru"
    coins = get_multiple(list(CRYPTOCURRENCIES.keys()))
    msg = [MESSAGES[lang]["popular"]]
    for c in coins:
        symbol = next((k for k, v in CRYPTOCURRENCIES.items() if v == c["id"]), c["id"])
        coin = {
            "price": c["current_price"],
            "change_24h": c["price_change_percentage_24h"],
            "high_24h": c["high_24h"],
            "low_24h": c["low_24h"],
        }
        msg.append(format_coin(symbol, coin, lang))
    await callback.message.edit_text("\n\n".join(msg), reply_markup=get_main_inline(lang))

@router.callback_query(F.data == "favorites")
async def favorites(callback: types.CallbackQuery):
    user = await get_user(callback.message.chat.id)
    lang = user["language"] if user else "ru"
    favs = await get_favorites(callback.message.chat.id)
    if not favs:
        await callback.message.edit_text(MESSAGES[lang]["favorites_empty"], reply_markup=get_main_inline(lang))
    else:
        msg = []
        for f in favs:
            coin = get_coin_data(f)
            msg.append(format_coin(f, coin, lang))
        await callback.message.edit_text("\n\n".join(msg), reply_markup=get_main_inline(lang))

@router.callback_query(F.data == "change_lang")
async def change_lang(callback: types.CallbackQuery):
    await callback.message.edit_text("Выберите язык:", reply_markup=get_lang_keyboard())

@router.callback_query(F.data.startswith("set_lang_"))
async def set_lang(callback: types.CallbackQuery):
    lang_code = callback.data.split("_")[-1]
    lang = "ru" if lang_code == "ru" else "en"
    await update_language(callback.message.chat.id, lang)
    await callback.message.edit_text(MESSAGES[lang]["lang_changed"], reply_markup=get_main_inline(lang))

@router.callback_query(F.data == "edit_favorites")
async def edit_favorites(callback: types.CallbackQuery):
    user = await get_user(callback.message.chat.id)
    lang = user["language"] if user else "ru"
    await callback.message.edit_text("Редактировать избранное:", reply_markup=get_edit_favorites_keyboard(lang))

@router.callback_query(F.data == "add_fav")
async def add_fav(callback: types.CallbackQuery):
    user = await get_user(callback.message.chat.id)
    lang = user["language"] if user else "ru"
    await callback.message.edit_text(MESSAGES[lang]["enter_symbol"])

@router.message()
async def handle_message(message: types.Message):
    user = await get_user(message.chat.id)
    lang = user["language"] if user else "ru"
    text = message.text.strip().upper()

    # Проверка на добавление или удаление
    if text.startswith("+"):  # Добавление
        symbol = text[1:]
        coin = get_coin_data(symbol)
        if not coin:
            await message.answer(MESSAGES[lang]["not_found"])
            return
        await add_favorite(message.chat.id, symbol)
        favs = await get_favorites(message.chat.id)
        await message.answer(MESSAGES[lang]["added"].format(symbol=symbol, favorites=", ".join(favs)), reply_markup=get_main_inline(lang))

    elif text.startswith("-"):  # Удаление
        symbol = text[1:]
        await remove_favorite(message.chat.id, symbol)
        favs = await get_favorites(message.chat.id)
        await message.answer(MESSAGES[lang]["removed"].format(symbol=symbol, favorites=", ".join(favs)), reply_markup=get_main_inline(lang))

    else:  # Поиск валюты
        coin = get_coin_data(text)
        if not coin:
            await message.answer(MESSAGES[lang]["not_found"])
            return
        await message.answer(format_coin(text, coin, lang), reply_markup=get_main_inline(lang))
