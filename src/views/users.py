from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from dependencies import get_current_user
from schemas.user import UserUpdate
from services.storage_service import upload_post_photo
from database import supabase
from typing import Any, cast
from postgrest import CountMethod
import uuid

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{user_id}")
async def get_user(user_id: uuid.UUID, user: dict = Depends(get_current_user)):
    result = (
        supabase.table("users")
        .select(
            "id, username, display_name, avatar_url, notification_pref, notification_time"
        )
        .eq("id", str(user_id))
        .single()
        .execute()
    )
    if not result.data:
        raise HTTPException(status_code=404, detail="User not found")

    post_count = (
        supabase.table("posts")
        .select("id", count=CountMethod.exact)
        .eq("user_id", str(user_id))
        .execute()
    ).count or 0

    badge_count = (
        supabase.table("user_badges")
        .select("id", count=CountMethod.exact)
        .eq("user_id", str(user_id))
        .execute()
    ).count or 0

    return {
        **cast(dict[str, Any], result.data),
        "post_count": post_count,
        "badge_count": badge_count,
    }


@router.post("/me/avatar")
async def upload_avatar(
    photo: UploadFile = File(...), user: dict = Depends(get_current_user)
):
    url = await upload_post_photo(photo, user["id"])
    _result = (
        supabase.table("users")
        .update({"avatar_url": url})
        .eq("id", user["id"])
        .execute()
    )
    return {"avatarUrl": url}


@router.put("/me")
async def update_me(updates: UserUpdate, user: dict = Depends(get_current_user)):
    data = updates.model_dump(exclude_none=True)
    if not data:
        raise HTTPException(status_code=422, detail="No fields to update")

    result = supabase.table("users").update(data).eq("id", user["id"]).execute()
    rows = cast(list[dict[str, Any]], result.data)
    return rows[0] if rows else {}
