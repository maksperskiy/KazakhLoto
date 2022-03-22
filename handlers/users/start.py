from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
import markups.markups as nav
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.utils.callback_data import CallbackData
from loader import dp, bot
from services.service import *
from datetime import datetime
from states.storage import StartGame, Cards
import json

@dp.message_handler(commands=['start'], state=None)
async def start(message: types.Message):
    chat = await bot.get_chat(message.chat.id)
    if chat.type == "group":
        return
    else:
        await message.answer("Здарова,заебал!")
        user = message.from_user
        try:
            if not userExists(message.chat.id):
                addUser(message.chat.id)
        except:
            print("Что то с добавлен в бд")
            await message.answer("<b>НЕУДАЧА </b>Проверте свой никнейм телеграм")
        try:
            if getTwitchName(user.id) is None:
                await message.answer("Введите свой никнейм Твич!")
                try:
                    await StartGame.StartGameOne.set()
                except:
                    print("Неккоректные символы")
                    await message.answer("Неккоректные символы")
            else:
                await message.reply("Вы уже авторизированны!")
        except:
            return

@dp.message_handler(state=StartGame.StartGameOne)
async def AddTwitch(message: types.Message, state: FSMContext):
    print(f"Имя {message.text}")
    addTwitchName(message.chat.id, message.text)
    await message.answer("Вы установили ник")
    await state.finish()


# ------------------------------------------------------------------------
# @dp.message_handler(commands=['addCard'], state=None)
# async def massiveCardAdd(message: types.Message):
#     if (isAdmin(message.chat.id)):
#         await message.answer("Введите № карточки")
#         await Cards.CardOne.set()
#     else:
#         await message.answer("У вас нет прав")

# @dp.message_handler(state=Cards.CardOne)
# async def AddCard(message: types.Message, state: FSMContext):
#     text = message.text
#     await state.update_data(text=text)
#     if (CheckCard(text) != 0):
#         await message.answer("Такая карта уже существует")
#         await state.finish()
#     else:
#         await message.answer("Введите числа через запятую")
#         await Cards.CardTwo.set()

# @dp.message_handler(state=Cards.CardTwo)
# async def AddCard(message: types.Message, state: FSMContext):
#     data = await state.get_data()
#     id_card = int(data.get("text"))
#     num_card = message.text
#     InsertMass(id_card, num_card)
#     await message.answer("Карточка сохранена")
#     await state.finish()







