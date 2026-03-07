"""
FastAPI REST API for Crop Disease Detection.
POST /predict - Accepts image, returns disease + recommendations.
"""

from pathlib import Path

from fastapi import FastAPI, File, HTTPException, Query, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from predict import predict_disease
from recommend import get_recommendation

# Initialize FastAPI app
app = FastAPI(
    title="Crop Disease Detection API",
    description="YOLOv8-based crop leaf disease detection with recommendations",
    version="1.0.0",
)

# CORS for hackathon demos (allow all origins)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Model path
MODEL_PATH = Path(__file__).parent / "model" / "best.pt"


@app.get("/")
def root():
    """Health check and API info."""
    return {
        "message": "Crop Disease Detection API",
        "docs": "/docs",
        "predict": "POST /predict with image file",
    }


@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "ok"}


@app.post("/predict")
async def predict(
    file: UploadFile = File(...),
    demo: bool = Query(False, description="Return mock response when model not trained"),
):
    """
    Predict crop disease from uploaded image.

    Input: image file (jpg, png, jpeg)
    Output: disease, confidence, medicine, fertilizer, tips

    Use ?demo=true for mock response when model not trained (hackathon demo).
    """
    # Validate file type
    allowed_types = {"image/jpeg", "image/jpg", "image/png"}
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: jpg, jpeg, png. Got: {file.content_type}",
        )

    # Demo mode: return mock response (for hackathon when model not trained)
    if demo:
        rec = get_recommendation("tomato_early_blight")
        return {
            "disease": "Tomato___Early_blight",
            "confidence": 0.92,
            "medicine": rec["medicine"],
            "fertilizer": rec["fertilizer"],
            "tips": rec["tips"],
        }

    try:
        # Read image bytes
        image_bytes = await file.read()

        if len(image_bytes) == 0:
            raise HTTPException(status_code=400, detail="Empty image file")

        # Run prediction
        prediction = predict_disease(
            image_source=image_bytes,
            model_path=MODEL_PATH,
            top_k=1,
        )

        disease = prediction["disease"]
        confidence = prediction["confidence"]

        # Get recommendations
        recommendation = get_recommendation(disease)

        return {
            "disease": disease,
            "confidence": confidence,
            "medicine": recommendation["medicine"],
            "fertilizer": recommendation["fertilizer"],
            "tips": recommendation["tips"],
        }

    except FileNotFoundError:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded. Run train.py first. Use ?demo=true for mock response.",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def run_server(host: str = "0.0.0.0", port: int = 8000):
    """Run the API server."""
    import uvicorn

    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind")
    args = parser.parse_args()

    run_server(host=args.host, port=args.port)
