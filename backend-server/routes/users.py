from __future__ import annotations

from fastapi import APIRouter, HTTPException

from models.user import UserCreate, UserLogin
from services.db_service import DBService

router = APIRouter(tags=["Users"])


@router.post("/register")
def register(payload: UserCreate):
    """
    Register a new user.
    Hackathon demo: uses Firestore if configured, else in-memory storage.
    """
    db = DBService()
    try:
        user = db.create_user(payload)
        return {"message": "registered", "user": user.model_dump()}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
def login(payload: UserLogin):
    """
    Login with email + password.
    Hackathon demo: returns a simple token-like string (not a real JWT).
    """
    db = DBService()
    user = db.authenticate_user(payload.email, payload.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # Demo token: in a real system use JWT
    token = f"demo-token-{user.id}"
    return {"message": "login_success", "token": token, "user": user.model_dump()}