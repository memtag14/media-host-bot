import uuid
import os

def generate_filename(original_filename: str) -> str:
    ext = os.path.splitext(original_filename)[1]
    unique_name = uuid.uuid4().hex
    return f"{unique_name}{ext}"
