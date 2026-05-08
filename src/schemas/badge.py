from pydantic import BaseModel
from typing import Optional
from enum import Enum
from datetime import datetime
import uuid


class BadgeConditionType(str, Enum):
    seasonal = "seasonal"
    streak = "streak"
    ingredient = "ingredient"
    social = "social"


class BadgeCategory(str, Enum):
    seasonal = "seasonal"
    streak = "streak"
    social = "social"
    special = "special"


class BadgeResponse(BaseModel):
    id: uuid.UUID
    name: str
    description: str
    icon_url: str
    condition_type: BadgeConditionType
    category: BadgeCategory
    display_order: int
    is_secret: bool


class UserBadgeResponse(BaseModel):
    badge: BadgeResponse
    earned_at: datetime
    post_id: Optional[uuid.UUID] = None
