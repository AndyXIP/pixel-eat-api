from fastapi import APIRouter, Depends, HTTPException
from app.dependencies import get_current_user
from app.schemas.user import UserUpdate
from app.database import supabase
import uuid

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{user_id}")
async def get_user(user_id: uuid.UUID, user: dict = Depends(get_current_user)):
    result = (
        supabase.table("users")
        .select("id, username, display_name, avatar_url, notification_pref, notification_time")
        .eq("id", str(user_id))
        .single()
        .execute()
    )
    if not result.data:
        raise HTTPException(status_code=404, detail="User not found")

    post_count = (
        supabase.table("posts").select("id", count="exact").eq("user_id", str(user_id)).execute()
    ).count or 0

    badge_count = (
        supabase.table("user_badges").select("id", count="exact").eq("user_id", str(user_id)).execute()
    ).count or 0

    return {**result.data, "post_count": post_count, "badge_count": badge_count}


@router.put("/me")
async def update_me(updates: UserUpdate, user: dict = Depends(get_current_user)):
    data = updates.model_dump(exclude_none=True)
    if not data:
        raise HTTPException(status_code=422, detail="No fields to update")

    result = (
        supabase.table("users")
        .update(data)
        .eq("id", user["id"])
        .execute()
    )
    return result.data[0] if result.data else {}
