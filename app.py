import streamlit as st
from ultralytics import YOLO
import yaml
from PIL import Image
from treatment import treatment

# Load model
model = YOLO(r"plant_disease_data\runs\detect\train\weights\best.pt")

CONFIDENCE_THRESHOLD = 0.6  

# Load class names
with open("plant_disease_data\data.yaml", "r") as f:
    data = yaml.safe_load(f)

names = data["names"]

st.title("🌿 Plant Disease Detection")

uploaded_file = st.file_uploader("Upload leaf image", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image")

    results = model(image)

    for r in results:
      if len(r.boxes) > 0:
          # pick highest confidence box
          best_box = max(r.boxes, key=lambda x: float(x.conf))

          cls = int(best_box.cls)
          disease = names[cls].replace("___", " ").replace("_", " ")
          conf = float(best_box.conf)

          # Check if confidence is above threshold
          if conf < CONFIDENCE_THRESHOLD:
              st.error(f"❌ Invalid Image - Not a leaf or too unclear (Confidence: {conf:.2f})")
          else:
              st.write(f"🦠 Disease: {disease}")
              st.write(f"📊 Confidence: {conf:.2f}")

        # show treatment
          if disease in treatment:
              st.write(f"🌿 Fertilizer: {treatment[disease]['fertilizer']}")
              st.write(f"🛠 Action: {treatment[disease]['action']}")