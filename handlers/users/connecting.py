from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram import types
from aiogram.dispatcher.filters import Text

from aiogram.utils.callback_data import CallbackData
from services.service import *

cardClose = CallbackData("post", "card_id", "chat_id", "action")
skipCard = CallbackData("post", "action")


@dp.message_handler(Text(equals="Присоединиться"), state=None)
async def userConnect(message: types.Message):
    if (getGameStatus()):
        if(usersCount() < getMaxUsersValue()):
            chat_id = message.chat.id
            connectUser(chat_id)
            card_id = addCardToUser(chat_id)

            keyboard = types.InlineKeyboardMarkup()
            await message.answer("<b>Вы присоединились</b>, ожидайте свою карточку", reply_markup=ReplyKeyboardRemove())
            await message.answer_dice(emoji="🎰")

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
async def process_callback_cardClose(call: types.CallbackQuery, callback_data: dict):

    card_id = int(callback_data["card_id"])
    chat_id = int(callback_data["chat_id"])
    twitch_name = getTwitchName(chat_id)

    isWin(chat_id)

    if (not isWin(chat_id)):
        if(getGameStatus()):
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
            print("Строка 54")

        await bot.send_message(call.from_user.id, 'Карта отправлена на проверку\n'
                                                  'по тех вопросам к @mironchikk')

        #keyboard = types.InlineKeyboardMarkup()
        # button = types.InlineKeyboardButton(
        #    text=f"Скипнуть",
        #    callback_data=skipCard.new(action="skip")
        # )
        # keyboard.add(button)
        for chat_id in getAdmins():
            await bot.send_message(chat_id, f"Победил! \n <b>{twitch_name}</b>")
            await bot.send_photo(chat_id, photo=open(f'cards/loto-{card_id}.jpg', 'rb'))
        await call.answer()
    # except:
    #    await call.message.answer("Карты нет в базе, сори мой косяк, фикс в скором времени")
    #    await call.answer()


@dp.callback_query_handler(skipCard.filter(action="skip"))
async def skipCard_CardClose(call: types.CallbackQuery):
    try:
        await bot.delete_message(call.message.chat.id, call.message.message_id - 1)
    except:
        print("Строка 74")
    await call.message.delete()
    await call.answer()


@dp.message_handler(Text(equals="Нет"), state=None)
async def userConnect(message: types.Message):
    try:
        await bot.delete_message(message.chat.id, message.message_id - 1)
    except:
        await message.answer("ну ок")

    await message.answer("<b>ГАЛЯЯЯ ОТКАААТ!</b>", reply_markup=ReplyKeyboardRemove())


@dp.message_handler(commands=['stop'])
async def stop(message: types.Message):
    if (isAdmin(message.chat.id)):
        print(getGameStatus())
        if (getGameStatus()):
            try:
                for chat_id in getUserMailingInSession():
                    await bot.send_message(chat_id[0], "<b>Игра завершена!</b>\n"
                                                       "по тех вопросам к @mironchikk")
                stopSession()
                await bot.send_message(message.chat.id, "Вы завершили игру")
            except:
                await message.answer("Нет участников")
        else:
            await message.answer("Игра уже закончена!")
    else:
        await message.answer("У вас нет прав")
