from datetime import date, datetime, timezone
from typing import Any, List, cast
from database import supabase
import uuid


async def evaluate_badges(user_id: str, post_id: uuid.UUID) -> List[dict]:
    """
    Run badge evaluation after a post is created.
    Returns a list of newly earned badge records.
    """
    earned = []

    earned += await _check_seasonal_badges(user_id, post_id)
    earned += await _check_streak_badges(user_id, post_id)

    return earned


async def _check_seasonal_badges(user_id: str, post_id: uuid.UUID) -> List[dict]:
    """Award seasonal badges for any seasonal ingredients used in this post."""
    earned = []
    today = date.today()

    # Get ingredients on this post that are seasonal and currently available
    result = (
        supabase.table("post_ingredients")
        .select(
            "ingredient_id, ingredients(id, season, available_from, available_until, tier)"
        )
        .eq("post_id", str(post_id))
        .execute()
    )

    rows = cast(list[dict[str, Any]], result.data)
    seasonal_ingredient_ids = set()
    for row in rows:
        ing = cast(dict[str, Any], row.get("ingredients"))
        if not ing or ing.get("tier") == "always":
            continue
        available_from = cast(str | None, ing.get("available_from"))
        available_until = cast(str | None, ing.get("available_until"))
        if available_from and available_until:
            if (
                date.fromisoformat(available_from)
                <= today
                <= date.fromisoformat(available_until)
            ):
                seasonal_ingredient_ids.add(ing["id"])

    if not seasonal_ingredient_ids:
        return earned

    # Find seasonal badges whose condition_value matches these ingredients
    badges_result = (
        supabase.table("badges").select("*").eq("condition_type", "seasonal").execute()
    )

    already_earned = _get_already_earned_badge_ids(user_id)

    for badge in cast(list[dict[str, Any]], badges_result.data):
        if badge["id"] in already_earned:
            continue
        condition = cast(dict[str, Any], badge.get("condition_value") or {})
        required_ingredient = condition.get("ingredient_id")
        if required_ingredient and required_ingredient in seasonal_ingredient_ids:
            earned.append(_award_badge(user_id, badge["id"], post_id))

    return earned


async def _check_streak_badges(user_id: str, post_id: uuid.UUID) -> List[dict]:
    """Award streak badges based on consecutive posting days."""
    earned = []

    posts_result = (
        supabase.table("posts")
        .select("posted_at")
        .eq("user_id", user_id)
        .order("posted_at", desc=True)
        .execute()
    )

    streak = _calculate_streak(cast(list[dict[str, Any]], posts_result.data))

    badges_result = (
        supabase.table("badges").select("*").eq("condition_type", "streak").execute()
    )

    already_earned = _get_already_earned_badge_ids(user_id)

    for badge in cast(list[dict[str, Any]], badges_result.data):
        if badge["id"] in already_earned:
            continue
        required_streak = (
            cast(dict[str, Any], badge.get("condition_value") or {})
        ).get("days", 0)
        if streak >= required_streak:
            earned.append(_award_badge(user_id, badge["id"], post_id))

    return earned


def _calculate_streak(posts: list[dict[str, Any]]) -> int:
    if not posts:
        return 0

    dates = sorted(
        {datetime.fromisoformat(p["posted_at"]).date() for p in posts},
        reverse=True,
    )

    streak = 1
    for i in range(1, len(dates)):
        if (dates[i - 1] - dates[i]).days == 1:
            streak += 1
        else:
            break

    return streak


def _get_already_earned_badge_ids(user_id: str) -> set:
    result = (
        supabase.table("user_badges")
        .select("badge_id")
        .eq("user_id", user_id)
        .execute()
    )
    return {row["badge_id"] for row in cast(list[dict[str, Any]], result.data)}


def _award_badge(user_id: str, badge_id: str, post_id: uuid.UUID) -> dict:
    record = {
        "user_id": user_id,
        "badge_id": badge_id,
        "post_id": str(post_id),
        "earned_at": datetime.now(timezone.utc).isoformat(),
    }
    supabase.table("user_badges").insert(record).execute()
    return record
