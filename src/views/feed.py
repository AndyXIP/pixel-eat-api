from fastapi import APIRouter, Depends
from database import supabase
from dependencies import get_current_user
from datetime import datetime, timezone

router = APIRouter(prefix="/feed", tags=["feed"])


def _ordinal(n: int) -> str:
    if 11 <= n % 100 <= 13:
        return f"{n}th"
    return f"{n}" + {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")


def _fmt_date(dt_str: str) -> str:
    try:
        dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
        return f"{dt.strftime('%B')} {_ordinal(dt.day)}"
    except Exception:
        return ""


def _time_ago(dt_str: str) -> str:
    try:
        dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
        now = datetime.now(timezone.utc)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        diff = int((now - dt).total_seconds())
        if diff < 60:
            return "just now"
        if diff < 3600:
            m = diff // 60
            return f"{m} min{'s' if m != 1 else ''} ago"
        if diff < 86400:
            h = diff // 3600
            return f"{h} hour{'s' if h != 1 else ''} ago"
        d = diff // 86400
        return f"{d} day{'s' if d != 1 else ''} ago"
    except Exception:
        return ""


def _fmt_post(p: dict) -> dict:
    user = p.get("users") or {}
    ingredient_names = [
        pi["ingredients"]["name"]
        for pi in (p.get("post_ingredients") or [])
        if pi.get("ingredients")
    ]
    return {
        "id": p["id"],
        "photoUrl": p["photo_url"],
        "cuisine": None,
        "user": {
            "id": p["user_id"],
            "displayName": user.get("display_name", ""),
            "username": user.get("username", ""),
            "avatarUrl": user.get("avatar_url") or "",
        },
        "date": _fmt_date(p["posted_at"]),
        "caption": p.get("caption"),
        "timeAgo": _time_ago(p["posted_at"]),
        "ingredients": {
            "vessel": p.get("vessel_type"),
            "toppings": ingredient_names,
        },
        "spriteColors": {"bg": "#8B6F47", "accent": "#F0C27F"},
        "isHot": p.get("is_hot", True),
    }


@router.get("")
async def get_feed(user: dict = Depends(get_current_user)):
    follows = (
        supabase.table("follows")
        .select("following_id")
        .eq("follower_id", user["id"])
        .execute()
    )
    following_ids = [f["following_id"] for f in follows.data] + [user["id"]]

    result = (
        supabase.table("posts")
        .select("*, users(display_name, username, avatar_url), post_ingredients(ingredient_id, ingredients(name))")
        .in_("user_id", following_ids)
        .order("posted_at", desc=True)
        .limit(50)
        .execute()
    )
    return [_fmt_post(p) for p in result.data]
