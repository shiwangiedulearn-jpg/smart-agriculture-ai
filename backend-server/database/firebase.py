from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class FirebaseConfig:
    """
    Hackathon-friendly Firebase config.

    Supported options:
    - FIREBASE_SERVICE_ACCOUNT_PATH: path to service account JSON file
    - FIREBASE_SERVICE_ACCOUNT_JSON: JSON string of service account (optional)
    - FIREBASE_PROJECT_ID: used for sanity checks/logging
    """

    service_account_path: Optional[str] = None
    service_account_json: Optional[str] = None
    project_id: Optional[str] = None

    @staticmethod
    def from_env() -> "FirebaseConfig":
        return FirebaseConfig(
            service_account_path=os.getenv("FIREBASE_SERVICE_ACCOUNT_PATH"),
            service_account_json=os.getenv("FIREBASE_SERVICE_ACCOUNT_JSON"),
            project_id=os.getenv("FIREBASE_PROJECT_ID"),
        )


def init_firestore():
    """
    Initialize Firestore client if credentials are available.
    Returns firestore.Client or None if not configured.
    """
    try:
        import firebase_admin
        from firebase_admin import credentials, firestore
    except Exception:
        return None

    try:
        if firebase_admin._apps:
            return firestore.client()
    except Exception:
        # Continue to initialization attempt below
        pass

    cfg = FirebaseConfig.from_env()

    cred_obj = None
    if cfg.service_account_path and os.path.exists(cfg.service_account_path):
        cred_obj = credentials.Certificate(cfg.service_account_path)
    elif cfg.service_account_json:
        try:
            cred_obj = credentials.Certificate(json.loads(cfg.service_account_json))
        except Exception:
            cred_obj = None

    if cred_obj is None:
        return None

    try:
        firebase_admin.initialize_app(cred_obj)
        return firestore.client()
    except Exception:
        return None