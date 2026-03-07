from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(tags=["Vendors"])


@router.get("/vendors")
def get_vendors():
    """
    Hackathon demo: returns a static list of nearby vendors/shops.
    """
    return {
        "count": 5,
        "vendors": [
            {"name": "GreenGrow Agro Store", "location": "MG Road, Bengaluru"},
            {"name": "FarmCare Supplies", "location": "Vijayanagar, Mysuru"},
            {"name": "Krishi Kendra", "location": "Ameerpet, Hyderabad"},
            {"name": "AgriMart", "location": "Andheri East, Mumbai"},
            {"name": "Soil & Seed Hub", "location": "Anna Nagar, Chennai"},
        ],
    }