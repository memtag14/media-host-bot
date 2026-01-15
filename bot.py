import os
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.types import ContentType
from aiogram.filters import Command
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
BACKEND_URL = os.getenv("BACKEND_URL")  # пример: https://media-host-backend.onrender.com

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Привет! Отправь мне фото, и я дам прямую ссылку на него.")

@dp.message(content_types=ContentType.PHOTO)
async def handle_photo(message: types.Message):
    photo = message.photo[-1]  # берём фото наибольшего размера
    file = await photo.download(destination=bytes)  # загружаем в память

    files = {"file": (photo.file_id + ".jpg", file.getvalue())}
    try:
        response = requests.post(f"{BACKEND_URL}/upload/image", files=files)
        data = response.json()
        url = f"{BACKEND_URL}{data['url']}"
        await message.answer(f"Прямая ссылка на фото:\n{url}")
    except Exception as e:
        await message.answer(f"Ошибка при загрузке фото: {e}")

if __name__ == "__main__":
    import asyncio
    from aiogram import F
    from aiogram.utils import exceptions

    async def main():
        try:
            await dp.start_polling(bot)
        except exceptions.TelegramAPIError as e:
            print("Ошибка Telegram API:", e)

    asyncio.run(main())
