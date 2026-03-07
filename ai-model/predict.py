"""
Crop Disease Prediction using trained YOLOv8 classification model.
Takes image input and returns disease name with confidence.
"""

from pathlib import Path
from typing import Union

from PIL import Image
from ultralytics import YOLO

# Default model path
MODEL_PATH = Path(__file__).parent / "model" / "best.pt"


def load_model(model_path: Union[str, Path] = None) -> YOLO:
    """
    Load trained YOLOv8 classification model.

    Args:
        model_path: Path to trained model weights (.pt file)

    Returns:
        Loaded YOLO model

    Raises:
        FileNotFoundError: If model file doesn't exist
    """
    model_path = Path(model_path or MODEL_PATH)
    if not model_path.exists():
        # Try alternative locations
        alt_paths = [
            Path(__file__).parent / "model" / "crop_disease" / "weights" / "best.pt",
            Path(__file__).parent / "runs" / "classify" / "crop_disease" / "weights" / "best.pt",
        ]
        for alt in alt_paths:
            if alt.exists():
                model_path = alt
                break
        else:
            raise FileNotFoundError(
                f"Model not found at {model_path}. "
                "Run train.py first to train the model."
            )
    return YOLO(str(model_path))


def predict_disease(
    image_source: Union[str, Path, bytes, Image.Image],
    model: YOLO = None,
    model_path: Union[str, Path] = None,
    top_k: int = 1,
) -> dict:
    """
    Predict crop disease from image.

    Args:
        image_source: Image path, bytes, or PIL Image
        model: Pre-loaded YOLO model (optional, loads if not provided)
        model_path: Path to model (used if model not provided)
        top_k: Number of top predictions to return (default 1)

    Returns:
        Dictionary with keys: disease, confidence, all_predictions
    """
    # Load model if not provided
    if model is None:
        model = load_model(model_path)

    # Handle different input types
    if isinstance(image_source, bytes):
        # Save bytes to temp file for YOLO
        import tempfile
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as f:
            f.write(image_source)
            temp_path = f.name
        try:
            results = model.predict(temp_path, verbose=False)
        finally:
            Path(temp_path).unlink(missing_ok=True)
    elif isinstance(image_source, Image.Image):
        # Save PIL Image to temp file
        import tempfile
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as f:
            image_source.save(f.name, format="JPEG")
            temp_path = f.name
        try:
            results = model.predict(temp_path, verbose=False)
        finally:
            Path(temp_path).unlink(missing_ok=True)
    else:
        image_path = Path(image_source)
        if not image_path.exists():
            raise FileNotFoundError(f"Image not found: {image_path}")
        results = model.predict(str(image_path), verbose=False)

    # Extract predictions from YOLOv8 classification result
    result = results[0]
    if not hasattr(result, "probs") or result.probs is None:
        return {
            "disease": "unknown",
            "confidence": 0.0,
            "all_predictions": [],
        }

    probs = result.probs
    names = result.names or {}

    # probs.top1 = top class index, probs.top5 = top 5 indices
    top5_indices = probs.top5 if hasattr(probs, "top5") else [probs.top1]
    top_indices = list(top5_indices)[:top_k]

    # Handle tensor/array - convert to list if needed
    prob_data = probs.data
    if hasattr(prob_data, "cpu"):
        prob_data = prob_data.cpu().numpy()

    all_predictions = []
    for cls_id in top_indices:
        cls_id = int(cls_id)
        conf = float(prob_data[cls_id])
        name = names.get(cls_id, str(cls_id))
        all_predictions.append({"disease": name, "confidence": round(conf, 4)})

    # Primary prediction
    disease = all_predictions[0]["disease"] if all_predictions else "unknown"
    confidence = all_predictions[0]["confidence"] if all_predictions else 0.0

    return {
        "disease": disease,
        "confidence": round(confidence, 4),
        "all_predictions": all_predictions,
    }


def predict_from_file(image_path: Union[str, Path]) -> dict:
    """
    Convenience function to predict from image file path.

    Args:
        image_path: Path to image file

    Returns:
        Prediction dictionary
    """
    return predict_disease(str(image_path))


def main():
    """CLI entry point for prediction."""
    import argparse

    parser = argparse.ArgumentParser(description="Predict crop disease from image")
    parser.add_argument("image", type=str, help="Path to image file")
    parser.add_argument("--model", type=str, default=None, help="Path to model weights")
    parser.add_argument("--top", type=int, default=1, help="Number of top predictions")
    args = parser.parse_args()

    result = predict_disease(args.image, model_path=args.model, top_k=args.top)
    print(f"Disease: {result['disease']}")
    print(f"Confidence: {result['confidence']:.2%}")
    if result["all_predictions"]:
        print("All predictions:", result["all_predictions"])


if __name__ == "__main__":
    main()
