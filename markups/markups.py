from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton

#Выбор y/n
btnYes = KeyboardButton('Присоединиться')
btnNo = KeyboardButton('Нет')
ynMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnYes)

#Админ
startGame = KeyboardButton('Начать игру')
closeGame = KeyboardButton('Завершить игру')
AdminMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(startGame, closeGame)





