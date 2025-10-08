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
menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📚 Menu")],
        [KeyboardButton(text="🛒 Orders")],
        [KeyboardButton(text="📞 Contact")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
) 
menu_option_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔍 Search"), KeyboardButton(text="📚 All")],
        [KeyboardButton(text="💸 Discount"), KeyboardButton(text="🆕 New")],
        [KeyboardButton(text="↩️ Back")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

search_inline_kb = InlineKeyboardMarkup(
    inline_keyboard=[
    [   InlineKeyboardButton(text="Title", callback_data="search_title"),
        InlineKeyboardButton(text="Genre", callback_data="search_genre"),
    ],
    [
        InlineKeyboardButton(text="Author", callback_data="search_author"),
        InlineKeyboardButton(text="Back", callback_data="search_back")

    ]
    
]
)