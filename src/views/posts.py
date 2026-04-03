from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from typing import List, Optional
from datetime import datetime, timedelta
import json
import uuid

from dependencies import get_current_user
from services import post_service
from database import supabase
from config import settings

router = APIRouter(prefix="/posts", tags=["posts"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_post(
    vessel_type: str = Form(...),
    is_hot: bool = Form(...),
    ingredient_ids: str = Form(...),  # JSON array of UUIDs
    caption: Optional[str] = Form(None),
    late_post_mins: int = Form(0),
    photo: UploadFile = File(...),
    user: dict = Depends(get_current_user),
):
    from schemas.post import PostCreate
    try:
        parsed_ids = [uuid.UUID(i) for i in json.loads(ingredient_ids)]
    except (ValueError, json.JSONDecodeError):
        raise HTTPException(status_code=422, detail="ingredient_ids must be a JSON array of UUIDs")

    post_data = PostCreate(
        vessel_type=vessel_type,
        is_hot=is_hot,
        caption=caption,
        late_post_mins=late_post_mins,
        ingredient_ids=parsed_ids,
    )
    return await post_service.create_post(post_data, photo, user)


# Map frontend vessel names to valid DB vessel types
_VESSEL_MAP = {
    "bowl": "bowl", "plate": "plate", "wrap": "wrap",
    "mug": "cup",   "soup": "bowl",   "pan": "other",
    "sandwich": "other", "pizza": "other",
}


@router.post("/quick", status_code=status.HTTP_201_CREATED)
async def create_quick_post(data: dict, user: dict = Depends(get_current_user)):
    from schemas.post import QuickPostCreate
    body = QuickPostCreate(**data)
    now = datetime.utcnow()
    post_id = str(uuid.uuid4())
    post_row = {
        "id":            post_id,
        "user_id":       user["id"],
        "photo_url":     f"{settings.base_url}/images/mockimages/1.png",
        "vessel_type":   _VESSEL_MAP.get(body.vessel_type, "other"),
        "is_hot":        body.is_hot,
        "caption":       body.caption,
        "posted_at":     now.isoformat(),
        "expires_at":    (now + timedelta(days=30)).isoformat(),
        "late_post_mins": 0,
    }
    result = supabase.table("posts").insert(post_row).execute()
    return result.data[0] if result.data else post_row


@router.get("/{post_id}")
async def get_post(post_id: uuid.UUID, user: dict = Depends(get_current_user)):
    result = (
        supabase.table("posts")
        .select("*, users(username, display_name, avatar_url), post_ingredients(ingredient_id)")
        .eq("id", str(post_id))
        .single()
        .execute()
    )
    if not result.data:
        raise HTTPException(status_code=404, detail="Post not found")
    return result.data
