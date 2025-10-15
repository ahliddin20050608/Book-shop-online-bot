from aiogram.types import Message, CallbackQuery
from aiogram import Router, F
from aiogram.fsm.context import FSMContext 
from aiogram.filters import Command, CommandStart
from database import is_admin_by_id, all_books, save_book, get_orders, get_book_by_id, get_user_by_id, change_status
from buttons import main_button_admin,menu_kb, menu_admin_button, order_button, order_changed, order_finish
from buttons import menu_admin_button, ADMIN_MAIN_TEXT, MAIN_TEXT, ADMIN_MENU,back_button, ORDERS_TEXT, convert_books_to_html
from states import AddBookState
from aiogram.types import FSInputFile
import pdfkit

from database import get_all_admin, get_all_books, get_all_orders, get_all_users

admin_router = Router()

@admin_router.message(Command("admin"))
async def start_admin(message:Message):
    chat_id = message.from_user.id
    if is_admin_by_id(chat_id):
        await message.answer(ADMIN_MAIN_TEXT, reply_markup=main_button_admin)
    else:
        await message.answer("Siz admin emassiz😂")

@admin_router.message(F.text == "⬅️ Back")
async def admin_back_button(message:Message):
    chat_id = message.from_user.id
    if is_admin_by_id(chat_id):
        await message.answer(MAIN_TEXT,reply_markup=menu_kb)
    else:
        await message.answer("Siz admin emassiz😂")

@admin_router.message(F.text == "📃 Menu")
async def menu_admin(message:Message):
    chat_id = message.from_user.id
    if is_admin_by_id(chat_id):
        await message.answer(text=ADMIN_MENU, reply_markup=menu_admin_button)
    else:
        await message.answer("Siz admin emassiz😂")


@admin_router.message(F.text == "📦 All")
async def menu_admin(message:Message):
    chat_id = message.from_user.id
    if is_admin_by_id(chat_id):
        books = all_books()
        books_html = convert_books_to_html(books)
        path_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
        config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
        await message.answer(text="Kitoblar ro'yxati tayyorlanmoqda...")
        pdfkit.from_string(books_html, "books.pdf",options={"enable-local-file-access": ""}, configuration=config)
        file = FSInputFile("books.pdf")
        await message.answer_document(file)
    else:
        await message.answer("Siz admin emassiz😂")




@admin_router.message(F.text=="➕ Add")
async def add_handler(message:Message, state:FSMContext):
    chat_id = message.from_user.id
    if is_admin_by_id(chat_id):
        await message.answer("Iltimos, kitob nomini kiriting...")
        await state.set_state(AddBookState.title)
    else:
        await message.answer("Siz admin emassiz😂")



@admin_router.message(AddBookState.title)
async def get_title(message: Message, state: FSMContext):
    title = message.text
    await state.update_data(title=title)
    await message.answer("📖 Endi kitob haqida qisqacha ma'lumot kiriting ✍️")
    await state.set_state(AddBookState.description)




@admin_router.message(AddBookState.description)
async def get_description(message: Message, state: FSMContext):
    description = message.text
    await state.update_data(description=description)
    await message.answer("👤 Kitob muallifini kiriting:")
    await state.set_state(AddBookState.author)


@admin_router.message(AddBookState.author)
async def get_author(message: Message, state: FSMContext):
    author = message.text
    await state.update_data(author=author)
    await message.answer("🎭 Kitob janrini kiriting:")
    await state.set_state(AddBookState.genre)


@admin_router.message(AddBookState.genre)
async def get_genre(message: Message, state: FSMContext):
    genre = message.text
    await state.update_data(genre=genre)
    await message.answer("💰 Kitob narxini kiriting (so‘mda):")
    await state.set_state(AddBookState.price)


@admin_router.message(AddBookState.price)
async def get_price(message: Message, state: FSMContext):
    price = message.text
    await state.update_data(price=price)
    await message.answer("📦 Kitob sonini kiriting:")
    await state.set_state(AddBookState.quantity)


