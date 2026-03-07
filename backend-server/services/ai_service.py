from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Dict, Optional

import requests


@dataclass(frozen=True)
class AIServiceConfig:
    """
    Config for connecting to the AI model server.

    Defaults assume your YOLO API is running locally at port 8000.
    """

    base_url: str
    timeout_s: int = 30

    @staticmethod
    def from_env() -> "AIServiceConfig":
        return AIServiceConfig(
            base_url=os.getenv("AI_MODEL_URL", "http://localhost:8000").rstrip("/"),
            timeout_s=int(os.getenv("AI_MODEL_TIMEOUT_S", "30")),
        )


class AIService:
    """
    Calls an external AI server that exposes POST /predict (multipart file upload).
    """

    def __init__(self, cfg: Optional[AIServiceConfig] = None) -> None:
        self.cfg = cfg or AIServiceConfig.from_env()

    def predict(self, image_bytes: bytes, filename: str = "leaf.jpg", content_type: str = "image/jpeg") -> Dict:
        """
        Forward image to AI server and return prediction fields.
        """
        url = f"{self.cfg.base_url}/predict"
        files = {"file": (filename, image_bytes, content_type)}
        resp = requests.post(url, files=files, timeout=self.cfg.timeout_s)
        resp.raise_for_status()
        data = resp.json()

        # Normalize output for our backend
        return {
            "disease": data.get("disease", "unknown"),
            "confidence": data.get("confidence", 0.0),
            "medicine": data.get("medicine", ""),
            "fertilizer": data.get("fertilizer", ""),
            "tips": data.get("tips", ""),
        }