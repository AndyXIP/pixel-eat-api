from fastapi import APIRouter
from mock_data import FEED_POSTS

router = APIRouter(prefix="/feed", tags=["feed"])

@router.get("")
async def get_feed():
    return FEED_POSTS
