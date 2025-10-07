from aiogram.types import Message, ReplyKeyboardRemove
from aiogram import Router, F
from buttons import REG_TEXT, NAME_TEXT, PHONE_TEXT
from buttons import register_kb, phone_kb
from aiogram.filters import Command, CommandStart
from states import Register, FSMContext
from filter import validate_fullname, validate_phone
user_router = Router()
@user_router.message(CommandStart())
async def start(message:Message):
    await message.answer(text=REG_TEXT, reply_markup=register_kb)


@user_router.message(F.text=="Ro'yxatdan o'tish")
async def start_register(message:Message, state:FSMContext):
    await state.set_state(Register.name)
    await message.answer(text=NAME_TEXT, reply_markup=ReplyKeyboardRemove())


@user_router.message(Register.name)
async def get_name(message:Message, state:FSMContext):
    if validate_fullname(message.text):
        await state.update_data(name = message.text)
        await state.set_state(Register.phone)
        await message.answer(PHONE_TEXT, reply_markup=phone_kb)
    else:
        await message.answer("Iltimos to'g'ri formatda kiriting: ")

@user_router.message(Register.phone)
async def get_phone(message:Message, state:FSMContext):
    phone = None
    if message.contact:
       phone = message.contact.phone_number
    else:
        if validate_phone:
            phone = message.text
        else:
            await message.answer("Iltimos to'g'ri formatda kiriting:")
    if phone:
        await state.update_data(phone=phone)
        await message.answer("Hali ham ishlayabdi.")