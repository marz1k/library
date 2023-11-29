from aiogram.dispatcher.filters.state import StatesGroup, State


class FindBook(StatesGroup):
    phrase = State()


class AddBook(StatesGroup):
    name = State()
    author = State()
    genre = State()
    description = State()
    confirm = State()