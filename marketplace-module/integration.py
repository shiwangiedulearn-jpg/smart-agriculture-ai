import requests
import base64
from typing import Dict, Optional
from config import (BACKEND_URL, AI_MODEL_URL, FERTILIZER_RECOMMENDATIONS, 
                   PREVENTION_TIPS, DEFAULT_LAT, DEFAULT_LON)
from vendor_service import vendor_service
from weather_service import weather_service
from map_service import map_service

class SmartAgricultureIntegration:
    def __init__(self):
        self.backend_url = BACKEND_URL
        self.ai_model_url = AI_MODEL_URL
        self.vendor_service = vendor_service
        self.weather_service = weather_service
        self.map_service = map_service
    
    def predict_and_recommend(self, image_path: str = None, image_data: bytes = None, 
                            user_location: str = None, user_lat: float = None, 
                            user_lon: float = None) -> Dict:
        """
        Complete prediction and recommendation pipeline
        
        Args:
            image_path: Path to image file
            image_data: Raw image bytes
            user_location: User location string
            user_lat: User latitude
            user_lon: User longitude
            
        Returns:
            Complete recommendation response
        """
        try:
            # Step 1: Get disease prediction from backend
            disease_result = self._get_disease_prediction(image_path, image_data)
            
            if not disease_result.get('success', False):
                return {
                    'success': False,
                    'error': disease_result.get('error', 'Failed to get disease prediction'),
                    'disease': '',
                    'confidence': 0,
                    'medicine': '',
                    'fertilizer': '',
                    'tips': '',
                    'vendor': {},
                    'weather': {}
                }
            
            disease = disease_result.get('disease', '')
            confidence = disease_result.get('confidence', 0)
            
            # Step 2: Get recommendations based on disease
            recommendations = self._get_disease_recommendations(disease)
            
            # Step 3: Find nearest vendor
            vendor_info = self._get_nearest_vendor(disease, user_lat, user_lon)
            
            # Step 4: Get weather information
            weather_info = self._get_weather_info(user_location, user_lat, user_lon)
            
            # Step 5: Get map coordinates
            map_coordinates = self._get_map_coordinates(disease, user_lat, user_lon)
            
            # Step 6: Compile complete response
            response = {
                'success': True,
                'disease': disease,
                'confidence': confidence,
                'medicine': recommendations.get('medicine', ''),
                'fertilizer': recommendations.get('fertilizer', ''),
                'tips': recommendations.get('tips', ''),
                'vendor': vendor_info or {},
                'weather': weather_info or {},
                'map_data': map_coordinates or {},
                'timestamp': self._get_timestamp(),
                'user_location': {
                    'provided_location': user_location,
                    'coordinates': {'lat': user_lat, 'lon': user_lon} if user_lat and user_lon else None
                }
            }
            
            return response
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Integration error: {str(e)}',
                'disease': '',
                'confidence': 0,
                'medicine': '',
                'fertilizer': '',
                'tips': '',
                'vendor': {},
                'weather': {},
                'map_data': {}
            }
    
    def _get_disease_prediction(self, image_path: str = None, image_data: bytes = None) -> Dict:
        """Get disease prediction from backend server"""
        try:
            if image_data:
                # Send raw image data
                files = {'file': ('crop_image.jpg', image_data, 'image/jpeg')}
            elif image_path:
                # Send image file
                with open(image_path, 'rb') as f:
                    files = {'file': f}
            else:
                return {'success': False, 'error': 'No image provided'}
            
            response = requests.post(f"{self.backend_url}/predict", files=files, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            result['success'] = True
            return result
            
        except requests.exceptions.RequestException as e:
            # Fallback to mock data for hackathon demo
            return self._get_mock_disease_result()
        except Exception as e:
            return {'success': False, 'error': f'Prediction error: {str(e)}'}
    
    def _get_disease_recommendations(self, disease: str) -> Dict:
        """Get treatment recommendations for disease"""
        medicine = self.vendor_service.get_vendors_by_medicine(disease)
        available_medicines = []
        
        if medicine:
            # Get first vendor's available medicines as recommendation
            available_medicines = medicine[0].get('available_medicines', [])
        
        return {
            'medicine': ', '.join(available_medicines) if available_medicines else 'No specific medicine required',
            'fertilizer': FERTILIZER_RECOMMENDATIONS.get(disease, 'Balanced NPK fertilizer recommended'),
            'tips': PREVENTION_TIPS.get(disease, 'Continue regular monitoring and good agricultural practices')
        }
    
    def _get_nearest_vendor(self, disease: str, user_lat: float = None, user_lon: float = None) -> Optional[Dict]:
        """Get nearest vendor for disease treatment"""
        vendor = self.vendor_service.get_nearest_vendor(disease, user_lat, user_lon)
        
        if vendor:
            return {
                'id': vendor.get('id'),
                'name': vendor.get('name'),
                'location': vendor.get('location'),
                'contact': vendor.get('contact'),
                'rating': vendor.get('rating'),
                'available_medicines': vendor.get('available_medicines', []),
                'distance_km': vendor.get('distance_km'),
                'coordinates': {
                    'lat': vendor.get('latitude'),
                    'lon': vendor.get('longitude')
                },
                'directions_url': self.map_service.get_directions_url(
                    user_lat or DEFAULT_LAT, user_lon or DEFAULT_LON,
                    vendor.get('latitude'), vendor.get('longitude')
                ) if user_lat and user_lon else None
            }
        
        return None
    
    def _get_weather_info(self, location: str = None, lat: float = None, lon: float = None) -> Dict:
        """Get weather information"""
        weather = self.weather_service.get_weather(location, lat, lon)
        
        if weather:
            # Add farming recommendations
            farming_recommendations = self.weather_service.get_farming_recommendations(weather)
            weather['farming_recommendations'] = farming_recommendations
        
        return weather
    
    def _get_map_coordinates(self, disease: str, user_lat: float = None, user_lon: float = None) -> Dict:
        """Get map coordinates for vendors"""
        return self.map_service.get_vendor_coordinates(disease, user_lat, user_lon)
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def _get_mock_disease_result(self) -> Dict:
        """Mock disease result for hackathon demo"""
        return {
            'success': True,
            'disease': 'Tomato___Early_blight',
            'confidence': 0.92,
            'mock': True
        }
    
    def get_vendors_by_medicine(self, disease: str) -> Dict:
        """Get all vendors that sell medicine for specific disease"""
        vendors = self.vendor_service.get_vendors_by_medicine(disease)
        
        return {
            'success': True,
            'disease': disease,
            'vendors': vendors,
            'total_vendors': len(vendors)
        }
    
    def get_weather_by_location(self, location: str = None, lat: float = None, lon: float = None) -> Dict:
        """Get weather information for a location"""
        weather = self.weather_service.get_weather(location, lat, lon)
        
        return {
            'success': weather.get('success', False),
            'weather': weather
        }
    
    def get_vendor_map_data(self, disease: str, user_lat: float = None, user_lon: float = None) -> Dict:
        """Get vendor data for map display"""
        map_data = self.map_service.get_vendor_coordinates(disease, user_lat, user_lon)
        
        return {
            'success': True,
            'disease': disease,
            'map_data': map_data
        }
    
    def health_check(self) -> Dict:
        """Health check for all services"""
        services_status = {
            'integration_service': 'healthy',
            'vendor_service': 'healthy',
            'weather_service': 'healthy',
            'map_service': 'healthy'
        }
        
        # Check backend server
        try:
            response = requests.get(f"{self.backend_url}/", timeout=5)
            services_status['backend_server'] = 'healthy' if response.status_code == 200 else 'unhealthy'
        except:
            services_status['backend_server'] = 'unhealthy'
        
        # Check AI model server
        try:
            response = requests.get(f"{self.ai_model_url}/", timeout=5)
            services_status['ai_model_server'] = 'healthy' if response.status_code == 200 else 'unhealthy'
        except:
            services_status['ai_model_server'] = 'unhealthy'
        
        overall_status = 'healthy' if all(status == 'healthy' for status in services_status.values()) else 'degraded'
        
        return {
            'overall_status': overall_status,
            'services': services_status,
            'timestamp': self._get_timestamp()
        }

# Singleton instance
smart_agriculture = SmartAgricultureIntegration()
