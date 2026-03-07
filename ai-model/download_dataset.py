"""
Download and prepare PlantVillage dataset for training.
Use --copy-from "path" to bring a dataset from elsewhere on your laptop.
"""

import shutil
from pathlib import Path

DATASET_DIR = Path(__file__).parent / "dataset"


def create_sample_dataset():
    """
    Create a minimal sample dataset structure for testing.
    Uses placeholder structure - user should add real images.
    """
    sample_classes = [
        "Tomato___Early_blight",
        "Tomato___Late_blight",
        "Tomato___healthy",
        "Potato___Early_blight",
        "Potato___Late_blight",
        "Potato___healthy",
    ]
    for split in ["train", "val"]:
        for cls in sample_classes:
            (DATASET_DIR / split / cls).mkdir(parents=True, exist_ok=True)
    print(f"Created sample structure at {DATASET_DIR}")
    print("Add images to dataset/train/Class_Name/ and dataset/val/Class_Name/")


def download_plantvillage_subset():
    """
    Download PlantVillage from alternative source.
    Kaggle requires API key - we provide manual instructions.
    """
    print("PlantVillage Dataset Setup")
    print("=" * 50)
    print("Option 1: Download from Kaggle (recommended)")
    print("  1. Get Kaggle API key from kaggle.com/account")
    print("  2. pip install kaggle")
    print("  3. kaggle datasets download -d abdallahalidev/plantvillage-dataset")
    print("  4. unzip and place in dataset/ folder")
    print()
    print("Option 2: Use sample structure")
    print("  Run: python download_dataset.py --create-sample")
    print()
    create_sample_dataset()


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--create-sample",
        action="store_true",
        help="Create sample dataset folder structure",
    )
    parser.add_argument(
        "--from-folder",
        type=str,
        help="Use existing folder path (creates train/val split in dataset/)",
    )
    parser.add_argument(
        "--copy-from",
        type=str,
        metavar="PATH",
        help="Copy dataset from this path into dataset/raw/ then create train/val",
    )
    args = parser.parse_args()

    if args.create_sample:
        create_sample_dataset()
        return

    # Copy from another location into dataset/raw, then prepare train/val
    if args.copy_from:
        src = Path(args.copy_from).resolve()
        if not src.is_dir():
            print(f"Error: Not a folder or not found: {src}")
            return
        dest = DATASET_DIR / "raw"
        dest.mkdir(parents=True, exist_ok=True)
        print(f"Copying from {src} to {dest} ...")
        if (dest / src.name).exists():
            shutil.rmtree(dest / src.name, ignore_errors=True)
        shutil.copytree(src, dest / src.name)
        print("Copy done. Creating train/val split...")
        from train import prepare_dataset_structure, prepare_dataset_from_nested_splits

        copied_path = dest / src.name
        # Try nested structure first (e.g. Train/Train/Class, Validation/Validation/Class)
        train_path, val_path = prepare_dataset_from_nested_splits(copied_path)
        if train_path is None:
            train_path, val_path = prepare_dataset_structure(copied_path)
        print(f"Done. Train: {train_path}, Val: {val_path}")
        print("Run: python train.py")
        return

    if args.from_folder:
        src = Path(args.from_folder).resolve()
        if not src.is_dir():
            print(f"Folder not found: {src}")
            return
        from train import prepare_dataset_structure

        train_path, val_path = prepare_dataset_structure(src)
        print(f"Prepared: train={train_path}, val={val_path}")
        return

    download_plantvillage_subset()


if __name__ == "__main__":
    main()
