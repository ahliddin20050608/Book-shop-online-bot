from aiogram import Bot, Dispatcher
from aiogram.types import Message
from handler import user_router, admin_router, register_router
import logging
import asyncio
from environs import Env

env = Env()
env.read_env()

TOKEN = env.str("TOKEN")
dp = Dispatcher()

async def main():
    bot = Bot(token=TOKEN)
    dp.include_router(user_router)
    dp.include_router(admin_router)
    dp.include_router(register_router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    asyncio.run(main())
 
