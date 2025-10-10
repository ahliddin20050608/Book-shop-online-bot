from aiogram.types import (
    ReplyKeyboardMarkup, InlineKeyboardMarkup,
    ReplyKeyboardRemove, InlineKeyboardButton,
    KeyboardButton,
)


main_button_admin = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📃 Menu")],
        [KeyboardButton(text="🗑️ Orders")],

        [KeyboardButton(text="📊 Dashboard")]
    ],
    resize_keyboard=True
)

