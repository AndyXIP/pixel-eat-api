from fastapi import APIRouter, Depends
from mock_data import FEED_POSTS
from dependencies import get_current_user

router = APIRouter(prefix="/feed", tags=["feed"])

@router.get("")
async def get_feed(user: dict = Depends(get_current_user)):
    return FEED_POSTS
