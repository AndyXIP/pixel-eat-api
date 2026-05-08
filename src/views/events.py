from fastapi import APIRouter, Depends, HTTPException
from database import supabase
from dependencies import get_current_user
from datetime import datetime, timezone

router = APIRouter(prefix="/events", tags=["events"])


@router.get("/current")
async def get_current_event(user: dict = Depends(get_current_user)):
    now = datetime.now(timezone.utc).isoformat()
    result = (
        supabase.table("events")
        .select(
            "title, description, event_ingredients(label, image_key), event_featured_recipes(recipe_name)"
        )
        .lte("starts_at", now)
        .gte("ends_at", now)
        .limit(1)
        .execute()
    )
    if not result.data:
        raise HTTPException(status_code=404, detail="No active event")

    event = result.data[0]
    return {
        "title": event["title"],
        "detail": {
            "title": event["title"],
            "description": event.get("description") or "",
            "ingredients": [
                {"label": ei["label"], "imageKey": ei["image_key"]}
                for ei in (event.get("event_ingredients") or [])
            ],
            "featuredRecipes": [
                er["recipe_name"] for er in (event.get("event_featured_recipes") or [])
            ],
        },
        "lanternProgress": {"filled": 0, "total": 10, "mealsUntilBadge": 10},
    }
