from aiogram.types import Message
from aiogram import Router
from buttons import REG_TEXT
from buttons import register_kb
from aiogram.filters import Command, CommandStart


user_router = Router()
@user_router.message(CommandStart())
async def start(message:Message):
    await message.answer(text=REG_TEXT, reply_markup=register_kb)