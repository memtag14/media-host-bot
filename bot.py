import os
import requests
from aiogram import Bot, Dispatcher, executor, types

BOT_TOKEN = os.getenv("BOT_TOKEN")
BACKEND_URL = "https://media-host-backend.onrender.com/upload"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start(msg: types.Message):
    await msg.answer("👋 Я жив. Отправь фото или музыку — дам прямую ссылку.")


async def upload_file(file_path: str, filename: str) -> str:
    with open(file_path, "rb") as f:
        r = requests.post(
            BACKEND_URL,
            files={"file": (filename, f)},
            timeout=30
        )

    r.raise_for_status()
    return r.json()["url"]


@dp.message_handler(content_types=types.ContentType.PHOTO)
async def handle_photo(msg: types.Message):
    await msg.answer("📥 Фото получено, обрабатываю...")

    photo = msg.photo[-1]
    file = await bot.get_file(photo.file_id)

    os.makedirs("tmp", exist_ok=True)
    local_path = f"tmp/{photo.file_unique_id}.jpg"
    await bot.download_file(file.file_path, local_path)

    try:
        url_path = await upload_file(local_path, os.path.basename(local_path))
        full_url = f"https://media-host-backend.onrender.com{url_path}"

        await msg.answer(
            "✅ ГОТОВО!\n\n"
            f"🔗 Прямая ссылка:\n{full_url}"
        )

    except Exception:
        await msg.answer("❌ Ошибка загрузки")

    finally:
        os.remove(local_path)


@dp.message_handler(content_types=types.ContentType.AUDIO)
async def handle_audio(msg: types.Message):
    await msg.answer("🎵 Музыка получена, загружаю...")

    audio = msg.audio
    file = await bot.get_file(audio.file_id)

    os.makedirs("tmp", exist_ok=True)
    local_path = f"tmp/{audio.file_unique_id}.mp3"
    await bot.download_file(file.file_path, local_path)

    try:
        url_path = await upload_file(local_path, os.path.basename(local_path))
        full_url = f"https://media-host-backend.onrender.com{url_path}"

        await msg.answer(
            "✅ ГОТОВО!\n\n"
            f"🔗 Прямая ссылка:\n{full_url}"
        )

    except Exception:
        await msg.answer("❌ Ошибка загрузки")

    finally:
        os.remove(local_path)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
import os
import requests
from aiogram import Bot, Dispatcher, executor, types

BOT_TOKEN = os.getenv("BOT_TOKEN")
BACKEND_URL = "https://media-host-backend.onrender.com/upload"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start(msg: types.Message):
    await msg.answer("👋 Я жив. Отправь фото или музыку — дам прямую ссылку.")


async def upload_file(file_path: str, filename: str) -> str:
    with open(file_path, "rb") as f:
        r = requests.post(
            BACKEND_URL,
            files={"file": (filename, f)},
            timeout=30
        )

    r.raise_for_status()
    return r.json()["url"]


@dp.message_handler(content_types=types.ContentType.PHOTO)
async def handle_photo(msg: types.Message):
    await msg.answer("📥 Фото получено, обрабатываю...")

    photo = msg.photo[-1]
    file = await bot.get_file(photo.file_id)

    os.makedirs("tmp", exist_ok=True)
    local_path = f"tmp/{photo.file_unique_id}.jpg"
    await bot.download_file(file.file_path, local_path)

    try:
        url_path = await upload_file(local_path, os.path.basename(local_path))
        full_url = f"https://media-host-backend.onrender.com{url_path}"

        await msg.answer(
            "✅ ГОТОВО!\n\n"
            f"🔗 Прямая ссылка:\n{full_url}"
        )

    except Exception:
        await msg.answer("❌ Ошибка загрузки")

    finally:
        os.remove(local_path)


@dp.message_handler(content_types=types.ContentType.AUDIO)
async def handle_audio(msg: types.Message):
    await msg.answer("🎵 Музыка получена, загружаю...")

    audio = msg.audio
    file = await bot.get_file(audio.file_id)

    os.makedirs("tmp", exist_ok=True)
    local_path = f"tmp/{audio.file_unique_id}.mp3"
    await bot.download_file(file.file_path, local_path)

    try:
        url_path = await upload_file(local_path, os.path.basename(local_path))
        full_url = f"https://media-host-backend.onrender.com{url_path}"

        await msg.answer(
            "✅ ГОТОВО!\n\n"
            f"🔗 Прямая ссылка:\n{full_url}"
        )

    except Exception:
        await msg.answer("❌ Ошибка загрузки")

    finally:
        os.remove(local_path)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
