from aiogram import Bot, Dispatcher,F
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from database import env

import logging
import asyncio

TOKEN = env.str("TOKEN")
dp = Dispatcher()

async def main():
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    asyncio.run(main=())

