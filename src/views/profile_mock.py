from fastapi import APIRouter
from mock_data import PROFILE

router = APIRouter(prefix="/profile", tags=["profile"])

@router.get("/me")
async def get_my_profile():
    return PROFILE
