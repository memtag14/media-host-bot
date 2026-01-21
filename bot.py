import os
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(BOT_TOKEN)
dp = Dispatcher()


@dp.message()
async def test(message: Message):
    await message.answer("✅ Я жив")


async def main():
    print("BOT_TOKEN =", BOT_TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
