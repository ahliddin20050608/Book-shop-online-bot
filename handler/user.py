from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from buttons import menu_option_kb, search_inline_kb, menu_kb, plus_minus_inline_button
from buttons import MENU_TEXT, SEARCH_TEXT, MAIN_TEXT
from aiogram.types import FSInputFile
from database import find_books, find_by_books_id
from states import SearchBook 
from filter import get_all_books
import os
user_router = Router()

CHECKED_BOOKS = []
@user_router.message(F.text=="📚 Menu")
async def user_menu_handler(message:Message):
    photo = "images/menu.webp"

    await message.answer_photo(photo=FSInputFile(path=photo), caption=MENU_TEXT, reply_markup=menu_option_kb)

@user_router.message(F.text=="🔍 Search")
async def search_choice(message:Message):
    await  message.answer(text=SEARCH_TEXT, reply_markup=search_inline_kb)

@user_router.message(F.text=="↩️ Back")
async def back_menu(message:Message):
    photo = "images/menu.webp"

    await message.answer_photo(photo=FSInputFile(path=photo), caption=MAIN_TEXT, reply_markup=menu_kb)


    await message.answer(reply_markup=search_inline_kb)

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
    search_name = await state.get_data()
    search_name = search_name.get("name")
    data = get_all_books(search_name = search_name, text = message.text)
    if data :
        await message.answer(text=data[0], reply_markup=data[1])
    else:
        await message.answer(f"{message.text} - bunday {search_name} bizda mavjud emas.")

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

    for i in CHECKED_BOOKS:
        book = find_by_books_id(i)
        if not book:
            continue  # Agar topilmasa keyingisiga o'tadi

        # Fayl yo‘li
        file_name = book[-1] if len(book) > 4 and book[-1] else None
        book_path = os.path.join("images", file_name) if file_name else "images/not_found_image.webp"

        # Agar rasm mavjud bo‘lmasa, defaultni ishlatamiz
        if not os.path.exists(book_path):
            book_path = "images/not_found_image.webp"

        # Rasmni yuborish
        await call.message.answer_photo(
            photo=FSInputFile(path=book_path),
            caption=f"📖 {book[1]}\n\n📝 {book[2]}",
            reply_markup=plus_minus_inline_button(book[0], count=1)
        )


# ➖ Minus tugmasi
@user_router.callback_query(F.data.startswith("minus_"))
async def minus_button(call: CallbackQuery):
    data_parts = call.data.split("_")
    if len(data_parts) < 3:
        return  # noto‘g‘ri formatdagi callback

    count = int(data_parts[1])
    book_id = int(data_parts[-1])

    for i in CHECKED_BOOKS:
        book = find_by_books_id(i)
        if not book:
            continue
        if int(book[0]) == book_id:
            if count <= 1:
                await call.answer("❗️Kamaytirish mumkin emas.", show_alert=True)
                return
            count -= 1
            await call.message.edit_reply_markup(
                reply_markup=plus_minus_inline_button(book[0], count)
            )
            break


# ➕ Plus tugmasi
@user_router.callback_query(F.data.startswith("plus_"))
async def plus_button(call: CallbackQuery):
    data_parts = call.data.split("_")
    if len(data_parts) < 3:
        return  # noto‘g‘ri formatdagi callback

    count = int(data_parts[1])
    book_id = int(data_parts[-1])

    for i in CHECKED_BOOKS:
        book = find_by_books_id(i)
        if not book:
            continue
        if int(book[0]) == book_id:
            if count >= 10:
                await call.answer("❗️10 tadan ortiq yuborish mumkin emas.", show_alert=True)
                return
            count += 1
            await call.message.edit_reply_markup(
                reply_markup=plus_minus_inline_button(book[0], count)
            )
            break