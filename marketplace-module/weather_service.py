import requests
import os
from typing import Dict, Optional
from config import WEATHER_API_KEY, WEATHER_BASE_URL, DEFAULT_LOCATION, DEFAULT_LAT, DEFAULT_LON

class WeatherService:
    def __init__(self):
        self.api_key = WEATHER_API_KEY
        self.base_url = WEATHER_BASE_URL
    
    def get_weather(self, location: str = None, lat: float = None, lon: float = None) -> Dict:
        """
        Get weather information for a location
        
        Args:
            location: City name (e.g., 'Bengaluru,IN')
            lat: Latitude
            lon: Longitude
            
        Returns:
            Weather information dictionary
        """
        # Use coordinates if provided, otherwise use location name
        if lat is not None and lon is not None:
            url = f"{self.base_url}?lat={lat}&lon={lon}&appid={self.api_key}&units=metric"
        elif location:
            url = f"{self.base_url}?q={location}&appid={self.api_key}&units=metric"
        else:
            # Use default location
            url = f"{self.base_url}?q={DEFAULT_LOCATION}&appid={self.api_key}&units=metric"
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Extract relevant weather information
            weather_info = {
                'location': data.get('name', 'Unknown'),
                'country': data.get('sys', {}).get('country', ''),
                'temperature': round(data.get('main', {}).get('temp', 0), 1),
                'humidity': data.get('main', {}).get('humidity', 0),
                'pressure': data.get('main', {}).get('pressure', 0),
                'description': data.get('weather', [{}])[0].get('description', '').title(),
                'wind_speed': data.get('wind', {}).get('speed', 0),
                'visibility': data.get('visibility', 0) / 1000,  # Convert to km
                'rain': self._get_rain_info(data),
                'coordinates': {
                    'lat': data.get('coord', {}).get('lat', DEFAULT_LAT),
                    'lon': data.get('coord', {}).get('lon', DEFAULT_LON)
                },
                'success': True
            }
            
            return weather_info
            
        except requests.exceptions.RequestException as e:
            print(f"Weather API error: {e}")
            return self._get_mock_weather(location)
        except (KeyError, ValueError) as e:
            print(f"Weather data parsing error: {e}")
            return self._get_mock_weather(location)
    
    def _get_rain_info(self, data: Dict) -> Dict:
        """Extract rain information from weather data"""
        rain_data = data.get('rain', {})
        if rain_data:
            # Rain in last 3 hours (mm)
            rain_3h = rain_data.get('3h', 0)
            return {
                'amount_mm': rain_3h,
                'status': 'Raining' if rain_3h > 0 else 'No rain'
            }
        
        # Check from weather description
        description = data.get('weather', [{}])[0].get('description', '').lower()
        if any(word in description for word in ['rain', 'drizzle', 'shower']):
            return {
                'amount_mm': 0,
                'status': 'Possible rain'
            }
        
        return {
            'amount_mm': 0,
            'status': 'No rain'
        }
    
    def _get_mock_weather(self, location: str = None) -> Dict:
        """
        Get mock weather data when API is unavailable
        
        Args:
            location: Location name
            
        Returns:
            Mock weather information
        """
        mock_data = {
            'location': location or 'Bengaluru',
            'country': 'IN',
            'temperature': 28.5,
            'humidity': 65,
            'pressure': 1013,
            'description': 'Partly cloudy',
            'wind_speed': 5.2,
            'visibility': 10.0,
            'rain': {
                'amount_mm': 0,
                'status': 'No rain'
            },
            'coordinates': {
                'lat': DEFAULT_LAT,
                'lon': DEFAULT_LON
            },
            'success': False,
            'mock': True
        }
        
        return mock_data
    
    def get_weather_forecast(self, location: str = None, days: int = 5) -> Dict:
        """
        Get weather forecast (mock implementation for hackathon)
        
        Args:
            location: Location name
            days: Number of forecast days
            
        Returns:
            Weather forecast information
        """
        # Mock forecast data for hackathon demo
        forecast = []
        base_temp = 28.5
        
        for i in range(days):
            forecast.append({
                'day': f'Day {i + 1}',
                'temperature_high': base_temp + (i * 2),
                'temperature_low': base_temp - (i * 3),
                'humidity': 60 + (i * 5),
                'description': ['Sunny', 'Partly cloudy', 'Cloudy', 'Light rain', 'Sunny'][i % 5],
                'rain_chance': [10, 20, 40, 70, 15][i % 5]
            })
        
        return {
            'location': location or 'Bengaluru',
            'forecast': forecast,
            'success': True
        }
    
    def get_farming_recommendations(self, weather: Dict) -> Dict:
        """
        Get farming recommendations based on weather
        
        Args:
            weather: Weather information
            
        Returns:
            Farming recommendations
        """
        temp = weather.get('temperature', 25)
        humidity = weather.get('humidity', 50)
        rain_status = weather.get('rain', {}).get('status', 'No rain')
        
        recommendations = []
        
        # Temperature recommendations
        if temp > 35:
            recommendations.append("High temperature detected - ensure proper irrigation and consider shade nets")
        elif temp < 15:
            recommendations.append("Low temperature - delay planting sensitive crops, use protective covers")
        else:
            recommendations.append("Temperature is optimal for most crops")
        
        # Humidity recommendations
        if humidity > 80:
            recommendations.append("High humidity - increased risk of fungal diseases, ensure proper air circulation")
        elif humidity < 30:
            recommendations.append("Low humidity - increase irrigation frequency, consider mulching")
        else:
            recommendations.append("Humidity levels are good for crop growth")
        
        # Rain recommendations
        if 'rain' in rain_status.lower():
            recommendations.append("Rain detected - delay pesticide application, check drainage systems")
        else:
            recommendations.append("No rain - ensure proper irrigation schedule")
        
        # General recommendations based on conditions
        if temp > 25 and humidity > 70:
            recommendations.append("Favorable conditions for disease development - monitor crops closely")
        
        return {
            'recommendations': recommendations,
            'overall_condition': 'Favorable' if 20 <= temp <= 30 and 40 <= humidity <= 70 else 'Challenging',
            'irrigation_needed': rain_status == 'No rain' and temp > 25
        }

# Singleton instance
weather_service = WeatherService()
