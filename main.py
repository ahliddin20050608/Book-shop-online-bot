from aiogram import Bot, Dispatcher,F
from aiogram.types import Message
from database import env
from handler import user_router, admin_router, register_router
import logging
import asyncio

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

