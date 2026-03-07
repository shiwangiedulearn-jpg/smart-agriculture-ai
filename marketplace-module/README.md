# Smart Agriculture AI - Marketplace Module

🌱 **Complete integration system for crop disease detection, vendor recommendations, and weather services**

## 🚀 Features

### 🤖 AI Disease Detection
- Integration with AI model server
- Disease prediction with confidence scores
- Treatment recommendations

### 🏪 Vendor System
- **10+ vendors** across major Indian cities
- **Medicine availability** tracking
- **Distance calculation** and nearest vendor finding
- **Contact information** and ratings

### 🌤️ Weather Services
- **Real-time weather** data from OpenWeatherMap API
- **Farming recommendations** based on conditions
- **Temperature, humidity, rain** information
- **Mock data** fallback for offline demos

### 🗺️ Map Integration
- **Vendor coordinates** for map display
- **Distance calculations** using Haversine formula
- **Google Maps** integration for directions
- **Static map** generation

## 📁 Project Structure

```
marketplace-module/
├── app.py                    # Flask API server
├── integration.py            # Main integration logic
├── vendor_service.py         # Vendor management system
├── weather_service.py        # Weather API integration
├── map_service.py           # Map and location services
├── config.py                # Configuration and mappings
├── vendor_data.json         # Vendor database
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variables template
└── README.md               # This file
```

## 🛠️ Setup Instructions

### 1. Install Dependencies
```bash
cd marketplace-module
pip install -r requirements.txt
```

### 2. Environment Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your configuration
# Add your OpenWeatherMap API key
```

### 3. Start the Server
```bash
python app.py
```

Server will start on `http://localhost:5000`

## 📡 API Endpoints

### 🎯 Main Prediction API
```
POST /predict-and-recommend
Content-Type: application/json

{
    "image": "base64_encoded_image",
    "location": "Bengaluru,IN",
    "latitude": 12.9716,
    "longitude": 77.5946
}
```

### 🏪 Vendor APIs
```
GET /vendors/<disease>
GET /map/<disease>?lat=12.9716&lon=77.5946
```

### 🌤️ Weather APIs
```
GET /weather?location=Bengaluru,IN
GET /weather?lat=12.9716&lon=77.5946
```

### 🔧 Utility APIs
```
GET /health          # Service health check
GET /demo            # Demo data for testing
POST /upload-demo    # File upload demo
```

## 📊 Response Format

```json
{
    "success": true,
    "disease": "Tomato___Early_blight",
    "confidence": 0.92,
    "medicine": "Mancozeb, Chlorothalonil",
    "fertilizer": "NPK (10-10-10) with extra potassium",
    "tips": "Remove infected leaves, ensure proper spacing...",
    "vendor": {
        "id": "v001",
        "name": "GreenLife Agro Store",
        "location": "Bengaluru, Karnataka",
        "contact": "+91-80-23456789",
        "rating": 4.5,
        "distance_km": 2.5,
        "coordinates": {"lat": 12.9716, "lon": 77.5946}
    },
    "weather": {
        "location": "Bengaluru",
        "temperature": 28.5,
        "humidity": 65,
        "description": "Partly cloudy",
        "rain": {"amount_mm": 0, "status": "No rain"},
        "farming_recommendations": {
            "recommendations": ["Temperature is optimal for most crops"],
            "overall_condition": "Favorable"
        }
    },
    "map_data": {
        "center": {"lat": 12.9716, "lon": 77.5946},
        "vendors": [...]
    },
    "timestamp": "2024-03-07T10:30:00"
}
```

## 🏪 Vendor Database

### Available Vendors (10+ cities):
- **Bengaluru** - GreenLife Agro Store
- **Pune** - Farmers Choice Solutions  
- **Hyderabad** - AgriCare Essentials
- **Chennai** - Rural Farm Supplies
- **Kochi** - Organic Farm Hub
- **Jaipur** - Crop Protection Center
- **Lucknow** - Smart Agro Solutions
- **Bhopal** - Green Valley Supplies
- **Ahmedabad** - Farm Tech Solutions
- **Indore** - Nature Care Agro

### Available Medicines:
- Mancozeb, Chlorothalonil, Copper Oxychloride
- Carbendazim, Thiram, Zineb, Captan
- Neem Oil, Bordeaux Mixture, Sulfur
- And more...

## 🌦️ Weather Integration

### Features:
- **Real-time data** from OpenWeatherMap
- **Farming recommendations** based on conditions
- **Automatic fallback** to mock data
- **Location-based** queries

### Weather Factors:
- Temperature & Humidity
- Rain probability
- Wind speed & visibility
- Pressure & conditions

## 🗺️ Map Services

### Features:
- **Distance calculations** using Haversine formula
- **Nearest vendor** finding
- **Google Maps** integration
- **Static map** generation
- **Coordinate management**

### Map Data:
- Vendor coordinates
- Distance calculations
- Direction URLs
- Info window content

## 🧪 Testing & Demo

### Quick Demo:
```bash
curl http://localhost:5000/demo
```

### Health Check:
```bash
curl http://localhost:5000/health
```

### File Upload Demo:
```bash
curl -X POST -F "file=@crop_image.jpg" \
     -F "location=Bengaluru,IN" \
     -F "lat=12.9716" -F "lon=77.5946" \
     http://localhost:5000/upload-demo
```

## 🔗 Integration with Backend

### Connected Services:
1. **AI Model Server** (`http://localhost:8001`)
2. **Backend Server** (`http://localhost:8000`)
3. **Frontend App** (`http://localhost:3000`)

### Data Flow:
```
Frontend → Marketplace Module → Backend Server → AI Model
                ↓
            Vendor + Weather Services
```

## 🎯 Hackathon Ready Features

### ✅ Production Features:
- Complete API integration
- Error handling & fallbacks
- Mock data for demos
- Health monitoring
- CORS enabled
- File upload support

### 🚀 Demo Features:
- Pre-populated vendor data
- Mock weather data
- Demo endpoints
- Sample responses
- Easy setup

### 📱 Frontend Integration:
- RESTful APIs
- JSON responses
- CORS enabled
- Error handling
- Status codes

## 🔧 Configuration

### Environment Variables:
```bash
BACKEND_URL=http://localhost:8000
AI_MODEL_URL=http://localhost:8001
WEATHER_API_KEY=your_api_key
PORT=5000
DEBUG=false
```

### Disease Mappings:
- Medicine recommendations
- Fertilizer suggestions
- Prevention tips
- Vendor availability

## 🌟 Key Features for Hackathon

1. **Complete Integration** - All services working together
2. **Real Data** - Actual vendor information across India
3. **Location Services** - GPS and distance calculations
4. **Weather Intelligence** - Smart farming recommendations
5. **Map Integration** - Visual vendor locations
6. **Error Handling** - Robust fallback systems
7. **Demo Ready** - Instant demo capabilities
8. **Scalable** - Clean architecture for expansion

## 🏆 Winning Features

- **AI + Marketplace** - Unique combination
- **Location Intelligence** - GPS-based recommendations
- **Weather Integration** - Smart farming insights
- **Vendor Network** - Real agricultural supply chain
- **Complete Solution** - End-to-end platform
- **Hackathon Ready** - Demo in minutes

---

🌱 **Transforming Agriculture with AI and Location Intelligence** 🚀
