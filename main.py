from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import os
import uuid

app = FastAPI()

# Папка для хранения изображений
IMAGE_DIR = "images"
os.makedirs(IMAGE_DIR, exist_ok=True)

# Раздача файлов по URL /images/filename
app.mount("/images", StaticFiles(directory=IMAGE_DIR), name="images")


@app.post("/upload/image")
async def upload_image(file: UploadFile = File(...)):
    # Генерируем уникальное имя файла
    ext = os.path.splitext(file.filename)[1]
    filename = f"{uuid.uuid4().hex}{ext}"
    path = os.path.join(IMAGE_DIR, filename)
    
    # Сохраняем файл
    with open(path, "wb") as f:
        f.write(await file.read())
    
    # Возвращаем прямую ссылку
    url = f"/images/{filename}"
    return JSONResponse({"url": url})
