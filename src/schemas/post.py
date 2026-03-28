from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import uuid


class PostIngredientIn(BaseModel):
    ingredient_id: uuid.UUID


class PostCreate(BaseModel):
    vessel_type: str
    is_hot: bool
    caption: Optional[str] = None
    late_post_mins: int = 0
    ingredient_ids: List[uuid.UUID]


class PostResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    photo_url: str
    vessel_type: str
    is_hot: bool
    caption: Optional[str] = None
    posted_at: datetime
    expires_at: datetime
    late_post_mins: int


class FeedPost(PostResponse):
    user_username: str
    user_display_name: str
    user_avatar_url: Optional[str] = None
    ingredient_ids: List[uuid.UUID] = []
