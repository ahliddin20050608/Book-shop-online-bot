from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from buttons import menu_option_kb, search_inline_kb
from buttons import MENU_TEXT, SEARCH_TEXT
from aiogram.types import FSInputFile
from database import find_books
from states import SearchBook 
user_router = Router()


@user_router.message(F.text=="📚 Menu")
async def user_menu_handler(message:Message):
    photo = "images/menu.webp"

    await message.answer_photo(photo=FSInputFile(path=photo), caption=MENU_TEXT, reply_markup=menu_option_kb)

@user_router.message(F.text=="🔍 Search")
async def search_choice(message:Message):
    await  message.answer(text=SEARCH_TEXT, reply_markup=search_inline_kb)
@user_router.callback_query(F.data.startswith("search"))
async def search_query(call:CallbackQuery, state:FSMContext):
    await state.set_state(SearchBook.search_name)
    data = call.data.split("_")[-1]
    await state.update_data(name = data)
    await state.set_state(SearchBook.text)
    if data !="back":
        await call.message.answer(f"{data.title()} kiriting:")
    else:
        await state.clear()
        await call.message.edit_reply_markup(None)
        photo = "images/menu.webp"
        await call.message.answer_photo(photo=FSInputFile(path=photo), caption=MENU_TEXT, reply_markup=menu_option_kb)

@user_router.message(SearchBook.text)
async def get_search_books(message:Message,state:FSMContext):
    search_name = await state.get_data()
    search_name = search_name.get("name")
    data = find_books(search_name, message.text)
    if data :
        pass
    else:
        await message.answer(f"{message.text} - bunday {search_name} bizda mavjud emas.")