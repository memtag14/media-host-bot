import os
from dotenv import load_dotenv

load_dotenv()  # загружает .env

BOT_TOKEN = os.getenv("BOT_TOKEN")

IMAGE_DIR = "uploads/images"
MUSIC_DIR = "uploads/music"

ALLOWED_IMAGE_TYPES = ["image/png", "image/jpeg", "image/jpg", "image/gif", "image/webp"]
ALLOWED_MUSIC_TYPES = ["audio/mpeg", "audio/mp3", "audio/wav", "audio/ogg"]

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 МБ

os.makedirs(IMAGE_DIR, exist_ok=True)
os.makedirs(MUSIC_DIR, exist_ok=True)
