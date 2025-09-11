from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# def get_start_keyboard(lang="ru"):
#     text = "СТАРТ" if lang == "ru" else "START"
#     return ReplyKeyboardMarkup(
#         keyboard=[[KeyboardButton(text=text)]],
#         resize_keyboard=True
#     )

def get_main_inline(lang="ru"):
    if lang == "ru":
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📊 Популярные", callback_data="popular")],
            [InlineKeyboardButton(text="⭐ Избранное", callback_data="favorites")],
            [InlineKeyboardButton(text="✏ Редактировать избранное", callback_data="edit_favorites")],
            [InlineKeyboardButton(text="🔎 Найти", callback_data="find")],
            [InlineKeyboardButton(text="🔄 Поменять язык", callback_data="change_lang")],
        ])
    else:
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📊 Popular", callback_data="popular")],
            [InlineKeyboardButton(text="⭐ Favorites", callback_data="favorites")],
            [InlineKeyboardButton(text="✏ Edit favorites", callback_data="edit_favorites")],
            [InlineKeyboardButton(text="🔎 Search", callback_data="find")],
            [InlineKeyboardButton(text="🔄 Change language", callback_data="change_lang")],
        ])

def get_lang_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Русский 🇷🇺", callback_data="set_lang_ru")],
        [InlineKeyboardButton(text="English 🇬🇧", callback_data="set_lang_en")],
    ])

def get_edit_favorites_keyboard(lang="ru"):
    if lang == "ru":
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="➕ Добавить", callback_data="add_fav")],
            [InlineKeyboardButton(text="➖ Удалить", callback_data="remove_fav")],
            [InlineKeyboardButton(text="⬅ Назад", callback_data="back")],
        ])
    else:
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="➕ Add", callback_data="add_fav")],
            [InlineKeyboardButton(text="➖ Remove", callback_data="remove_fav")],
            [InlineKeyboardButton(text="⬅ Back", callback_data="back")],
        ])
