from fastapi import APIRouter
from mock_data import CURRENT_EVENT

router = APIRouter(prefix="/events", tags=["events"])

@router.get("/current")
async def get_current_event():
    return CURRENT_EVENT
