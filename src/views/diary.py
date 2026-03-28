from fastapi import APIRouter
from mock_data import DIARY

router = APIRouter(prefix="/diary", tags=["diary"])

@router.get("")
async def get_diary():
    return DIARY
