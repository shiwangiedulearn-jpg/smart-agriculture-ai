"""
YOLOv8 Classification Model Training for Crop Disease Detection.
Trains on PlantVillage-style dataset (folder per class).
"""

import os
import shutil
from pathlib import Path
from typing import Tuple

from ultralytics import YOLO


# Default paths
DATASET_ROOT = Path(__file__).parent / "dataset"
MODEL_SAVE_DIR = Path(__file__).parent / "model"
TRAIN_DATA_DIR = DATASET_ROOT / "train"
VAL_DATA_DIR = DATASET_ROOT / "val"


def prepare_dataset_structure(
    source_dir: Path,
    train_ratio: float = 0.8,
) -> Tuple[Path, Path]:
    """
    Prepare train/val split from PlantVillage-style dataset.
    Expects: source_dir/Class_Name/image.jpg

    Args:
        source_dir: Root directory with class folders
        train_ratio: Fraction of images for training (default 0.8)

    Returns:
        Tuple of (train_path, val_path)
    """
    import random

    train_dir = DATASET_ROOT / "train"
    val_dir = DATASET_ROOT / "val"

    # Create directories
    train_dir.mkdir(parents=True, exist_ok=True)
    val_dir.mkdir(parents=True, exist_ok=True)

    # Get all class folders
    class_folders = [d for d in source_dir.iterdir() if d.is_dir()]

    for class_folder in class_folders:
        class_name = class_folder.name
        images = list(class_folder.glob("*.jpg")) + list(class_folder.glob("*.jpeg")) + list(class_folder.glob("*.png"))

        if not images:
            continue

        random.shuffle(images)
        split_idx = int(len(images) * train_ratio)
        train_images = images[:split_idx]
        val_images = images[split_idx:]

        # Copy to train/val
        for img in train_images:
            dest = train_dir / class_name / img.name
            dest.parent.mkdir(parents=True, exist_ok=True)
            if not dest.exists() or dest.stat().st_size != img.stat().st_size:
                shutil.copy2(img, dest)

        for img in val_images:
            dest = val_dir / class_name / img.name
            dest.parent.mkdir(parents=True, exist_ok=True)
            if not dest.exists() or dest.stat().st_size != img.stat().st_size:
                shutil.copy2(img, dest)

    return train_dir, val_dir


def prepare_dataset_from_nested_splits(
    source_dir: Path,
    train_folder: str = "Train",
    val_folder: str = "Validation",
) -> Tuple[Path, Path]:
    """
    Prepare train/val when dataset has split folders with inner duplicate name.
    Expects: source_dir/Train/Train/Class1/, source_dir/Validation/Validation/Class1/
    """
    train_dir = DATASET_ROOT / "train"
    val_dir = DATASET_ROOT / "val"
    train_dir.mkdir(parents=True, exist_ok=True)
    val_dir.mkdir(parents=True, exist_ok=True)

    def get_class_root(base: Path, split_name: str) -> Path:
        inner = base / split_name / split_name
        if inner.exists() and any(inner.iterdir()):
            return inner
        if (base / split_name).exists():
            return base / split_name
        return None

    train_src = get_class_root(source_dir, train_folder)
    val_src = get_class_root(source_dir, val_folder)

    if not train_src or not train_src.is_dir():
        return None, None

    for class_folder in train_src.iterdir():
        if not class_folder.is_dir():
            continue
        class_name = class_folder.name
        dest_class = train_dir / class_name
        dest_class.mkdir(parents=True, exist_ok=True)
        for img in list(class_folder.glob("*.jpg")) + list(class_folder.glob("*.jpeg")) + list(class_folder.glob("*.png")):
            shutil.copy2(img, dest_class / img.name)

    if val_src and val_src.is_dir():
        for class_folder in val_src.iterdir():
            if not class_folder.is_dir():
                continue
            class_name = class_folder.name
            dest_class = val_dir / class_name
            dest_class.mkdir(parents=True, exist_ok=True)
            for img in list(class_folder.glob("*.jpg")) + list(class_folder.glob("*.jpeg")) + list(class_folder.glob("*.png")):
                shutil.copy2(img, dest_class / img.name)

    return train_dir, val_dir


