from fastapi import APIRouter, Depends
from mock_data import PROFILE
from dependencies import get_current_user

router = APIRouter(prefix="/profile", tags=["profile"])

@router.get("/me")
async def get_my_profile(user: dict = Depends(get_current_user)):
    return PROFILE
