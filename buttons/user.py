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


PEG_NEXT = 10

def get_pagination_button(data, page: int, search_name: str, text: str):

    total_page = (len(data) - 1) // PEG_NEXT + 1

    # Har bir sahifa uchun ko‘rsatiladigan kitoblar
    start = (page - 1) * PEG_NEXT
    end = start + PEG_NEXT
    books_page = data[start:end]

    # Tugmalarni 2 qatorga bo‘lish
    first_inline = []
    last_inline = []

    for idx, book in enumerate(books_page, start=start + 1):
        if idx < (page - 1) * PEG_NEXT+6:
            first_inline.append(InlineKeyboardButton(
            text=f"{idx}",
            callback_data=f"book_id_{book[0]}"
        ))
        else:
            last_inline.append(InlineKeyboardButton(
            text=f"{idx}",
            callback_data=f"book_id_{book[0]}"
        ))

    inline_b = []
    if first_inline:
        inline_b.append(first_inline)
    if last_inline:
        inline_b.append(last_inline)

    # Navigatsiya tugmalari (oldingi/keyingi sahifalar)
    nav_buttons = []
    if page > 1:
        nav_buttons.append(
            InlineKeyboardButton(
                text="⏪ Oldingi",
                callback_data=f"back_{search_name}_{text}_{page-1}"
            )
        )

    nav_buttons.append(
        InlineKeyboardButton(
            text=f"📄 {page}/{total_page}",
            callback_data="none"
        )
    )

    if page < total_page:
        nav_buttons.append(
            InlineKeyboardButton(
                text="Keyingi ⏩",
                callback_data=f"next_{search_name}_{text}_{page+1}"
            )
        )

    inline_b.append(nav_buttons)
    inline_b.append([
        InlineKeyboardButton(text="↩️ Bekor qilish", callback_data="cancel_books"),
        InlineKeyboardButton(text="✈️ Yuborish", callback_data="send_books")
    ])

    return InlineKeyboardMarkup(inline_keyboard=inline_b)




def plus_minus_inline_button(book_id,count):
    buttons = InlineKeyboardMarkup(

        inline_keyboard=[
          [
           InlineKeyboardButton(text="➖", callback_data=f"minus_{count}"),
           InlineKeyboardButton(text=f"{count}", callback_data=f"values"),
           InlineKeyboardButton(text="➕", callback_data=f"plus_{count}")
          ],
          [
              InlineKeyboardButton(text ="Cancel",callback_data=f"cancel_{book_id}"),
              InlineKeyboardButton(text ="Save",callback_data=f"save_{count}_{book_id}")

          ]  
        ]
    )
    return buttons