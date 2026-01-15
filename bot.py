import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from config import BOT_TOKEN, IMAGE_DIR, MUSIC_DIR, ALLOWED_IMAGE_TYPES, ALLOWED_MUSIC_TYPES, MAX_FILE_SIZE
from utils import generate_filename

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

async def check_file_size(file_bytes: bytes):
    return len(file_bytes) <= MAX_FILE_SIZE

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.reply("Привет! Я бот-хостинг. Пришли мне изображение или аудио, и я дам ссылку на него.")

@dp.message_handler(content_types=types.ContentType.PHOTO)
async def handle_photo(message: types.Message):
    photo = message.photo[-1]
    file = await bot.get_file(photo.file_id)
    file_bytes = await bot.download_file(file.file_path)
    data = file_bytes.read()

    if not await check_file_size(data):
        await message.reply("Файл слишком большой. Максимум 10 МБ.")
        return

    filename = generate_filename("photo.jpg")
    path = os.path.join(IMAGE_DIR, filename)

    with open(path, "wb") as f:
        f.write(data)

    await message.reply(f"Изображение загружено! Ссылка: {filename}")

@dp.message_handler(content_types=[types.ContentType.AUDIO, types.ContentType.VOICE])
async def handle_audio(message: types.Message):
    audio_file = message.audio if message.audio else message.voice
    file = await bot.get_file(audio_file.file_id)
    file_bytes = await bot.download_file(file.file_path)
    data = file_bytes.read()

    if not await check_file_size(data):
        await message.reply("Файл слишком большой. Максимум 10 МБ.")
        return

    filename = generate_filename(audio_file.file_name if audio_file.file_name else "audio.ogg")
    path = os.path.join(MUSIC_DIR, filename)

    with open(path, "wb") as f:
        f.write(data)

    await message.reply(f"Аудио загружено! Ссылка: {filename}")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
