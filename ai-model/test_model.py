from ultralytics import YOLO
import yaml
import streamlit as st
from treatment import treatment 

# Load model
model = YOLO("plant_disease_data/runs/detect/train/weights/best.pt")

# Load class names
with open("plant_disease_data\data.yaml", "r") as f:
    data = yaml.safe_load(f)

names = data["names"]

# Run prediction
results = model("plant_disease_data/test/images/1c4c2235-2c28-438e-8fa9-505b5d3004a0___JR_FrgE-S-8720_90deg_JPG.rf.89541064a2792730d17de3c9dc6a429b.jpg",conf= 0.4,  show=True, save=True)

for r in results:
    if len(r.boxes) > 0:
        best_box = max(r.boxes, key=lambda x: float(x.conf))
        
        cls = int(best_box.cls)
        disease = names[cls].replace("___", " ").replace("_", " ")
        conf = float(best_box.conf)

        st.write(f"🦠 Disease: {disease}")
        st.write(f"📊 Confidence: {conf:.2f}")

        if disease in treatment:
            st.write(f"🌿 Fertilizer: {treatment[disease]['fertilizer']}")
            st.write(f"🛠 Action: {treatment[disease]['action']}")
