from aiogram.dispatcher.filters.state import StatesGroup, State
class StartGame(StatesGroup):
    StartGameOne = State()
    StartGameTwo = State()
    StartGameThree = State()
    StartGameFour = State()

class Cards(StatesGroup):
    CardOne = State()
    CardTwo = State()

