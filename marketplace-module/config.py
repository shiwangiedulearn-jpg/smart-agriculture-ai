import os

# API Configuration
BACKEND_URL = os.getenv('BACKEND_URL', 'http://localhost:8000')
AI_MODEL_URL = os.getenv('AI_MODEL_URL', 'http://localhost:8001')

# Weather API Configuration
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY', 'your_openweather_api_key_here')
WEATHER_BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'

# Vendor Configuration
VENDOR_DATA_FILE = os.path.join(os.path.dirname(__file__), 'vendor_data.json')

# Default Location (for weather when no location provided)
DEFAULT_LOCATION = 'Bengaluru,IN'
DEFAULT_LAT = 12.9716
DEFAULT_LON = 77.5946

# Disease to Medicine Mapping
DISEASE_MEDICINE_MAP = {
    'Tomato___Early_blight': ['Mancozeb', 'Chlorothalonil', 'Copper Oxychloride'],
    'Tomato___Late_blight': ['Metalaxyl', 'Mancozeb', 'Copper Oxychloride'],
    'Tomato___Septoria_leaf_spot': ['Chlorothalonil', 'Mancozeb', 'Carbendazim'],
    'Tomato___Target_Spot': ['Chlorothalonil', 'Thiophanate', 'Iprodione'],
    'Tomato___Bacterial_spot': ['Copper Oxychloride', 'Bordeaux Mixture', 'Copper Soap'],
    'Tomato___Leaf_Mold': ['Sulfur', 'Neem Oil', 'Bordeaux Mixture'],
    'Tomato___Powdery_mildew': ['Sulfur', 'Neem Oil', 'Tebuconazole'],
    'Tomato___Spider_mites': ['Neem Oil', 'Pyrethrum', 'Karate'],
    'Tomato___healthy': [],
    'Potato___Early_blight': ['Mancozeb', 'Chlorothalonil', 'Copper Oxychloride'],
    'Potato___Late_blight': ['Metalaxyl', 'Mancozeb', 'Copper Oxychloride'],
    'Potato___healthy': [],
    'Corn___Common_rust': ['Mancozeb', 'Tebuconazole', 'Carbendazim'],
    'Corn___Northern_Leaf_Blight': ['Chlorothalonil', 'Mancozeb', 'Carbendazim'],
    'Corn___healthy': []
}

# Fertilizer Recommendations
FERTILIZER_RECOMMENDATIONS = {
    'Tomato___Early_blight': 'NPK (10-10-10) with extra potassium, reduce nitrogen during infection',
    'Tomato___Late_blight': 'Balanced NPK (12-12-12) with calcium supplement, avoid excess nitrogen',
    'Tomato___Septoria_leaf_spot': 'NPK (15-15-15) with micronutrients, ensure proper drainage',
    'Tomato___Target_Spot': 'NPK (20-20-20) with iron and zinc supplements',
    'Tomato___Bacterial_spot': 'NPK (8-8-8) with copper supplement, avoid high nitrogen',
    'Tomato___Leaf_Mold': 'NPK (10-10-10) with sulfur, ensure good air circulation',
    'Tomato___Powdery_mildew': 'NPK (5-10-10) with potassium, reduce nitrogen',
    'Tomato___Spider_mites': 'NPK (15-15-15) with micronutrients, increase potassium',
    'Tomato___healthy': 'Balanced NPK (10-10-10) with regular feeding schedule',
    'Potato___Early_blight': 'NPK (6-12-12) with high potassium, avoid excess nitrogen',
    'Potato___Late_blight': 'NPK (5-10-10) with calcium, reduce nitrogen during infection',
    'Potato___healthy': 'NPK (10-10-10) with regular feeding schedule',
    'Corn___Common_rust': 'NPK (20-10-10) with high nitrogen, add zinc',
    'Corn___Northern_Leaf_Blight': 'NPK (15-15-15) with micronutrients',
    'Corn___healthy': 'NPK (16-8-8) with regular feeding schedule'
}

# Prevention Tips
PREVENTION_TIPS = {
    'Tomato___Early_blight': 'Remove infected leaves, ensure proper spacing, avoid overhead watering, use resistant varieties',
    'Tomato___Late_blight': 'Improve air circulation, remove infected plants, use copper fungicides preventively, avoid wet leaves',
    'Tomato___Septoria_leaf_spot': 'Crop rotation, remove plant debris, proper spacing, avoid working with wet plants',
    'Tomato___Target_Spot': 'Maintain proper humidity, regular fungicide application, remove infected leaves',
    'Tomato___Bacterial_spot': 'Use disease-free seeds, copper sprays, avoid overhead irrigation, proper sanitation',
    'Tomato___Leaf_Mold': 'Improve air circulation, reduce humidity, sulfur fungicides, resistant varieties',
    'Tomato___Powdery_mildew': 'Increase air circulation, reduce humidity, neem oil sprays, resistant varieties',
    'Tomato___Spider_mites': 'Regular monitoring, neem oil sprays, introduce beneficial insects, proper irrigation',
    'Tomato___healthy': 'Regular monitoring, proper watering, balanced fertilization, good air circulation',
    'Potato___Early_blight': 'Crop rotation, remove infected plants, proper drainage, resistant varieties',
    'Potato___Late_blight': 'Destroy infected plants, proper drainage, preventive fungicides, avoid wet conditions',
    'Potato___healthy': 'Crop rotation, proper hilling, balanced fertilization, regular inspection',
    'Corn___Common_rust': 'Resistant varieties, proper spacing, fungicide application, crop rotation',
    'Corn___Northern_Leaf_Blight': 'Resistant hybrids, proper drainage, balanced fertilization, timely fungicide',
    'Corn___healthy': 'Proper spacing, balanced fertilization, regular monitoring, crop rotation'
}
