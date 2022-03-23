from aiogram.dispatcher.filters.state import StatesGroup, State


class StartGame(StatesGroup):
    startGame = State()
