import json
import markups.markups as nav
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from services.service import *
from aiogram.utils.callback_data import CallbackData
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from loader import dp, bot

onl = CallbackData("post", "users", "action")


@dp.message_handler(commands=['admin'])
async def admin(message: types.Message):
    user = message.from_user
    if isAdmin(user.id):
        await message.answer("Вы админ", reply_markup=nav.AdminMenu)
    else:
        await message.answer("У вас нет прав")


@dp.message_handler(Text(equals="Онлайн"), state=None)
async def admin(message: types.Message):
    if isAdmin(message.chat.id):
        if isGameStarted():
            await message.answer(f"Онлайн: {usersCount()}")
        else:
            await message.answer(f"Игра не начата")
    else:
        await message.answer("У вас нет прав")

@dp.message_handler(Text(equals="Начать игру"), state=None)
async def answer_b1(message: types.Message, state: FSMContext):
    if isAdmin(message.chat.id):
        if isGameStarted():
            await message.answer("Игра уже начата")
            return
        
        keyboard = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton(
            text=f"{usersCount()}/{getMaxUsersValue()}",
            callback_data=onl.new(users={usersCount()}, action="del")
        )
        keyboard.add(button)

        startSession()
        for chat_id in getUserMailing():
           await bot.send_message(chat_id, "Ку игра началась!\nНе желаешь присоединиться?", reply_markup=nav.ynMenu)
        await message.answer("<b>ADMIN</b> По мере необходимости вводи выпавшее число", reply_markup=keyboard)
    else:
        await message.answer("У вас нет прав")

@dp.callback_query_handler(onl.filter(action="del"))
async def onlineCheck(call: types.CallbackQuery, callback_data: dict):
    await call.message.answer(f"Онлайн: {usersCount()}")
    await call.answer()




@dp.message_handler(Text(equals="Завершить игру"), state=None)
async def answer_b1(message: types.Message, state: FSMContext):
    if isAdmin(message.chat.id):
        if isGameStarted():
            try:
                for chat_id in getUserMailingInSession():
                    await bot.send_message(chat_id, "<b>Игра завершена!</b>\n"
                                                       "по тех вопросам к @mironchikk")
                stopSession()
                await bot.send_message(message.chat.id, "Вы завершили игру")
            except:
                await message.answer("Нет участников")
        else:
            await message.answer("Игра уже закончена!")
    else:
        await message.answer("У вас нет прав")

# @dp.message_handler(Text(equals="saddsasadadssadadsmass"), state=None)
# async def massiveCardAdd(message: types.Message):
#     count = 0
#     card = SelectMass(2)
#     for card_user in card:
#         if card_user in SelAdminCard():
#             count += 1
#     if (len(card) != count):
#         await message.answer("Ты лох")
#     else:
#         await message.answer("Мегахарош")



@dp.message_handler(Text(equals="Read lotteries file"), state=None)
async def ppp(message: types.Message):
    if isAdmin(message.chat.id):
        file = open("generator/lotteries.txt", "r")
        for line_number, loto in enumerate(file.readlines()):
            addCard(line_number+1, json.loads(loto))

        file.close()
    


@dp.message_handler()
async def answer_b1(message: types.Message, state: FSMContext):
    if (isAdmin(message.chat.id)):
        if isGameStarted():
            try:
                mess = int(message.text)
                addNum(mess)
                await message.answer("Число зарегистрированно")

            except:
                await message.answer("Вы ввели не число")



