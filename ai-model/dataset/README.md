# Dataset folder

## Bring your dataset from another folder

**Option 1: Copy using script (recommended)**

From the `ai-model` folder run:

```powershell
cd d:\smart-agriculture-ai\ai-model
python download_dataset.py --copy-from "C:\path\to\your\dataset"
```

Replace `C:\path\to\your\dataset` with the actual path where your dataset is (e.g. `D:\Downloads\PlantVillage` or `C:\Users\YourName\PlantVillage`).

This copies your folder into `dataset/raw/` and creates `train/` and `val/` splits here.

**Option 2: Copy manually**

1. Copy your entire dataset folder.
2. Paste it inside this folder, e.g. `dataset/PlantVillage/`.
3. Then from `ai-model` run:
   ```powershell
   python train.py --prepare dataset/PlantVillage
   ```
   That creates `dataset/train/` and `dataset/val/` from your folder.

**Option 3: Use dataset in place (no copy)**

If you prefer not to copy, you can train using the path directly:

```powershell
python train.py --prepare "C:\path\to\your\dataset"
```

That creates train/val inside this `dataset/` folder from your existing path.

---

## Expected structure

Your folder should look like this (one folder per class, images inside):

```
YourFolder/
  Tomato___Early_blight/
    img1.jpg
    img2.jpg
  Tomato___healthy/
    img1.jpg
  Potato___Late_blight/
    ...
```

After `--prepare` or `--copy-from`, you get:

```
dataset/
  train/
    Tomato___Early_blight/  ...
    Tomato___healthy/       ...
  val/
    Tomato___Early_blight/  ...
    Tomato___healthy/       ...
```

Then train with: `python train.py`
