from aiogram.types import Message, ReplyKeyboardRemove
from aiogram import Router, F
from buttons import REG_TEXT, NAME_TEXT, PHONE_TEXT, SUCCESS_REG_TEXT,MAIN_TEXT
from buttons import register_kb, phone_kb,menu_kb
from aiogram.filters import Command, CommandStart
from database import is_register_by_chat_id
from states import Register, FSMContext
from filter import validate_fullname, validate_phone
from aiogram.types import FSInputFile



register_router = Router()
@register_router.message(CommandStart())
async def start(message:Message):
    registrated = is_register_by_chat_id(message.from_user.id)
    photo_path = "images/image.png"

    if registrated:
        await message.answer_photo(photo=FSInputFile(path=photo_path), caption=MAIN_TEXT, reply_markup= menu_kb)
        await message.answer(text=MAIN_TEXT, reply_markup=register_kb)
    else:
        await message.answer_photo(photo=FSInputFile(path=photo_path), caption=REG_TEXT, reply_markup= register_kb)

@register_router.message(F.text=="Ro'yxatdan o'tish")
async def start_register(message:Message, state:FSMContext):
    await state.set_state(Register.name)
    await message.answer(text=NAME_TEXT, reply_markup=ReplyKeyboardRemove())


@register_router.message(Register.name)
async def get_name(message:Message, state:FSMContext):
    if validate_fullname(message.text):
        await state.update_data(name = message.text)
        await state.set_state(Register.phone)
        await message.answer(PHONE_TEXT, reply_markup=phone_kb)
    else:
        await message.answer("Iltimos to'g'ri formatda kiriting: ")

@register_router.message(Register.phone)
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
        await message.answer(text=SUCCESS_REG_TEXT, reply_markup=menu_kb)