from fastapi import HTTPException, UploadFile, status
from datetime import datetime, timedelta
from typing import List
from database import supabase
from schemas.post import PostCreate, PostResponse
from services import storage_service, badge_service
import uuid

VALID_VESSEL_TYPES = {"bowl", "plate", "box", "wrap", "cup", "other"}


async def create_post(
    post_data: PostCreate,
    photo: UploadFile,
    user: dict,
) -> dict:
    # 1. Validate vessel type
    if post_data.vessel_type not in VALID_VESSEL_TYPES:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid vessel_type. Must be one of: {', '.join(VALID_VESSEL_TYPES)}",
        )

    # 2. Validate ingredient IDs exist and are currently available
    await _validate_ingredients(post_data.ingredient_ids)

    # 3. Upload photo
    photo_url = await storage_service.upload_post_photo(photo, user["id"])

    # 4. Save post row
    now = datetime.utcnow()
    post_id = uuid.uuid4()
    post_row = {
        "id": str(post_id),
        "user_id": user["id"],
        "photo_url": photo_url,
        "vessel_type": post_data.vessel_type,
        "is_hot": post_data.is_hot,
        "caption": post_data.caption,
        "posted_at": now.isoformat(),
        "expires_at": (now + timedelta(days=30)).isoformat(),
        "late_post_mins": post_data.late_post_mins,
    }
    supabase.table("posts").insert(post_row).execute()

    # 5. Save post_ingredients rows
    post_ingredients = [
        {
            "post_id": str(post_id),
            "ingredient_id": str(ing_id),
            "added_at": now.isoformat(),
            "post_time": True,
            "ai_suggested": False,
            "user_confirmed": True,
        }
        for ing_id in post_data.ingredient_ids
    ]
    if post_ingredients:
        supabase.table("post_ingredients").insert(post_ingredients).execute()

    # 6. Run badge evaluation
    new_badges = await badge_service.evaluate_badges(user["id"], post_id)

    return {**post_row, "badges_earned": new_badges}


async def _validate_ingredients(ingredient_ids: List[uuid.UUID]) -> None:
    if not ingredient_ids:
        return

    from datetime import date
    today = date.today().isoformat()

    result = (
        supabase.table("ingredients")
        .select("id, tier, available_from, available_until")
        .in_("id", [str(i) for i in ingredient_ids])
        .execute()
    )

    found_ids = {row["id"] for row in result.data}
    requested_ids = {str(i) for i in ingredient_ids}

    missing = requested_ids - found_ids
    if missing:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Unknown ingredient IDs: {missing}",
        )

    for row in result.data:
        if row["tier"] == "always":
            continue
        available_from = row.get("available_from")
        available_until = row.get("available_until")
        if available_from and available_until:
            if not (available_from <= today <= available_until):
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"Ingredient {row['id']} is not currently available.",
                )