@admin_router.message(AddBookState.quantity)
async def get_quantity(message: Message, state: FSMContext):
    quantity = message.text
    await state.update_data(quantity=quantity)
    await message.answer("🖼 Kitob rasmini yuboring (jpg yoki png formatda):")
    await state.set_state(AddBookState.image)



@admin_router.message(AddBookState.image)
async def get_image(message: Message, state: FSMContext):
    data = await state.get_data()

    file = message.photo[-1]
    path = f"images/{file.file_unique_id}.jpg"
    await message.bot.download(file, destination=path)


    save_book(title=data["title"], description=data["description"],author=data["author"],genre=data["genre"],price=data["price"], quantity=data["quantity"], image_path=path)
    await message.answer("✅ Kitob muvaffaqiyatli qo‘shildi!", reply_markup=menu_admin_button)



@admin_router.message(F.text=="🗑️ Orders")
async def order_menu(message:Message):
    chat_id = message.from_user.id
    if is_admin_by_id(chat_id):
        await message.answer(text=ORDERS_TEXT, reply_markup=order_button)
    else:
        await message.answer("Siz admin emassiz😂")



@admin_router.message(F.text=="New")
async def get_new_orders(message:Message):
    orders = get_orders("new")
    for order in  orders:
        _,book_id,user_id,price,quantity,_,create_at = order
        book_name = get_book_by_id(int(book_id))[1]
        user_name = get_user_by_id(int(user_id))[2]
        text =f"Book Name: {book_name}\nUser_name: {user_name}\nPrice: {price}\nQuantity: {quantity}\nCreate_at: {create_at}\n"
        await message.answer(text, reply_markup=order_changed(id))

@admin_router.callback_query(F.data.startswith("in_progress"))
async def change_order_status(call:CallbackQuery):
    order_id = call.data.split("_")[-1]
    change_order_status("in progress",order_id)

    orders = get_orders("new")

    for order in orders:
        if order[0] == order_id:
            change_order_status("in_progress",order_id)
        
            await call.message.edit_reply_markup(reply_markup=None)



@admin_router.message(F.text=="In Progress")
async def get_in_progress_orders(message:Message):
    orders = get_orders("In Progress")
    for order in  orders:
        _,book_id,user_id,price,quantity,_,create_at = order
        book_name = get_book_by_id(int(book_id))[1]
        user_name = get_user_by_id(int(user_id))[2]
        text =f"Book Name: {book_name}\nUser_name: {user_name}\nPrice: {price}\nQuantity: {quantity}\nCreate_at: {create_at}\n"
        await message.answer(text, reply_markup=order_finish(id))


@admin_router.callback_query(F.data.startswith("finish_order"))
async def change_order_finish(call:CallbackQuery):
    order_id = call.data.split("_")[-1]
    change_order_status("in progress",order_id)

    orders = get_orders("in_progress")

    for order in orders:
        if order[0] == order_id:
            change_order_status("finished",order_id)
        
            await call.message.edit_reply_markup(reply_markup=None)


@admin_router.message(F.text=="Finish")
async def admin_order_finish(message:Message):
    orders = get_orders("finished")
    for order in  orders:
        _,book_id,user_id,price,quantity,_,create_at = order
        book_name = get_book_by_id(int(book_id))[1]
        user_name = get_user_by_id(int(user_id))[2]
        text =f"Book Name: {book_name}\nUser_name: {user_name}\nPrice: {price}\nQuantity: {quantity}\nCreate_at: {create_at}\n"
        await message.answer(text)



@admin_router.message(F.text=="Back")
async def admin_order_back(message:Message):
    await message.answer("Admin paneliga xush kelibsiz!", reply_markup=ADMIN_MAIN_TEXT)

 




@admin_router.message(F.text == "📊 Dashboard")
async def show_dashboard(message:Message):
    users = len(get_all_users())
    books = len(get_all_books())
    admins = len(get_all_admin)
    summa = 0
    for i in get_all_orders():
        summa += int(i[3])*int(i[4])
    text = f"Users: {users}\nBooks: {books}\nAdmins:{admins}\nTotal:{summa}"
    await message.answer(text, reply_markup=back_button)