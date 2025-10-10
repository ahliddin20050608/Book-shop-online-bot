from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from buttons import menu_option_kb, search_inline_kb, menu_kb, plus_minus_inline_button, register_kb
from buttons import MENU_TEXT, SEARCH_TEXT, MAIN_TEXT, REG_TEXT
from aiogram.types import FSInputFile
from database import find_books, find_by_books_id, order_save_books, is_register_by_chat_id
from states import SearchBook 
from filter import get_all_books
import os
user_router = Router()


photo_path = "images/image.png"

CHECKED_BOOKS = []
@user_router.message(F.text=="📚 Menu")
async def user_menu_handler(message:Message):
    if is_register_by_chat_id(message.from_user.id):
        photo = "images/menu.webp"

        await message.answer_photo(photo=FSInputFile(path=photo), caption=MENU_TEXT, reply_markup=menu_option_kb)
    else:
        photo_path = "images/image.png"
        await message.answer_photo(photo=FSInputFile(path=photo_path), caption=REG_TEXT, reply_markup= register_kb)

@user_router.message(F.text=="🔍 Search")
async def search_choice(message:Message):
    if is_register_by_chat_id(message.from_user.id):
        await  message.answer(text=SEARCH_TEXT, reply_markup=search_inline_kb)
    else:
        await message.answer_photo(photo=FSInputFile(path=photo_path), caption=REG_TEXT, reply_markup= register_kb)

@user_router.message(F.text=="↩️ Back")
async def back_menu(message:Message):
    if is_register_by_chat_id(message.from_user.id):
        photo = "images/menu.webp"

        await message.answer_photo(photo=FSInputFile(path=photo), caption=MAIN_TEXT, reply_markup=menu_kb)
    else:
        await message.answer_photo(photo=FSInputFile(path=photo_path), caption=REG_TEXT, reply_markup= register_kb)


    await message.answer(" ",reply_markup=search_inline_kb)

@user_router.callback_query(F.data.startswith("search"))
async def search_query(call:CallbackQuery, state:FSMContext):
    await state.set_state(SearchBook.search_name)
    data = call.data.split("_")[-1]
    await state.update_data(name = data)
    await state.set_state(SearchBook.text)
    if data !="back":
        await call.message.edit_reply_markup(None)
        await call.message.answer(f"{data.title()} kiriting:")

    else:
        await state.clear()
        await call.message.edit_reply_markup(None)
        photo = "images/menu.webp"
        await call.message.answer_photo(photo=FSInputFile(path=photo), caption=MENU_TEXT, reply_markup=menu_option_kb)

@user_router.message(SearchBook.text)
async def get_search_books(message:Message,state:FSMContext):
    if is_register_by_chat_id(message.from_user.id):    
        search_name = await state.get_data()
        search_name = search_name.get("name")
        data = get_all_books(search_name = search_name, text = message.text)
        if data :
            await message.answer(text=data[0], reply_markup=data[1])
        else:
            await message.answer(f"{message.text} - bunday {search_name} bizda mavjud emas.")
    else:
        await message.answer_photo(photo=FSInputFile(path=photo_path), caption=REG_TEXT, reply_markup= register_kb)

@user_router.callback_query(F.data.startswith("cancel_books"))
async def back_search(call:CallbackQuery):
    await call.message.edit_text(SEARCH_TEXT)

@user_router.callback_query(F.data.startswith("next"))
async def next_page_book(call:CallbackQuery):
    search_name = call.data.split("_")[1]
    text = call.data.split("_")[2]
    page = int(call.data.split("_")[-1])


    data = get_all_books(search_name = search_name, text = text, page=page)
    await call.message.edit_text(text=data[0])
    await call.message.edit_reply_markup(reply_markup=data[1])



@user_router.callback_query(F.data.startswith("back"))
async def next_page_book(call:CallbackQuery):
    search_name = call.data.split("_")[1]
    text = call.data.split("_")[2]
    page = int(call.data.split("_")[-1])


    data = get_all_books(search_name = search_name, text = text, page=page)
    await call.message.edit_text(text=data[0])
    await call.message.edit_reply_markup(reply_markup=data[1])



@user_router.callback_query(F.data.startswith("book_id"))
async def get_checked_books(call:CallbackQuery):
    book_id = int(call.data.split("_")[-1])
    CHECKED_BOOKS.append(book_id)


@user_router.callback_query(F.data.startswith("send_books"))
async def get_checked_books(call: CallbackQuery):
    if not CHECKED_BOOKS:
        await call.message.answer("📚 Hech qanday kitob tanlanmagan.")
        return

    for book_id in CHECKED_BOOKS:
        book = find_by_books_id(book_id)

        book_file = book[-1] if book[-1] else "not_found_image.webp"
        book_path = os.path.join("images", book_file)

        if not os.path.exists(book_path):
            book_path = "images/not_found_image.webp"

        await call.message.answer_photo(
            photo=FSInputFile(book_path),
            caption=f"{book[1]}\n\n{book[2]}",
            reply_markup=plus_minus_inline_button(book[0], count=1)
        )


@user_router.callback_query(F.data.startswith("minus"))
async def minus_button(call: CallbackQuery):
    data = call.data.split("_")
    count = int(data[1])
    markup = call.message.reply_markup.inline_keyboard
    book_id = None
    for row in markup:
        for btn in row:
            if btn.callback_data.startswith("save_"):
                parts = btn.callback_data.split("_")
                if len(parts) == 3:
                    book_id = int(parts[2])
                break
        if book_id:
            break
    if not book_id:
        await call.answer("Book ID topilmadi!", show_alert=True)
        return
    if count <= 1:
        await call.answer("Kamaytirish mumkin emas!", show_alert=True)
        return
    count -= 1
    await call.message.edit_reply_markup(
        reply_markup=plus_minus_inline_button(book_id, count)
    )

@user_router.callback_query(F.data.startswith("plus"))
async def plus_button(call: CallbackQuery):
    data = call.data.split("_")
    count = int(data[1])  
    markup = call.message.reply_markup.inline_keyboard
    book_id = None
    for row in markup:
        for btn in row:
            if btn.callback_data.startswith("save_"):
                parts = btn.callback_data.split("_")
                if len(parts) == 3:
                    book_id = int(parts[2])
                break
        if book_id:
            break
    if not book_id:
        await call.answer("Book ID topilmadi!", show_alert=True)
        return
    if count >= 10:
        await call.answer("10 tadan ortiq yuborish mumkin emas!", show_alert=True)
        return
    count += 1
    await call.message.edit_reply_markup(
        reply_markup=plus_minus_inline_button(book_id, count)
    )
@user_router.callback_query(F.data.startswith("save_"))
async def save_book_by_id(call: CallbackQuery):
    data = call.data.split("_")
    count = int(data[1])         
    book_id = int(data[2])         

    for i in CHECKED_BOOKS:
        book = find_by_books_id(i)
        if int(book[0]) == book_id:
            book_price = int(book[5])   
            chat_id = call.from_user.id
            order_save_books(book_id, chat_id, count, book_price)
            await call.message.edit_reply_markup(reply_markup=None)
            await call.message.answer(f"{book[1]} savatchaga {count} dona sifatida qo‘shildi!")
            break

