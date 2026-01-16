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
    try:
        photo = message.photo[-1]

        # 1️⃣ Получаем файл от Telegram
        tg_file = await bot.get_file(photo.file_id)
        tg_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{tg_file.file_path}"

        async with aiohttp.ClientSession() as session:
            # 2️⃣ Скачиваем файл
            async with session.get(tg_url) as r:
                if r.status != 200:
                    await message.answer("❌ Не смог скачать файл из Telegram")
                    return
                data = await r.read()

            # 3️⃣ Готовим форму (ВАЖНО: поле называется file)
            form = aiohttp.FormData()
            form.add_field(
                name="file",
                value=data,
                filename="photo.jpg",
                content_type="image/jpeg"
            )

            # 4️⃣ Отправляем в backend
            async with session.post(f"{BACKEND}/upload/image", data=form) as resp:
                text = await resp.text()

        # 5️⃣ Пытаемся разобрать JSON
        if resp.status != 200:
            await message.answer(f"❌ Backend ответил {resp.status}")
            return

        try:
            result = eval(text) if text.startswith("{") else None
        except Exception:
            result = None

        if not result or "url" not in result:
            await message.answer(
                "❌ Ошибка загрузки\n\n"
                f"Ответ backend:\n{text}"
            )
            return

        full_url = BACKEND + result["url"]

        await message.answer(
            f"✅ Фото загружено!\n\n🔗 Прямая ссылка:\n{full_url}"
        )

    except Exception as e:
        await message.answer(f"❌ Ошибка:\n{e}")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
