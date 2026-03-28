from fastapi import APIRouter
from mock_data import RECIPES

router = APIRouter(prefix="/recipes", tags=["recipes"])

@router.get("")
async def get_recipes():
    return RECIPES
