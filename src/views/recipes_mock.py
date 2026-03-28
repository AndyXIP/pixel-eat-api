from fastapi import APIRouter, Depends
from mock_data import RECIPES
from dependencies import get_current_user

router = APIRouter(prefix="/recipes", tags=["recipes"])

@router.get("")
async def get_recipes(user: dict = Depends(get_current_user)):
    return RECIPES
