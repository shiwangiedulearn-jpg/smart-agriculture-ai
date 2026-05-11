from fastapi import FastAPI, UploadFile, File
from ultralytics import YOLO
from PIL import Image
import yaml
import io
from treatment import treatment

app = FastAPI()

# Load YOLO model
model = YOLO("best.pt")

CONFIDENCE_THRESHOLD = 0.6

# Load class names
with open("data.yaml", "r") as f:
    data = yaml.safe_load(f)

names = data["names"]


@app.get("/")
def home():
    return {"message": "Plant Disease API Running"}


@app.post("/predict")
async def predict(file: UploadFile = File(...)):

    contents = await file.read()

    image = Image.open(io.BytesIO(contents))

    results = model(image)

    for r in results:

        if len(r.boxes) > 0:

            # highest confidence box
            best_box = max(r.boxes, key=lambda x: float(x.conf))

            cls = int(best_box.cls)

            disease = names[cls].replace("___", " ").replace("_", " ")

            conf = float(best_box.conf)

            if conf < CONFIDENCE_THRESHOLD:

                return {
                    "status": "error",
                    "message": "Invalid image or unclear leaf",
                    "confidence": round(conf, 2)
                }

            response = {
                "status": "success",
                "disease": disease,
                "confidence": round(conf, 2)
            }

            # add treatment info
            if disease in treatment:

                response["fertilizer"] = treatment[disease]["fertilizer"]

                response["action"] = treatment[disease]["action"]

            return response

    return {
        "status": "error",
        "message": "No disease detected"
    }