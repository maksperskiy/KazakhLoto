import markups.markups as nav
from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp, bot
from services.service import *
from states.storage import StartGame


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
                    await StartGame.startGame.set()
                except:
                    print("Неккоректные символы")
                    await message.answer("Неккоректные символы")
            else:
                await message.reply("Вы уже авторизированны!")
        except:
            return


@dp.message_handler(state=StartGame.startGame)
async def add_twitchname(message: types.Message, state: FSMContext):
    print(f"Имя {message.text}")
    addTwitchName(message.chat.id, message.text)
    if isGameStarted():
        await message.answer("Вы установили ник", reply_markup=nav.connectMenu)
    else:
        await message.answer("Вы установили ник")
    await state.finish()
