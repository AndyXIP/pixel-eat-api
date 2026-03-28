from fastapi import APIRouter, Depends
from mock_data import CURRENT_EVENT
from dependencies import get_current_user

router = APIRouter(prefix="/events", tags=["events"])

@router.get("/current")
async def get_current_event(user: dict = Depends(get_current_user)):
    return CURRENT_EVENT
