from fastapi import APIRouter, Depends
from dependencies import get_current_user
from database import supabase
import uuid

router = APIRouter(prefix="/users", tags=["badges"])


@router.get("/{user_id}/badges")
async def get_user_badges(user_id: uuid.UUID, user: dict = Depends(get_current_user)):
    result = (
        supabase.table("user_badges")
        .select("earned_at, post_id, badges(*)")
        .eq("user_id", str(user_id))
        .order("earned_at", desc=True)
        .execute()
    )
    return result.data
