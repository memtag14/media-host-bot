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


async def upload_file(local_path: str, filename: str):
    async with aiohttp.ClientSession() as session:
        with open(local_path, "rb") as f:
            data = aiohttp.FormData()
            data.add_field(
                "file",
                f,
                filename=filename,
                content_type="application/octet-stream"
            )

            async with session.post(
                f"{BACKEND_URL}/upload/image",
                data=data
            ) as resp:
                if resp.status != 200:
                    return None
                return await resp.json()


@dp.message()
async def handle_message(message: Message):
    file = None
    filename = None

    # 📷 Фото
    if message.photo:
        photo = message.photo[-1]
        file = await bot.get_file(photo.file_id)
        filename = "image.jpg"

    # 🎵 Музыка
    elif message.audio:
        audio = message.audio
        file = await bot.get_file(audio.file_id)
        filename = audio.file_name or "audio.mp3"

    # 🎤 Голосовое
    elif message.voice:
        voice = message.voice
        file = await bot.get_file(voice.file_id)
        filename = "voice.ogg"

    else:
        await message.answer("Отправь фото 📷 или музыку 🎵")
        return

    # Временный файл
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        temp_path = tmp.name

    # Скачиваем файл из Telegram
    await bot.download_file(file.file_path, temp_path)

    # Загружаем в backend
    result = await upload_file(temp_path, filename)
    os.remove(temp_path)

    if not result or "url" not in result:
        await message.answer("❌ Ошибка загрузки")
        return

    url = result["url"]
    if url.startswith("/"):
        url = BACKEND_URL + url

    await message.answer(
        "✅ Файл загружен!\n\n"
        f"🔗 Прямая ссылка:\n{url}"
    )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
