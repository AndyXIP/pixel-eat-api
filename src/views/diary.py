import calendar
from fastapi import APIRouter, Depends
from database import supabase
from dependencies import get_current_user
from datetime import datetime, timezone, timedelta
from typing import Any, cast

router = APIRouter(prefix="/diary", tags=["diary"])


MONTH_NAMES = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]


def _ordinal(n: int) -> str:
    if 11 <= n % 100 <= 13:
        return f"{n}th"
    return f"{n}" + {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")


def _parse_dt(dt_str: str) -> datetime:
    dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def _day_streak(posts_data: list[dict[str, Any]]) -> int:
    """Count consecutive days ending today that have at least one post."""
    today = datetime.now(timezone.utc).date()
    days_with_posts = set()
    for p in posts_data:
        try:
            days_with_posts.add(_parse_dt(p["posted_at"]).date())
        except Exception:
            pass
    streak = 0
    current = today
    while current in days_with_posts:
        streak += 1
        current -= timedelta(days=1)
    return streak


@router.get("/dishes")
async def get_dish_history(user: dict = Depends(get_current_user)):
    """All dishes the user has cooked, newest first, with full date strings."""
    result = (
        supabase.table("posts")
        .select(
            "id, photo_url, vessel_type, caption, posted_at, post_ingredients(ingredient_id, ingredients(name))"
        )
        .eq("user_id", user["id"])
        .order("posted_at", desc=True)
        .execute()
    )
    dishes = []
    for p in cast(list[dict[str, Any]], result.data):
        dt = _parse_dt(p["posted_at"])
        ingredient_names = [
            cast(dict[str, Any], pi["ingredients"])["name"]
            for pi in cast(list[dict[str, Any]], p.get("post_ingredients") or [])
            if pi.get("ingredients")
        ]
        dishes.append(
            {
                "id": p["id"],
                "date": f"{MONTH_NAMES[dt.month - 1]} {_ordinal(dt.day)}, {dt.year}",
                "photoUrl": p["photo_url"],
                "name": p.get("caption") or p["vessel_type"],
                "cuisine": None,
                "ingredients": ingredient_names,
                "recipe": None,
            }
        )
    return dishes


@router.get("")
async def get_diary(user: dict = Depends(get_current_user)):
    now = datetime.now(timezone.utc)
    year, month = now.year, now.month
    _, days_in_month = calendar.monthrange(year, month)
    month_start = datetime(year, month, 1, tzinfo=timezone.utc)
    month_end = datetime(year, month, days_in_month, 23, 59, 59, tzinfo=timezone.utc)

    # All user posts (for streak + total stats)
    all_posts_result = (
        supabase.table("posts")
        .select(
            "id, photo_url, vessel_type, caption, posted_at, post_ingredients(ingredient_id, ingredients(name))"
        )
        .eq("user_id", user["id"])
        .order("posted_at", desc=True)
        .execute()
    )
    all_posts = cast(list[dict[str, Any]], all_posts_result.data)

    # Filter to this month (ascending for calendar)
    month_posts = sorted(
        [
            p
            for p in all_posts
            if _parse_dt(p["posted_at"]).year == year
            and _parse_dt(p["posted_at"]).month == month
        ],
        key=lambda p: p["posted_at"],
    )

    # loggedDays: one entry per unique day (first post of each day)
    logged_days = []
    seen_days: set = set()
    for p in month_posts:
        day = _parse_dt(p["posted_at"]).day
        if day not in seen_days:
            seen_days.add(day)
            logged_days.append(
                {"day": day, "photoUrl": p["photo_url"], "caption": p.get("caption")}
            )

    # dishesThisWeek: posts in the last 7 days, padded to 6 slots
    week_ago = now - timedelta(days=7)
    week_posts = [p for p in all_posts if _parse_dt(p["posted_at"]) >= week_ago]
    dishes_this_week = []
    for p in week_posts[:6]:
        ingredient_names = [
            cast(dict[str, Any], pi["ingredients"])["name"]
            for pi in cast(list[dict[str, Any]], p.get("post_ingredients") or [])
            if pi.get("ingredients")
        ]
        dishes_this_week.append(
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
    while len(dishes_this_week) < 6:
        dishes_this_week.append(
            {
                "id": f"empty-{len(dishes_this_week)}",
                "bg": "#E8E4E0",
                "imageUrl": None,
                "name": None,
                "cuisine": None,
                "ingredients": [],
                "recipe": None,
            }
        )

    # Recipes stats
    all_recipes_result = (
        supabase.table("recipes")
        .select("id, created_at")
        .eq("user_id", user["id"])
        .execute()
    )
    all_recipes = cast(list[dict[str, Any]], all_recipes_result.data)
    new_recipes_count = sum(
        1 for r in all_recipes if month_start <= _parse_dt(r["created_at"]) <= month_end
    )

    # Active event for challenge data
    event_result = (
        supabase.table("events")
        .select(
            "title, description, event_ingredients(label, image_key), event_featured_recipes(recipe_name)"
        )
        .lte("starts_at", now.isoformat())
        .gte("ends_at", now.isoformat())
        .limit(1)
        .execute()
    )
    events_data = cast(list[dict[str, Any]], event_result.data)
    event = events_data[0] if events_data else None

    challenge_title = event["title"] if event else None
    challenge_detail = None
    if event:
        challenge_detail = {
            "title": event["title"],
            "description": event.get("description") or "",
            "ingredients": [
                {"label": ei["label"], "imageKey": ei["image_key"]}
                for ei in cast(
                    list[dict[str, Any]], event.get("event_ingredients") or []
                )
            ],
            "featuredRecipes": [
                er["recipe_name"]
                for er in cast(
                    list[dict[str, Any]], event.get("event_featured_recipes") or []
                )
            ],
        }

    dishes_logged = len(month_posts)
    return {
        "month": now.strftime("%B %Y"),
        "year": year,
        "monthIndex": month - 1,
        "loggedDays": logged_days,
        "stats": {
            "recipesShared": len(all_recipes),
            "dishesLogged": len(all_posts),
            "newRecipes": new_recipes_count,
            "challengeRecipes": 0,
            "dayStreak": _day_streak(all_posts),
        },
        "challengeTitle": challenge_title,
        "challengeDetail": challenge_detail,
        "lanternProgress": {
            "filled": dishes_logged,
            "total": 10,
            "mealsUntilBadge": max(0, 10 - dishes_logged),
        },
        "dishesThisWeek": dishes_this_week,
    }
