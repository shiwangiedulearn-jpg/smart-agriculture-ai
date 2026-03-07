import json
from typing import List, Dict, Optional
from vendor_service import vendor_service

class MapService:
    def __init__(self):
        self.vendor_service = vendor_service
    
    def get_vendor_coordinates(self, disease: str, user_lat: float = None, user_lon: float = None) -> Dict:
        """
        Get vendor coordinates for map display
        
        Args:
            disease: Disease name
            user_lat: User latitude
            user_lon: User longitude
            
        Returns:
            Map-ready coordinate data
        """
        vendors = self.vendor_service.get_vendor_coordinates(disease, user_lat, user_lon)
        
        # Prepare data for map display
        map_data = {
            'user_location': {
                'lat': user_lat,
                'lon': user_lon,
                'marker': '📍'
            } if user_lat and user_lon else None,
            'vendors': [],
            'bounds': self._calculate_bounds(vendors, user_lat, user_lon),
            'center': self._calculate_center(vendors, user_lat, user_lon)
        }
        
        for vendor in vendors:
            vendor_map_data = {
                'id': vendor.get('id'),
                'name': vendor.get('name'),
                'location': vendor.get('location'),
                'coordinates': {
                    'lat': vendor.get('latitude'),
                    'lon': vendor.get('longitude')
                },
                'contact': vendor.get('contact'),
                'rating': vendor.get('rating'),
                'available_medicines': vendor.get('available_medicines', []),
                'distance_km': vendor.get('distance_km'),
                'marker': '🏪',
                'info_window': self._generate_info_window(vendor)
            }
            map_data['vendors'].append(vendor_map_data)
        
        return map_data
    
    def _calculate_bounds(self, vendors: List[Dict], user_lat: float = None, user_lon: float = None) -> Dict:
        """Calculate map bounds to show all vendors"""
        if not vendors:
            return {
                'northeast': {'lat': 30.0, 'lon': 80.0},
                'southwest': {'lat': 10.0, 'lon': 70.0}
            }
        
        lats = [v.get('latitude') for v in vendors if v.get('latitude')]
        lons = [v.get('longitude') for v in vendors if v.get('longitude')]
        
        # Add user location to bounds if provided
        if user_lat and user_lon:
            lats.append(user_lat)
            lons.append(user_lon)
        
        if not lats or not lons:
            return {
                'northeast': {'lat': 30.0, 'lon': 80.0},
                'southwest': {'lat': 10.0, 'lon': 70.0}
            }
        
        # Add padding to bounds
        lat_padding = 2.0
        lon_padding = 2.0
        
        bounds = {
            'northeast': {
                'lat': max(lats) + lat_padding,
                'lon': max(lons) + lon_padding
            },
            'southwest': {
                'lat': min(lats) - lat_padding,
                'lon': min(lons) - lon_padding
            }
        }
        
        return bounds
    
    def _calculate_center(self, vendors: List[Dict], user_lat: float = None, user_lon: float = None) -> Dict:
        """Calculate map center point"""
        if user_lat and user_lon:
            return {'lat': user_lat, 'lon': user_lon}
        
        if not vendors:
            return {'lat': 20.0, 'lon': 77.0}  # Center of India
        
        lats = [v.get('latitude') for v in vendors if v.get('latitude')]
        lons = [v.get('longitude') for v in vendors if v.get('longitude')]
        
        if not lats or not lons:
            return {'lat': 20.0, 'lon': 77.0}
        
        center = {
            'lat': sum(lats) / len(lats),
            'lon': sum(lons) / len(lons)
        }
        
        return center
    
    def _generate_info_window(self, vendor: Dict) -> str:
        """Generate HTML content for map info window"""
        medicines = ', '.join(vendor.get('available_medicines', []))
        distance = vendor.get('distance_km')
        
        info_html = f"""
        <div style="font-family: Arial, sans-serif; padding: 10px; max-width: 200px;">
            <h4 style="margin: 0 0 8px 0; color: #4CAF50;">{vendor.get('name')}</h4>
            <p style="margin: 4px 0; font-size: 14px;"><strong>📍</strong> {vendor.get('location')}</p>
            <p style="margin: 4px 0; font-size: 14px;"><strong>📞</strong> {vendor.get('contact')}</p>
            <p style="margin: 4px 0; font-size: 14px;"><strong>⭐</strong> {vendor.get('rating', 0)}/5.0</p>
            {f'<p style="margin: 4px 0; font-size: 14px;"><strong>📏</strong> {distance} km away</p>' if distance else ''}
            <p style="margin: 4px 0; font-size: 14px;"><strong>💊</strong> {medicines}</p>
        </div>
        """
        
        return info_html
    
    def get_directions_url(self, user_lat: float, user_lon: float, vendor_lat: float, vendor_lon: float) -> str:
        """
        Generate Google Maps directions URL
        
        Args:
            user_lat, user_lon: User coordinates
            vendor_lat, vendor_lon: Vendor coordinates
            
        Returns:
            Google Maps directions URL
        """
        return f"https://www.google.com/maps/dir/{user_lat},{user_lon}/{vendor_lat},{vendor_lon}"
    
    def get_static_map_url(self, disease: str, user_lat: float = None, user_lon: float = None, width: int = 600, height: int = 400) -> str:
        """
        Generate static map URL (for embedding)
        
        Args:
            disease: Disease name
            user_lat, user_lon: User coordinates
            width, height: Map dimensions
            
        Returns:
            Static map URL
        """
        vendors = self.vendor_service.get_vendor_coordinates(disease, user_lat, user_lon)
        
        # Build markers
        markers = []
        
        # Add user marker
        if user_lat and user_lon:
            markers.append(f"color:blue|label:U|{user_lat},{user_lon}")
        
        # Add vendor markers
        for i, vendor in enumerate(vendors[:5]):  # Limit to 5 vendors
            lat = vendor.get('latitude')
            lon = vendor.get('longitude')
            if lat and lon:
                markers.append(f"color:red|label:{i+1}|{lat},{lon}")
        
        if not markers:
            return ""
        
        markers_str = "|".join(markers)
        
        # Create static map URL (using OpenStreetMap as alternative to Google)
        center = self._calculate_center(vendors, user_lat, user_lon)
        
        static_map_url = f"https://maps.googleapis.com/maps/api/staticmap?center={center['lat']},{center['lon']}&zoom=8&size={width}x{height}&maptype=roadmap&markers={markers_str}&key=YOUR_API_KEY"
        
        return static_map_url
    
    def get_all_vendor_locations(self) -> List[Dict]:
        """
        Get all vendor locations for general map display
        
        Returns:
            List of all vendor coordinates
        """
        all_vendors = self.vendor_service.get_all_vendors()
        
        locations = []
        for vendor in all_vendors:
            location_data = {
                'id': vendor.get('id'),
                'name': vendor.get('name'),
                'location': vendor.get('location'),
                'coordinates': {
                    'lat': vendor.get('latitude'),
                    'lon': vendor.get('longitude')
                },
                'contact': vendor.get('contact'),
                'rating': vendor.get('rating'),
                'medicines': vendor.get('medicines', []),
                'marker': '🏪'
            }
            locations.append(location_data)
        
        return locations
    
    def search_nearby_vendors(self, lat: float, lon: float, radius_km: float = 50) -> List[Dict]:
        """
        Search for vendors within a specific radius
        
        Args:
            lat, lon: Center coordinates
            radius_km: Search radius in kilometers
            
        Returns:
            List of nearby vendors
        """
        all_vendors = self.vendor_service.get_all_vendors()
        nearby_vendors = []
        
        for vendor in all_vendors:
            vendor_lat = vendor.get('latitude')
            vendor_lon = vendor.get('longitude')
            
            if vendor_lat is None or vendor_lon is None:
                continue
            
            # Calculate distance (using vendor service method)
            distance = self.vendor_service._calculate_distance(lat, lon, vendor_lat, vendor_lon)
            
            if distance <= radius_km:
                vendor_data = vendor.copy()
                vendor_data['distance_km'] = round(distance, 2)
                nearby_vendors.append(vendor_data)
        
        # Sort by distance
        nearby_vendors.sort(key=lambda v: v.get('distance_km', float('inf')))
        
        return nearby_vendors

# Singleton instance
map_service = MapService()
