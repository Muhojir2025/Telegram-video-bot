import logging
from aiogram import Bot, Dispatcher, executor, types
import yt_dlp
import os

API_TOKEN = "ВАШ_ТОКЕН_ОТСЮДА"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Отправь ссылку с YouTube или Instagram, и я скачаю видео.")

@dp.message_handler()
async def download_video(message: types.Message):
    url = message.text.strip()
    if not url.startswith("http"):
        await message.reply("Пожалуйста, пришли правильную ссылку.")
        return

    await message.reply("Скачиваю видео, подождите...")

    try:
        ydl_opts = {
            'outtmpl': 'video.%(ext)s',
            'format': 'mp4',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)

        with open(file_path, 'rb') as video:
            await message.reply_video(video)

        os.remove(file_path)

    except Exception as e:
        await message.reply(f"Ошибка при скачивании: {e}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
