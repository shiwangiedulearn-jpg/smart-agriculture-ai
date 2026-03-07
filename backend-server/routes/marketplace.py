from __future__ import annotations

from fastapi import APIRouter, HTTPException

from models.listing import ListingCreate
from services.db_service import DBService

router = APIRouter(tags=["Marketplace"])


@router.post("/sell-crop")
def sell_crop(payload: ListingCreate):
    """
    Create a crop listing (sell).
    """
    db = DBService()
    try:
        listing = db.create_listing(payload)
        return {"message": "listed", "listing": listing.model_dump()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/buy-crops")
def buy_crops():
    """
    List available crop listings (buy).
    """
    db = DBService()
    listings = db.list_listings()
    return {"count": len(listings), "items": [x.model_dump() for x in listings]}