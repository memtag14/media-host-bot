import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# Загружаем токен из переменных окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("Укажите BOT_TOKEN в переменных окружения")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Папки для сохранения медиа
IMAGE_DIR = "uploads/images"
MUSIC_DIR = "uploads/music"
os.makedirs(IMAGE_DIR, exist_ok=True)
os.makedirs(MUSIC_DIR, exist_ok=True)

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет! Я бот для загрузки медиа.\n"
        "Отправьте мне фото или аудио, и я сохраню его."
    )

@dp.message()
async def handle_media(message: types.Message):
    if message.photo:
        # Берём самое большое фото
        photo = message.photo[-1]
        filename = f"{photo.file_id}.jpg"
        path = os.path.join(IMAGE_DIR, filename)
        file = await bot.get_file(photo.file_id)
        await bot.download_file(file.file_path, path)
        await message.answer(f"Фото сохранено: {filename}")

    elif message.audio:
        audio = message.audio
        filename = f"{audio.file_id}.mp3"
        path = os.path.join(MUSIC_DIR, filename)
        file = await bot.get_file(audio.file_id)
        await bot.download_file(file.file_path, path)
        await message.answer(f"Аудио сохранено: {filename}")

    else:
        await message.answer("Пожалуйста, отправьте фото или аудио.")

async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
