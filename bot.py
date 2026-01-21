import os
import asyncio
import aiohttp

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.enums import ContentType

BOT_TOKEN = os.getenv("BOT_TOKEN")
BACKEND = "https://media-host-backend.onrender.com"

bot = Bot(BOT_TOKEN)
dp = Dispatcher()


@dp.message(F.content_type == ContentType.PHOTO)
async def handle_photo(message: Message):
    await message.answer("📥 Фото получено, обрабатываю...")

    photo = message.photo[-1]

    try:
        tg_file = await bot.get_file(photo.file_id)
    except Exception as e:
        await message.answer(f"❌ Ошибка get_file:\n{e}")
        return

    tg_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{tg_file.file_path}"

    async with aiohttp.ClientSession() as session:
        async with session.get(tg_url) as r:
            if r.status != 200:
                await message.answer(f"❌ Не скачалось фото, status={r.status}")
                return
            data = await r.read()

        form = aiohttp.FormData()
        form.add_field(
            "file",
            data,
            filename="photo.jpg",
            content_type="image/jpeg"
        )

        async with session.post(f"{BACKEND}/upload/image", data=form) as resp:
            text = await resp.text()

            await message.answer(
                "📨 Ответ backend:\n"
                f"status: {resp.status}\n"
                f"body:\n{text}"
            )

            if resp.status != 200:
                return

            try:
                result = await resp.json()
            except Exception:
                return

    if "url" not in result:
        await message.answer("❌ В ответе нет url")
        return

    full_url = BACKEND + result["url"]

    await message.answer(
        "✅ ГОТОВО!\n\n"
        f"🔗 Прямая ссылка:\n{full_url}"
    )


@dp.message()
async def fallback(message: Message):
    await message.answer("📸 Отправь фото")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
