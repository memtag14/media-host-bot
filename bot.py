import asyncio
import os
import aiohttp

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import CommandStart

BOT_TOKEN = os.getenv("BOT_TOKEN")  # токен из Railway
BACKEND_UPLOAD_URL = "https://media-host-backend.onrender.com/upload/image"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "👋 Пришли мне фото, я загружу его и дам прямую ссылку"
    )


@dp.message(F.photo)
async def handle_photo(message: Message):
    photo = message.photo[-1]  # самое большое фото
    file = await bot.get_file(photo.file_id)

    file_url = (
        f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file.file_path}"
    )

    async with aiohttp.ClientSession() as session:
        # скачиваем фото из Telegram
        async with session.get(file_url) as resp:
            photo_bytes = await resp.read()

        data = aiohttp.FormData()
        data.add_field(
            "file",
            photo_bytes,
            filename="photo.jpg",
            content_type="image/jpeg"
        )

        # отправляем фото на твой backend
        async with session.post(BACKEND_UPLOAD_URL, data=data) as resp:
            if resp.status != 200:
                await message.answer("❌ Ошибка загрузки на сервер")
                return

            result = await resp.json()
            url = result.get("url")

    await message.answer(
        f"✅ Фото загружено!\n\n🔗 Прямая ссылка:\n{url}"
    )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
