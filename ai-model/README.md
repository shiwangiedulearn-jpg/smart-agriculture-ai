# Crop Disease Detection System

YOLOv8-based crop leaf disease detection with recommendation system. Hackathon-ready.

## Project Structure

```
ai-model/
├── dataset/          # PlantVillage dataset (train/val with class folders)
├── model/            # Trained model weights (best.pt)
├── train.py          # Train YOLOv8 classification model
├── predict.py        # Predict disease from image
├── recommend.py      # Disease → medicine, fertilizer, tips
├── api.py            # FastAPI REST API
├── download_dataset.py
├── requirements.txt
└── README.md
```

## Quick Start

### 1. Install Dependencies

```bash
cd ai-model
pip install -r requirements.txt
```

### 2. Prepare Dataset

**Option A: Kaggle PlantVillage**
```bash
pip install kaggle
kaggle datasets download -d abdallahalidev/plantvillage-dataset
# Unzip and run:
python train.py --prepare path/to/PlantVillage
```

**Option B: Create sample structure**
```bash
python download_dataset.py --create-sample
# Add images to dataset/train/Class_Name/ and dataset/val/Class_Name/
```

**Expected structure:**
```
dataset/
  train/
    Tomato___Early_blight/
      img1.jpg
    Tomato___healthy/
      img2.jpg
  val/
    Tomato___Early_blight/
    Tomato___healthy/
```

### 3. Train Model

```bash
python train.py --epochs 50 --batch 16
# Or with custom data:
python train.py --data dataset/train --epochs 50
```

### 4. Run API

```bash
python api.py
# Or: uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

### 5. Test Prediction

**CLI:**
```bash
python predict.py path/to/leaf_image.jpg
```

**API:**
```bash
curl -X POST "http://localhost:8000/predict" -F "file=@leaf.jpg"
```

**Response:**
```json
{
  "disease": "Tomato___Early_blight",
  "confidence": 0.92,
  "medicine": "Mancozeb, Chlorothalonil",
  "fertilizer": "NPK (balanced), Potassium-rich fertilizer",
  "tips": "Avoid overwatering, ensure proper spacing, remove infected leaves, rotate crops annually"
}
```

## Model accuracy

**After training**, accuracy is logged and saved automatically:

- **During training**: Each epoch prints loss; at the end YOLO shows validation metrics.
- **Training outputs**: In `model/crop_disease/` you get:
  - `results.csv` – loss and metrics per epoch
  - `confusion_matrix.png` – validation confusion matrix
  - `results.png` – loss/accuracy curves
- **Run validation again** (any time after training):

```bash
python validate.py
```

This runs the model on `dataset/val` and prints **Top-1** and **Top-5 accuracy**.

## Making predictions

**1. Command line** (single image):

```bash
python predict.py path/to/leaf_image.jpg
```

Example output:
```
Disease: Rust
Confidence: 94.50%
```

**2. API** (browser or any HTTP client):

1. Start the server: `python api.py`
2. Open http://localhost:8000/docs
3. Use **POST /predict** → click "Try it out" → upload an image → Execute

**3. API with curl:**

```bash
curl -X POST "http://localhost:8000/predict" -F "file=@your_leaf.jpg"
```

Response includes `disease`, `confidence`, `medicine`, `fertilizer`, `tips`.

**Note:** If you haven’t trained yet, use **?demo=true** in the API to get a sample response.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API info |
| GET | `/health` | Health check |
| POST | `/predict` | Upload image, get disease + recommendations |

## Training Options

```bash
python train.py --help
  --data PATH       Dataset path (default: dataset/train)
  --epochs N        Epochs (default: 50)
  --batch N         Batch size (default: 16)
  --model-size n|s|m|l|x   Model size (n=nano, x=extra large)
  --prepare PATH    Prepare train/val from PlantVillage folder
```

## Recommendations

The `recommend.py` module maps 40+ diseases to:
- **Medicine**: Fungicides, bactericides
- **Fertilizer**: NPK, specific nutrients
- **Tips**: Prevention and cultural practices

Supports: Tomato, Potato, Pepper, Corn, Grape, Apple, and more.

## Hackathon Tips

1. **Quick demo without training**: Use a pre-trained ImageNet model or mock API
2. **Small dataset**: 10-20 images per class can work with heavy augmentation
3. **Export to ONNX**: `yolo export model=model/best.pt format=onnx` for deployment
4. **Mobile**: Use `yolov8n-cls` (nano) for fast inference

## License

MIT
