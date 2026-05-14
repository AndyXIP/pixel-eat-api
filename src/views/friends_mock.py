from fastapi import APIRouter, Depends, HTTPException
from database import supabase
from dependencies import get_current_user
from typing import Any, cast

router = APIRouter(prefix="/friends", tags=["friends"])


def _fmt(row: dict[str, Any]) -> dict:
    """Convert snake_case user row to camelCase for the frontend."""
    return {
        "id": row["id"],
        "displayName": row.get("display_name") or "",
        "username": row.get("username") or "",
        "avatarUrl": row.get("avatar_url") or "",
    }


@router.get("")
async def get_friends(user: dict = Depends(get_current_user)):
    follows = (
        supabase.table("follows")
        .select("following_id")
        .eq("follower_id", user["id"])
        .execute()
    )
    ids = [f["following_id"] for f in cast(list[dict[str, Any]], follows.data)]
    if not ids:
        return []
    result = (
        supabase.table("users")
        .select("id, username, display_name, avatar_url")
        .in_("id", ids)
        .execute()
    )
    return [_fmt(u) for u in cast(list[dict[str, Any]], result.data)]


@router.get("/search")
async def search_users(q: str = "", user: dict = Depends(get_current_user)):
    base = (
        supabase.table("users")
        .select("id, username, display_name, avatar_url")
        .neq("id", user["id"])
    )
    if q.strip():
        result = base.or_(f"username.ilike.%{q}%,display_name.ilike.%{q}%").execute()
    else:
        result = base.limit(20).execute()
    return [_fmt(u) for u in cast(list[dict[str, Any]], result.data)]


@router.post("/{user_id}")
async def add_friend(user_id: str, user: dict = Depends(get_current_user)):
    if user_id == user["id"]:
        raise HTTPException(status_code=400, detail="Cannot follow yourself")
    supabase.table("follows").upsert(
        {
            "follower_id": user["id"],
            "following_id": user_id,
        }
    ).execute()
    return {"ok": True}


@router.delete("/{user_id}")
async def remove_friend(user_id: str, user: dict = Depends(get_current_user)):
    supabase.table("follows").delete().eq("follower_id", user["id"]).eq(
        "following_id", user_id
    ).execute()
    return {"ok": True}
