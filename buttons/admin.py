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
menu_admin_button = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="➕ Add")],
        [KeyboardButton(text="📦 All")],
        [KeyboardButton(text="⬅️ Back")]
    ],
    resize_keyboard=True
)
order_button = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="New")],
        [KeyboardButton(text="In Progress")],
        [KeyboardButton(text="Finish")],
        [KeyboardButton(text="Back")]

    ],
    resize_keyboard=True
)


def order_changed(order_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Cancel", callback_data=f"cancel_order_{order_id}"),
                InlineKeyboardButton(text="In progress", callback_data=f"in_progress_{order_id}")
            ]
        ]
    )


def order_finish(order_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Finish", callback_data=f"finish_order_{order_id}")
            ]
        ]
    )
back_button = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Back")]
    ],
    resize_keyboard=True
)