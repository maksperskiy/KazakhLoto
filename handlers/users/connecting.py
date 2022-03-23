from aiogram.types import ReplyKeyboardRemove
from aiogram import types
from aiogram.dispatcher.filters import Text
from loader import dp, bot

from aiogram.utils.callback_data import CallbackData
from services.service import *

cardClose = CallbackData("post", "card_id", "chat_id", "action")
skipCard = CallbackData("post", "action")


@dp.message_handler(Text(contains="рисоед"), state=None)
async def user_connect(message: types.Message):
    if isGameStarted():
        if usersCount() < getMaxUsersValue():
            chat_id = message.chat.id
            connectUser(chat_id)

            keyboard = types.InlineKeyboardMarkup()
            await message.answer("<b>Вы присоединились</b>, ожидайте свою карточку", reply_markup=ReplyKeyboardRemove())
            await message.answer_dice(emoji="🎰")

            card_id = addCardToUser(chat_id)
            button = types.InlineKeyboardButton(
                text=f"Я выиграл!",
                callback_data=cardClose.new(
                    card_id=card_id, chat_id=chat_id, action="del")
            )
            keyboard.add(button)
            print(f"{card_id} выпала")
            await message.answer(f"Ваша карта <b>{card_id}</b>")
            await message.answer_photo(photo=open(f'cards/loto-{card_id}.jpg', 'rb'),
                                       reply_markup=keyboard)
        else:
            await message.answer("Комната заполнена")

    else:
        await message.answer("Игра еще не началась")


@dp.callback_query_handler(cardClose.filter(action="del"))
async def win_check(call: types.CallbackQuery, callback_data: dict):

    card_id = int(callback_data["card_id"])
    chat_id = int(callback_data["chat_id"])
    twitch_name = getTwitchName(chat_id)

    isWin(chat_id)

    if not isWin(chat_id):
        if isGameStarted():
            await bot.send_message(call.from_user.id, 'Вы не собрали нужные числа!')
        else:
            await bot.send_message(call.from_user.id, 'Победитель определен,'
                                   ' в следующий раз вы успеете нажать кнопку быстрее него')
        await call.answer()
    else:
        try:
            await bot.delete_message(call.message.chat.id, call.message.message_id - 1)
            await call.message.delete()
        except:
            print("Строка 62")

        await bot.send_message(call.from_user.id, 'Карта отправлена на проверку\n'
                                                  'по тех вопросам к @mironchikk')

        for chat_id in getAdmins():
            await bot.send_message(chat_id, f"Победил! \n <b>{twitch_name}</b>")
            await bot.send_photo(chat_id, photo=open(f'cards/loto-{card_id}.jpg', 'rb'))
        await call.answer()


@dp.message_handler(Text(equals="I want to be an admin of this bot"), state=None)
async def get_admin(message: types.Message):
    try:
        if not isAdmin(message.chat.id):
            addAdmin(message.chat.id)
            await message.answer("Ты стал админом")
        else:
            await message.answer("Ты уже админ")
    except:
        await message.answer("Что-то пошло не так")
