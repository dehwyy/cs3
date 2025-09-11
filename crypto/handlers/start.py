from aiogram import types, Router
from aiogram.filters import Command
from db import get_user, add_user
from keyboards import get_start_keyboard, get_main_inline
from locales import MESSAGES

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    lang = "ru"
    name = message.from_user.first_name

    row = await get_user(message.chat.id)
    if not row:
        await add_user(message.chat.id, lang)
    else:
        lang = row["language"]

    await message.answer(
        MESSAGES[lang]["start"].format(name=name),
    )
    await message.answer(MESSAGES[lang]["menu"], reply_markup=get_main_inline(lang))
