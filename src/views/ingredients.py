from fastapi import APIRouter, Depends
from datetime import date
from dependencies import get_current_user
from database import supabase

router = APIRouter(prefix="/ingredients", tags=["ingredients"])


@router.get("")
async def list_ingredients(user: dict = Depends(get_current_user)):
    result = supabase.table("ingredients").select("*").execute()
    return result.data


@router.get("/seasonal")
async def list_seasonal_ingredients(user: dict = Depends(get_current_user)):
    today = date.today().isoformat()
    result = (
        supabase.table("ingredients")
        .select("*")
        .neq("tier", "always")
        .lte("available_from", today)
        .gte("available_until", today)
        .execute()
    )
    return result.data
