from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


class SearchBook(StatesGroup):
    search_name = State()
    text = State()