from pydantic import BaseModel
from typing import Optional
from enum import Enum
import uuid


class IngredientTier(str, Enum):
    always = "always"
    seasonal_bonus = "seasonal_bonus"
    seasonal_limited = "seasonal_limited"


class Season(str, Enum):
    spring = "spring"
    summer = "summer"
    autumn = "autumn"
    winter = "winter"


class IngredientResponse(BaseModel):
    id: uuid.UUID
    name: str
    display_name: str
    tier: IngredientTier
    season: Optional[Season] = None
    available_from: Optional[str] = None  # date string YYYY-MM-DD
    available_until: Optional[str] = None
    animated: bool
    animation_type: Optional[str] = None
    hot: bool
