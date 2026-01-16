import asyncio
import os
import aiohttp
import tempfile

from aiogram import Bot, Dispatcher
from aiogram.types import Message

BOT_TOKEN = os.getenv("BOT_TOKEN")
BACKEND_URL = "https://media-host-backend.onrender.com"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message()
async def handle_message(message: Message):
    if not message.photo:
        await message.answer("Отправь фото 📷")
        return

    # Берём самое большое фото
    photo = message.photo[-1]

    # Получаем файл от Telegram
    file = await bot.get_file(photo.file_id)

    # Временный файл
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        temp_path = tmp.name

    # Скачиваем фото
    await bot.download_file(file.file_path, temp_path)

    # Отправляем в backend
    async with aiohttp.ClientSession() as session:
        with open(temp_path, "rb") as f:
            data = aiohttp.FormData()
            data.add_field(
                "file",
                f,
                filename="image.jpg",
                content_type="image/jpeg"
            )

            async with session.post(
                f"{BACKEND_URL}/upload/image",
                data=data
            ) as resp:
                if resp.status != 200:
                    await message.answer("❌ Ошибка загрузки")
                    os.remove(temp_path)
                    return

                result = await resp.json()

    os.remove(temp_path)

    # Формируем АБСОЛЮТНУЮ ссылку
    url = result.get("url")
    if url and url.startswith("/"):
        url = BACKEND_URL + url

    await message.answer(
        "✅ Фото загружено!\n\n"
        f"🔗 Прямая ссылка:\n{url}"
    )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
