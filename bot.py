import os
import asyncio
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

TOKEN = os.getenv("BOT_TOKEN")
BACKEND_URL = "https://media-host-backend.onrender.com"

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer("👋 Я жив. Отправь фото или музыку — дам прямую ссылку.")


@dp.message(lambda m: m.photo)
async def handle_photo(message: types.Message):
    await message.answer("📥 Фото получено, обрабатываю...")

    photo = message.photo[-1]
    file = await bot.get_file(photo.file_id)
    file_bytes = await bot.download_file(file.file_path)

    files = {
        "file": ("image.jpg", file_bytes, "image/jpeg")
    }

    try:
        r = requests.post(f"{BACKEND_URL}/upload/image", files=files, timeout=30)
        r.raise_for_status()

        url = r.json()["url"]
        await message.answer(
            f"✅ ГОТОВО!\n\n🔗 Прямая ссылка:\n{BACKEND_URL}{url}"
        )

    except Exception as e:
        print("UPLOAD ERROR:", e)
        await message.answer("❌ Ошибка загрузки")


@dp.message(lambda m: m.audio)
async def handle_audio(message: types.Message):
    await message.answer("🎵 Музыка получена, загружаю...")

    audio = message.audio
    file = await bot.get_file(audio.file_id)
    file_bytes = await bot.download_file(file.file_path)

    files = {
        "file": (audio.file_name or "audio.mp3", file_bytes, "audio/mpeg")
    }

    try:
        r = requests.post(f"{BACKEND_URL}/upload/music", files=files, timeout=30)
        r.raise_for_status()

        url = r.json()["url"]
        await message.answer(
            f"✅ ГОТОВО!\n\n🔗 Прямая ссылка:\n{BACKEND_URL}{url}"
        )

    except Exception as e:
        print("UPLOAD ERROR:", e)
        await message.answer("❌ Ошибка загрузки")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
