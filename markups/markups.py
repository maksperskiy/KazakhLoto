from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton

#Выбор y/n
btnConnect = KeyboardButton('Присоединиться')
ynMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnConnect)

#Админ
startGame = KeyboardButton('Начать игру')
onlineOfGame = KeyboardButton('Онлайн')
closeGame = KeyboardButton('Завершить игру')
AdminMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(startGame, onlineOfGame, closeGame)
