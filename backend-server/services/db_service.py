from __future__ import annotations

import hashlib
import os
import secrets
from datetime import datetime
from typing import Any, Dict, List, Optional

from database.firebase import init_firestore
from models.listing import ListingCreate, ListingPublic
from models.user import UserCreate, UserInDB, UserPublic


class InMemoryDB:
    """
    Hackathon-ready storage fallback.
    Keeps data in memory for fast demos (data resets on restart).
    """

    def __init__(self) -> None:
        self.users: Dict[str, UserInDB] = {}
        self.listings: Dict[str, ListingPublic] = {}
        self.email_index: Dict[str, str] = {}  # email -> user_id


class DBService:
    """
    Database service that uses Firestore if configured, otherwise in-memory DB.
    """

    def __init__(self) -> None:
        self._firestore = init_firestore()
        self._mem = InMemoryDB()

    @staticmethod
    def _now() -> datetime:
        return datetime.utcnow()

    @staticmethod
    def _new_id(prefix: str) -> str:
        return f"{prefix}_{secrets.token_hex(8)}"

    @staticmethod
    def _hash_password(password: str, salt: str) -> str:
        return hashlib.sha256(f"{salt}:{password}".encode("utf-8")).hexdigest()

    def _get_auth_salt(self) -> str:
        return os.getenv("AUTH_SALT", "smart-agri-ai-demo-salt")

    # -------------------------
    # Users
    # -------------------------
    def create_user(self, payload: UserCreate) -> UserPublic:
        # Firestore path (optional)
        if self._firestore is not None:
            users_ref = self._firestore.collection("users")
            existing = users_ref.where("email", "==", payload.email).limit(1).stream()
            if any(True for _ in existing):
                raise ValueError("Email already registered")

            user_id = self._new_id("usr")
            created_at = self._now()
            password_hash = self._hash_password(payload.password, self._get_auth_salt())
            doc = {
                "id": user_id,
                "name": payload.name,
                "email": payload.email,
                "password_hash": password_hash,
                "created_at": created_at.isoformat(),
            }
            users_ref.document(user_id).set(doc)
            return UserPublic(id=user_id, name=payload.name, email=payload.email, created_at=created_at)

        # In-memory
        if payload.email in self._mem.email_index:
            raise ValueError("Email already registered")

        user_id = self._new_id("usr")
        created_at = self._now()
        password_hash = self._hash_password(payload.password, self._get_auth_salt())
        user = UserInDB(
            id=user_id,
            name=payload.name,
            email=payload.email,
            created_at=created_at,
            password_hash=password_hash,
        )
        self._mem.users[user_id] = user
        self._mem.email_index[payload.email] = user_id
        return UserPublic(id=user_id, name=user.name, email=user.email, created_at=user.created_at)

    def authenticate_user(self, email: str, password: str) -> Optional[UserPublic]:
        password_hash = self._hash_password(password, self._get_auth_salt())

        if self._firestore is not None:
            users_ref = self._firestore.collection("users")
            stream = users_ref.where("email", "==", email).limit(1).stream()
            for doc in stream:
                data = doc.to_dict() or {}
                if data.get("password_hash") == password_hash:
                    created_at = data.get("created_at")
                    dt = datetime.fromisoformat(created_at) if isinstance(created_at, str) else self._now()
                    return UserPublic(id=data["id"], name=data["name"], email=data["email"], created_at=dt)
            return None

        user_id = self._mem.email_index.get(email)
        if not user_id:
            return None
        user = self._mem.users.get(user_id)
        if not user or user.password_hash != password_hash:
            return None
        return UserPublic(id=user.id, name=user.name, email=user.email, created_at=user.created_at)

    # -------------------------
    # Marketplace listings
    # -------------------------
    def create_listing(self, payload: ListingCreate) -> ListingPublic:
        listing_id = self._new_id("lst")
        created_at = self._now()
        listing = ListingPublic(
            id=listing_id,
            seller_user_id=payload.seller_user_id,
            crop_name=payload.crop_name,
            quantity_kg=payload.quantity_kg,
            price_per_kg=payload.price_per_kg,
            location=payload.location,
            notes=payload.notes,
            created_at=created_at,
        )

        if self._firestore is not None:
            self._firestore.collection("listings").document(listing_id).set(
                {
                    **listing.model_dump(),
                    "created_at": created_at.isoformat(),
                }
            )
            return listing

        self._mem.listings[listing_id] = listing
        return listing

    def list_listings(self) -> List[ListingPublic]:
        if self._firestore is not None:
            out: List[ListingPublic] = []
            for doc in self._firestore.collection("listings").stream():
                data = doc.to_dict() or {}
                created_at = data.get("created_at")
                dt = datetime.fromisoformat(created_at) if isinstance(created_at, str) else self._now()
                out.append(
                    ListingPublic(
                        id=data["id"],
                        seller_user_id=data["seller_user_id"],
                        crop_name=data["crop_name"],
                        quantity_kg=float(data["quantity_kg"]),
                        price_per_kg=float(data["price_per_kg"]),
                        location=data["location"],
                        notes=data.get("notes"),
                        created_at=dt,
                    )
                )
            # newest first
            out.sort(key=lambda x: x.created_at, reverse=True)
            return out

        return sorted(self._mem.listings.values(), key=lambda x: x.created_at, reverse=True)