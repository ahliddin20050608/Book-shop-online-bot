from aiogram.types import Message
from aiogram import Router
from buttons import REG_TEXT
from aiogram.filters import Command, CommandStart
from database import is_admin_by_id
from buttons import main_button_admin
admin_router = Router()

@admin_router.message(Command("admin"))
async def start_admin(message:Message):
    chat_id = message.from_user.id
    if is_admin_by_id(chat_id):
        await message.answer("Admin paneliga xush kelibsiz!😍", reply_markup=main_button_admin)
    else:
        await message.answer("Siz admin emassiz😂")