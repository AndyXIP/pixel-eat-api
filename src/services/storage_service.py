from fastapi import UploadFile
from database import supabase
from config import settings
import uuid


async def upload_post_photo(file: UploadFile, user_id: str) -> str:
    """Upload a post photo to Supabase Storage. Returns the public URL."""
    filename = file.filename or ""
    ext = filename.rsplit(".", 1)[-1] if "." in filename else "jpg"
    path = f"{user_id}/{uuid.uuid4()}.{ext}"
    contents = await file.read()

    supabase.storage.from_(settings.storage_bucket).upload(
        path=path,
        file=contents,
        file_options={"content-type": file.content_type or "image/jpeg"},
    )

    public_url = supabase.storage.from_(settings.storage_bucket).get_public_url(path)
    return public_url
