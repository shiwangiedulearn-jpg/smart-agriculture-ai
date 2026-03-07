"""
Check model accuracy on the validation set.
Run after training to see top-1 and top-5 accuracy.
"""

from pathlib import Path

from ultralytics import YOLO

DATASET_ROOT = Path(__file__).parent / "dataset"
MODEL_PATH = Path(__file__).parent / "model" / "best.pt"


def get_model_path():
    """Find trained model weights."""
    candidates = [
        MODEL_PATH,
        Path(__file__).parent / "model" / "crop_disease" / "weights" / "best.pt",
    ]
    for p in candidates:
        if p.exists():
            return p
    return None


def main():
    model_path = get_model_path()
    if not model_path:
        print("No trained model found. Run: python train.py")
        return

    print(f"Loading model: {model_path}")
    model = YOLO(str(model_path))

    if not (DATASET_ROOT / "val").exists():
        print("No validation set at dataset/val. Run dataset preparation first.")
        return

    print("Running validation on dataset/val ...")
    metrics = model.val(data=str(DATASET_ROOT))

    print("\n" + "=" * 50)
    print("MODEL ACCURACY")
    print("=" * 50)
    # Handle different metric attribute names (top1/top5 or accuracy_top1/accuracy_top5)
    top1 = getattr(metrics, "top1", None) or getattr(metrics, "accuracy_top1", None)
    top5 = getattr(metrics, "top5", None) or getattr(metrics, "accuracy_top5", None)
    if top1 is not None:
        print(f"  Top-1 accuracy:  {float(top1):.2%}")
    if top5 is not None:
        print(f"  Top-5 accuracy:  {float(top5):.2%}")
    if top1 is None and top5 is None:
        print("  (Metrics printed above by Ultralytics)")
    print("=" * 50)


if __name__ == "__main__":
    main()