def train_model(
    data_path: Path = None,
    epochs: int = 50,
    batch_size: int = 16,
    model_size: str = "n",
    project: str = None,
    exist_ok: bool = True,
) -> Path:
    """
    Train YOLOv8 classification model on crop disease dataset.

    Args:
        data_path: Path to dataset (train/val folders with class subfolders)
        epochs: Number of training epochs
        batch_size: Batch size for training
        model_size: YOLOv8 size - n, s, m, l, x (n=nano, x=extra large)
        project: Project save directory
        exist_ok: Overwrite existing project

    Returns:
        Path to best trained model
    """
    # YOLOv8 classification expects path to folder containing train/ and val/
    data_path = data_path or DATASET_ROOT
    project = project or str(MODEL_SAVE_DIR)

    # If user passed dataset/train, use parent so YOLO finds train/ and val/
    if data_path.name == "train" and (data_path.parent / "val").is_dir():
        data_path = data_path.parent

    # Validate dataset exists (must have train/ and val/ with class subdirs)
    train_dir = data_path / "train"
    if not train_dir.exists() or not any(train_dir.iterdir()):
        raise FileNotFoundError(
            f"Dataset not found at {data_path}. "
            "Need dataset/train/ and dataset/val/ with class folders inside."
        )

    # Load YOLOv8 classification model
    model = YOLO(f"yolov8{model_size}-cls.pt")

    # Train
    results = model.train(
        data=str(data_path),
        epochs=epochs,
        batch=batch_size,
        project=project,
        name="crop_disease",
        exist_ok=exist_ok,
        imgsz=224,
        pretrained=True,
        optimizer="Adam",
        verbose=True,
    )

    # Best model is saved automatically
    best_model = Path(project) / "crop_disease" / "weights" / "best.pt"
    if best_model.exists():
        # Copy to model/ for easy access
        final_dest = MODEL_SAVE_DIR / "best.pt"
        MODEL_SAVE_DIR.mkdir(parents=True, exist_ok=True)
        shutil.copy2(best_model, final_dest)
        return final_dest

    return Path(project) / "crop_disease" / "weights" / "best.pt"


def main():
    """Main entry point for training."""
    import argparse

    parser = argparse.ArgumentParser(description="Train YOLOv8 for crop disease detection")
    parser.add_argument(
        "--data",
        type=str,
        default=str(DATASET_ROOT),
        help="Path to dataset root (folder containing train/ and val/)",
    )
    parser.add_argument("--epochs", type=int, default=50, help="Training epochs")
    parser.add_argument("--batch", type=int, default=16, help="Batch size")
    parser.add_argument(
        "--model-size",
        type=str,
        default="n",
        choices=["n", "s", "m", "l", "x"],
        help="YOLOv8 model size (n=nano to x=extra large)",
    )
    parser.add_argument(
        "--prepare",
        type=str,
        default=None,
        help="Prepare dataset from PlantVillage folder (creates train/val split)",
    )
    args = parser.parse_args()

    data_path = Path(args.data)

    # Optionally prepare dataset from raw PlantVillage structure
    if args.prepare:
        print(f"Preparing dataset from {args.prepare}...")
        train_path, val_path = prepare_dataset_structure(Path(args.prepare))
        print(f"Train: {train_path}, Val: {val_path}")
        data_path = DATASET_ROOT  # use root so YOLO finds train/ and val/

    print(f"Training on {data_path} (train + val)...")
    model_path = train_model(
        data_path=data_path,
        epochs=args.epochs,
        batch_size=args.batch,
        model_size=args.model_size,
    )
    print(f"Training complete. Best model: {model_path}")


if __name__ == "__main__":
    main()
