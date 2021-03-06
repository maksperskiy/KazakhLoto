from generator.generator import *
from loader import bot, storage
from services.service import *


async def on_shutdown(dp):
    await storage.close()
    await bot.close()


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    generate_images_if_not_exists()
    
    addGame()

    executor.start_polling(dp, on_shutdown=on_shutdown, skip_updates=True)
