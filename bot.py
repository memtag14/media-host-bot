import asyncio
import os
import uuid

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from dotenv import load_dotenv

# ======================
# НАСТРОЙКИ
# ======================
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

BASE_URL = "https://media-host-backend.onrender.com"  # <-- твой домен
IMAGE_DIR = "images"

os.makedirs(IMAGE_DIR, exist_ok=True)

# ======================
# BOT
# ======================
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(F.photo)
async def handle_photo(message: Message):
    photo = message.photo[-1]  # максимальный размер

    filename = f"{uuid.uuid4()}.jpg"
    path = os.path.join(IMAGE_DIR, filename)

    file = await bot.get_file(photo.file_id)
    await bot.download_file(file.file_path, path)

    url = f"{BASE_URL}/images/{filename}"

    await message.answer(
        f"✅ Фото загружено!\n\n"
        f"🔗 Прямая ссылка:\n{url}"
    )


@dp.message()
async def fallback(message: Message):
    await message.answer("📷 Отправь фото — я дам прямую ссылку")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
