from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class Recommendation:
    medicine: str
    fertilizer: str
    tips: str

    def to_dict(self) -> Dict[str, str]:
        return {"medicine": self.medicine, "fertilizer": self.fertilizer, "tips": self.tips}


class RecommendService:
    """
    Backend-side recommendation fallback.

    Note: If your AI model server already returns medicine/fertilizer/tips,
    you can keep this as a backup for demo resiliency.
    """

    _MAP: Dict[str, Recommendation] = {
        "healthy": Recommendation("None required", "Balanced NPK", "Keep monitoring, avoid overwatering."),
        "powdery": Recommendation(
            "Sulfur / Neem oil",
            "Balanced NPK (avoid excess nitrogen)",
            "Improve air flow, reduce humidity, avoid wetting leaves.",
        ),
        "rust": Recommendation(
            "Copper fungicide / Propiconazole",
            "Potassium-rich NPK",
            "Remove infected leaves, rotate crops, ensure drainage.",
        ),
        "early blight": Recommendation(
            "Mancozeb",
            "NPK",
            "Avoid overwatering, remove infected leaves.",
        ),
    }

    def get(self, disease: str) -> Recommendation:
        key = (disease or "").strip().lower().replace("_", " ").replace("-", " ")
        return self._MAP.get(key, Recommendation("Consult expert", "Balanced NPK", "Isolate plant and monitor."))