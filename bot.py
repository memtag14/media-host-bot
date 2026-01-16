import os
import uuid
import aiohttp
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.enums import ContentType
from dotenv import load_dotenv
import asyncio

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
BACKEND_URL = "https://media-host-backend.onrender.com"

bot = Bot(BOT_TOKEN)
dp = Dispatcher()


@dp.message(F.content_type == ContentType.PHOTO)
async def handle_photo(message: Message):
    photo = message.photo[-1]

    file = await bot.get_file(photo.file_id)
    file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file.file_path}"

    async with aiohttp.ClientSession() as session:
        async with session.get(file_url) as resp:
            image_bytes = await resp.read()

        data = aiohttp.FormData()
        data.add_field(
            "file",
            image_bytes,
            filename=f"{uuid.uuid4()}.jpg",
            content_type="image/jpeg",
        )

        async with session.post(
            f"{BACKEND_URL}/upload/image",
            data=data
        ) as upload:
            result = await upload.json()

    image_path = result["url"]
    full_url = f"{BACKEND_URL}{image_path}"

    await message.answer(
        "✅ Фото загружено!\n\n"
        f"🔗 Прямая ссылка:\n{full_url}"
    )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
