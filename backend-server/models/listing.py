from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ListingBase(BaseModel):
    crop_name: str = Field(..., min_length=1, max_length=80)
    quantity_kg: float = Field(..., gt=0)
    price_per_kg: float = Field(..., gt=0)
    location: str = Field(..., min_length=2, max_length=120)
    notes: Optional[str] = Field(None, max_length=500)


class ListingCreate(ListingBase):
    seller_user_id: str = Field(..., min_length=3)


class ListingPublic(ListingBase):
    id: str
    seller_user_id: str
    created_at: datetime