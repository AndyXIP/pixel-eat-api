from fastapi import APIRouter, Depends
from mock_data import DIARY
from dependencies import get_current_user

router = APIRouter(prefix="/diary", tags=["diary"])

@router.get("")
async def get_diary(user: dict = Depends(get_current_user)):
    return DIARY
