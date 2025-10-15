from aiogram.fsm.state import StatesGroup, State

class AddBookState(StatesGroup):
    title = State()
    description = State() 
    author = State() 
    genre = State() 
    price = State() 
    quantity = State() 
    image = State()