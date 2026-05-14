from fastapi import APIRouter, Depends, HTTPException
from database import supabase
from dependencies import get_current_user
from datetime import datetime, timezone, timedelta
from collections import Counter
from typing import Any, cast

router = APIRouter(prefix="/profile", tags=["profile"])


def _week_streak(posts_data: list[dict[str, Any]]) -> int:
    """Count consecutive weeks ending this week that have at least one post."""
    now = datetime.now(timezone.utc)
    week_start = now - timedelta(days=now.weekday())
    week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)

    weeks_with_posts = set()
    for p in posts_data:
        try:
            dt = datetime.fromisoformat(p["posted_at"].replace("Z", "+00:00"))
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            ws = dt - timedelta(days=dt.weekday())
            ws = ws.replace(hour=0, minute=0, second=0, microsecond=0)
            weeks_with_posts.add(ws.date())
        except Exception:
            pass

    streak = 0
    current = week_start
    while current.date() in weeks_with_posts:
        streak += 1
        current -= timedelta(weeks=1)
    return streak


@router.get("/me")
async def get_my_profile(user: dict = Depends(get_current_user)):
    user_result = (
        supabase.table("users")
        .select("id, username, display_name, avatar_url")
        .eq("id", user["id"])
        .single()
        .execute()
    )
    if not user_result.data:
        raise HTTPException(status_code=404, detail="User not found")
    profile = cast(dict[str, Any], user_result.data)

    posts_result = (
        supabase.table("posts")
        .select(
            "id, photo_url, vessel_type, caption, posted_at, post_ingredients(ingredient_id, ingredients(name))"
        )
        .eq("user_id", user["id"])
        .order("posted_at", desc=True)
        .execute()
    )
    posts_data = cast(list[dict[str, Any]], posts_result.data)

    recipes_result = (
        supabase.table("recipes").select("id").eq("user_id", user["id"]).execute()
    )
    recipes_count = len(cast(list[dict[str, Any]], recipes_result.data))

    badges_result = (
        supabase.table("user_badges").select("id").eq("user_id", user["id"]).execute()
    )
    badges_count = len(cast(list[dict[str, Any]], badges_result.data))

    ingredient_counter: Counter = Counter()
    for p in posts_data:
        for pi in cast(list[dict[str, Any]], p.get("post_ingredients") or []):
            if pi.get("ingredients"):
                ingredient_counter[cast(dict[str, Any], pi["ingredients"])["name"]] += 1
    total_uses = sum(ingredient_counter.values()) or 1
    top_ingredients = [
        {"label": name, "pct": round(count / total_uses, 2)}
        for name, count in ingredient_counter.most_common(3)
    ]

    pinned = []
    for p in posts_data[:3]:
        ingredient_names = [
            cast(dict[str, Any], pi["ingredients"])["name"]
            for pi in cast(list[dict[str, Any]], p.get("post_ingredients") or [])
            if pi.get("ingredients")
        ]
        pinned.append(
            {
                "id": p["id"],
                "bg": "#8B6F47",
                "imageUrl": p["photo_url"],
                "name": p.get("caption") or p["vessel_type"],
                "cuisine": None,
                "ingredients": ingredient_names,
                "recipe": None,
            }
        )

    return {
        "displayName": profile.get("display_name", ""),
        "username": profile.get("username", ""),
        "avatarUrl": profile.get("avatar_url") or "",
        "stats": {
            "recipesShared": recipes_count,
            "dishesLogged": len(posts_data),
            "badgesObtained": badges_count,
            "weekStreak": _week_streak(posts_data),
        },
        "pinnedDishes": pinned,
        "ingredientData": top_ingredients,
        "cuisineData": [],
    }
