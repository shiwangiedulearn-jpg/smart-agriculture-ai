from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import base64
from integration import smart_agriculture

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

@app.route('/')
def home():
    """Health check endpoint"""
    return jsonify({
        'message': 'Smart Agriculture AI Marketplace Module',
        'version': '1.0.0',
        'status': 'running',
        'endpoints': [
            'POST /predict-and-recommend',
            'GET /vendors/<disease>',
            'GET /weather',
            'GET /map/<disease>',
            'GET /health',
            'GET /'
        ]
    })

@app.route('/health')
def health_check():
    """Detailed health check"""
    return jsonify(smart_agriculture.health_check())

@app.route('/predict-and-recommend', methods=['POST'])
def predict_and_recommend():
    """
    Main prediction and recommendation endpoint
    
    Request body:
    {
        "image": "base64_encoded_image" (optional),
        "location": "Bengaluru,IN" (optional),
        "latitude": 12.9716 (optional),
        "longitude": 77.5946 (optional)
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        # Handle image input
        image_data = None
        if 'image' in data and data['image']:
            try:
                # Decode base64 image
                image_data = base64.b64decode(data['image'])
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': f'Invalid image data: {str(e)}'
                }), 400
        
        # Handle file upload
        if 'file' in request.files:
            file = request.files['file']
            if file.filename:
                image_data = file.read()
        
        # Get location information
        location = data.get('location')
        user_lat = data.get('latitude')
        user_lon = data.get('longitude')
        
        # Get prediction and recommendations
        result = smart_agriculture.predict_and_recommend(
            image_data=image_data,
            user_location=location,
            user_lat=user_lat,
            user_lon=user_lon
        )
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

@app.route('/vendors/<disease>')
def get_vendors_by_disease(disease):
    """Get vendors that sell medicine for specific disease"""
    try:
        result = smart_agriculture.get_vendors_by_medicine(disease)
        return jsonify(result)
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error getting vendors: {str(e)}'
        }), 500

@app.route('/weather')
def get_weather():
    """Get weather information"""
    try:
        location = request.args.get('location')
        lat = request.args.get('lat')
        lon = request.args.get('lon')
        
        # Convert lat/lon to float if provided
        user_lat = float(lat) if lat else None
        user_lon = float(lon) if lon else None
        
        result = smart_agriculture.get_weather_by_location(location, user_lat, user_lon)
        return jsonify(result)
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error getting weather: {str(e)}'
        }), 500

@app.route('/map/<disease>')
def get_vendor_map(disease):
    """Get vendor coordinates for map display"""
    try:
        lat = request.args.get('lat')
        lon = request.args.get('lon')
        
        # Convert lat/lon to float if provided
        user_lat = float(lat) if lat else None
        user_lon = float(lon) if lon else None
        
        result = smart_agriculture.get_vendor_map_data(disease, user_lat, user_lon)
        return jsonify(result)
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error getting map data: {str(e)}'
        }), 500

@app.route('/demo')
def demo_endpoint():
    """Demo endpoint for hackathon testing"""
    demo_data = {
        'success': True,
        'disease': 'Tomato___Early_blight',
        'confidence': 0.92,
        'medicine': 'Mancozeb, Chlorothalonil',
        'fertilizer': 'NPK (10-10-10) with extra potassium, reduce nitrogen during infection',
        'tips': 'Remove infected leaves, ensure proper spacing, avoid overhead watering, use resistant varieties',
        'vendor': {
            'id': 'v001',
            'name': 'GreenLife Agro Store',
            'location': 'Bengaluru, Karnataka',
            'contact': '+91-80-23456789',
            'rating': 4.5,
            'available_medicines': ['Mancozeb', 'Chlorothalonil'],
            'distance_km': 2.5,
            'coordinates': {'lat': 12.9716, 'lon': 77.5946}
        },
        'weather': {
            'location': 'Bengaluru',
            'temperature': 28.5,
            'humidity': 65,
            'description': 'Partly cloudy',
            'rain': {'amount_mm': 0, 'status': 'No rain'},
            'farming_recommendations': {
                'recommendations': [
                    'Temperature is optimal for most crops',
                    'Humidity levels are good for crop growth',
                    'No rain - ensure proper irrigation schedule'
                ],
                'overall_condition': 'Favorable',
                'irrigation_needed': True
            }
        },
        'map_data': {
            'center': {'lat': 12.9716, 'lon': 77.5946},
            'vendors': [
                {
                    'id': 'v001',
                    'name': 'GreenLife Agro Store',
                    'coordinates': {'lat': 12.9716, 'lon': 77.5946},
                    'distance_km': 2.5,
                    'marker': '🏪'
                }
            ]
        }
    }
    
    return jsonify(demo_data)

@app.route('/upload-demo', methods=['POST'])
def upload_demo():
    """Demo upload endpoint for testing"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Save file temporarily
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        
        # Process with demo data
        result = smart_agriculture.predict_and_recommend(
            image_path=filename,
            user_location=request.form.get('location'),
            user_lat=float(request.form.get('lat')) if request.form.get('lat') else None,
            user_lon=float(request.form.get('lon')) if request.form.get('lon') else None
        )
        
        # Clean up
        if os.path.exists(filename):
            os.remove(filename)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Upload error: {str(e)}'
        }), 500

@app.errorhandler(413)
def too_large(e):
    """Handle file too large error"""
    return jsonify({
        'success': False,
        'error': 'File too large. Maximum size is 16MB'
    }), 413

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors"""
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    
    print(f"🌱 Smart Agriculture AI Marketplace Module")
    print(f"🚀 Starting server on http://localhost:{port}")
    print(f"📊 Available endpoints:")
    print(f"   POST /predict-and-recommend - Main prediction API")
    print(f"   GET  /vendors/<disease> - Get vendors by disease")
    print(f"   GET  /weather - Get weather information")
    print(f"   GET  /map/<disease> - Get vendor map data")
    print(f"   GET  /demo - Demo endpoint")
    print(f"   GET  /health - Health check")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
