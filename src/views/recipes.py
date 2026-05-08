import uuid
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from database import supabase
from dependencies import get_current_user

router = APIRouter(prefix="/recipes", tags=["recipes"])


class RecipeCreate(BaseModel):
    name: str
    cuisine: Optional[str] = None
    notes: Optional[str] = None
    ingredients: List[str] = []


def _ordinal(n: int) -> str:
    if 11 <= n % 100 <= 13:
        return f"{n}th"
    return f"{n}" + {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")


def _fmt_last_made(date_str: Optional[str]) -> Optional[str]:
    if not date_str:
        return None
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return f"{dt.strftime('%b')} {_ordinal(dt.day)}, {dt.year}"
    except Exception:
        return date_str


def _fmt_recipe(r: dict, user_profile: dict) -> dict:
    ingredients = [
        ri["ingredient_name"]
        for ri in sorted(
            r.get("recipe_ingredients") or [], key=lambda x: x.get("sort_order", 0)
        )
    ]
    return {
        "id": r["id"],
        "name": r["name"],
        "cuisine": r.get("cuisine"),
        "creatorColor": "#5A6E7F",
        "creatorUsername": user_profile.get("username"),
        "creatorAvatarUrl": user_profile.get("avatar_url") or "",
        "lastMade": _fmt_last_made(r.get("last_made")),
        "ingredients": ingredients,
        "notes": r.get("notes") or "",
    }


def _get_user_profile(user_id: str) -> dict:
    result = (
        supabase.table("users")
        .select("username, avatar_url")
        .eq("id", user_id)
        .single()
        .execute()
    )
    return result.data or {}


@router.get("")
async def get_recipes(user: dict = Depends(get_current_user)):
    user_profile = _get_user_profile(user["id"])
    result = (
        supabase.table("recipes")
        .select("*, recipe_ingredients(ingredient_name, sort_order)")
        .eq("user_id", user["id"])
        .order("created_at", desc=True)
        .execute()
    )
    return [_fmt_recipe(r, user_profile) for r in result.data]


@router.post("", status_code=201)
async def create_recipe(body: RecipeCreate, user: dict = Depends(get_current_user)):
    recipe_id = str(uuid.uuid4())
    recipe_row = {
        "id": recipe_id,
        "user_id": user["id"],
        "name": body.name.upper(),
        "cuisine": body.cuisine,
        "notes": body.notes,
    }
    result = supabase.table("recipes").insert(recipe_row).execute()
    if not result.data:
        raise HTTPException(status_code=500, detail="Failed to create recipe")

    if body.ingredients:
        ingredient_rows = [
            {"recipe_id": recipe_id, "ingredient_name": name, "sort_order": i}
            for i, name in enumerate(body.ingredients)
        ]
        supabase.table("recipe_ingredients").insert(ingredient_rows).execute()

    user_profile = _get_user_profile(user["id"])
    recipe = result.data[0]
    recipe["recipe_ingredients"] = [
        {"ingredient_name": name, "sort_order": i}
        for i, name in enumerate(body.ingredients)
    ]
    return _fmt_recipe(recipe, user_profile)


@router.delete("/{recipe_id}", status_code=204)
async def delete_recipe(recipe_id: str, user: dict = Depends(get_current_user)):
    result = (
        supabase.table("recipes")
        .delete()
        .eq("id", recipe_id)
        .eq("user_id", user["id"])
        .execute()
    )
    if not result.data:
        raise HTTPException(status_code=404, detail="Recipe not found")
