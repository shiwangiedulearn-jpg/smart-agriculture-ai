from __future__ import annotations

from fastapi import APIRouter, File, HTTPException, UploadFile

from services.ai_service import AIService
from services.recommend_service import RecommendService

router = APIRouter(tags=["AI"])


@router.post("/predict")
async def predict(file: UploadFile = File(...)):
    """
    Receives an image and forwards it to the AI model server.
    Returns: disease, confidence, medicine, fertilizer, tips
    """
    allowed = {"image/jpeg", "image/jpg", "image/png"}
    if file.content_type not in allowed:
        raise HTTPException(status_code=400, detail=f"Invalid image type: {file.content_type}")

    image_bytes = await file.read()
    if not image_bytes:
        raise HTTPException(status_code=400, detail="Empty file")

    ai = AIService()
    rec = RecommendService()

    try:
        result = ai.predict(
            image_bytes=image_bytes,
            filename=file.filename or "leaf.jpg",
            content_type=file.content_type or "image/jpeg",
        )
    except Exception as e:
        # Hackathon-friendly fallback: still return something usable
        fallback = rec.get("healthy").to_dict()
        return {
            "disease": "unknown",
            "confidence": 0.0,
            **fallback,
            "error": f"AI server not reachable: {e}",
        }

    # If AI server didn't provide recommendations, fill them
    if not result.get("medicine") or not result.get("fertilizer") or not result.get("tips"):
        r = rec.get(result.get("disease", "")).to_dict()
        result = {**result, **r}

    return result