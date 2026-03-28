from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from typing import List, Optional
import json
import uuid

from app.dependencies import get_current_user
from app.services import post_service
from app.database import supabase

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
    from app.schemas.post import PostCreate
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
