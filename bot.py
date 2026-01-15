import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# Загружаем токен из переменной окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("Укажите BOT_TOKEN в переменных окружения")

# Создаём объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Создаём папки для хранения медиа
IMAGE_DIR = "uploads/images"
MUSIC_DIR = "uploads/music"
os.makedirs(IMAGE_DIR, exist_ok=True)
os.makedirs(MUSIC_DIR, exist_ok=True)

# Команда /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет! Я бот для загрузки медиа.\n"
        "Отправьте мне фото или аудио, и я сохраню его."
    )

# Обработчик фото
@dp.message()
async def handle_media(message: types.Message):
    if message.photo:
        photo = message.photo[-1]  # Берём самое большое фото
        filename = f"{photo.file_id}.jpg"
        path = os.path.join(IMAGE_DIR, filename)
        await photo.download(destination_file=path)
        await message.answer(f"Фото сохранено: {filename}")
    elif message.audio:
        audio = message.audio
        filename = f"{audio.file_id}.mp3"
        path = os.path.join(MUSIC_DIR, filename)
        await audio.download(destination_file=path)
        await message.answer(f"Аудио сохранено: {filename}")
    else:
        await message.answer("Пожалуйста, отправьте фото или аудио.")

# Основная функция запуска
async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

# Запуск бота
if __name__ == "__main__":
    asyncio.run(main())
