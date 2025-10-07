from aiogram.types import(
    KeyboardButton, ReplyKeyboardMarkup,
    ReplyKeyboardRemove, InlineKeyboardButton,
    InlineKeyboardMarkup)


register_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Ro'yxatdan o'tish")]
    ], 
    resize_keyboard=True
)
phone_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📞 Kontakt ulashish", request_contact=True)]
    ], 
    resize_keyboard=True
)