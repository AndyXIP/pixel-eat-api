from pydantic import BaseModel
from typing import Optional
from enum import Enum
import uuid


class NotificationPref(str, Enum):
    lunch = "lunch"
    dinner = "dinner"
    both = "both"


class UserCreate(BaseModel):
    username: str
    display_name: str
    notification_pref: NotificationPref = NotificationPref.both
    notification_time: Optional[str] = None  # "HH:MM"


class UserUpdate(BaseModel):
    display_name: Optional[str] = None
    avatar_url: Optional[str] = None
    notification_pref: Optional[NotificationPref] = None
    notification_time: Optional[str] = None


class UserResponse(BaseModel):
    id: uuid.UUID
    username: str
    display_name: str
    avatar_url: Optional[str] = None
    notification_pref: NotificationPref
    notification_time: Optional[str] = None


class UserProfile(UserResponse):
    post_count: int = 0
    badge_count: int = 0
