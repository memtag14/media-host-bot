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
    # 1️⃣ Берём фото
    photo = message.photo[-1]

    # 2️⃣ Получаем файл от Telegram
    tg_file = await bot.get_file(photo.file_id)
    tg_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{tg_file.file_path}"

    async with aiohttp.ClientSession() as session:
        # 3️⃣ Скачиваем фото
        async with session.get(tg_url) as r:
            if r.status != 200:
                await message.answer("❌ Не удалось скачать фото")
                return
            data = await r.read()

        # 4️⃣ Отправляем в backend (ВАЖНО: поле называется file)
        form = aiohttp.FormData()
        form.add_field(
            "file",
            data,
            filename="photo.jpg",
            content_type="image/jpeg"
        )

        async with session.post(f"{BACKEND}/upload/image", data=form) as resp:
            try:
                result = await resp.json()
            except Exception:
                text = await resp.text()
                await message.answer(f"❌ Backend вернул не JSON:\n{text}")
                return

    # 5️⃣ Проверяем ответ
    if "url" not in result:
        await message.answer(f"❌ Ошибка загрузки:\n{result}")
        return

    full_url = BACKEND + result["url"]

    # 6️⃣ Отдаём ПРЯМУЮ ссылку
    await message.answer(
        "✅ Фото загружено!\n\n"
        f"🔗 Прямая ссылка:\n{full_url}"
    )


@dp.message()
async def fallback(message: Message):
    await message.answer("📸 Отправь фото — я верну прямую ссылку")


async def main():
    print("Bot started")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
