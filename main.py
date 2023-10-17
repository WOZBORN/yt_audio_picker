import os
import asyncio
import logging

from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters.command import Command
from aiogram.types import Message, FSInputFile

from dotenv import load_dotenv

import yt_picker

# Loading TOKEN from .env file
load_dotenv()
TOKEN = os.getenv('TOKEN')

# Making a router (message handler)
router = Router()


@router.message(Command(commands=['audio', 'video']))
async def cmd_start(message: Message):
    await message.answer("Hello!")


@router.message()
async def echo(message: Message):
    if message.text.startswith("https://www.youtube.com/watch"):
        await message.answer("Обработка видео!")
        file = yt_picker.download_audio(message.text)
        if file:
            await message.answer_audio(FSInputFile(file))

    if message.text.startswith("https://www.youtube.com/playlist"):
        await message.answer("Обработка плейлиста!")




async def main():
    # Bot instance initialize
    bot = Bot(token=TOKEN)
    # Making a message handler with Router object
    dp = Dispatcher()
    dp.include_router(router)
    # Start message polling
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())


