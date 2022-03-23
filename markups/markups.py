from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

connect = KeyboardButton('Присоединиться')
connectMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(connect)

startGame = KeyboardButton('Начать игру')
onlineOfGame = KeyboardButton('Онлайн')
closeGame = KeyboardButton('Завершить игру')
adminMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(
    startGame, onlineOfGame, closeGame)
