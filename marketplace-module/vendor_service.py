import json
import math
from typing import List, Dict, Optional
from config import VENDOR_DATA_FILE, DISEASE_MEDICINE_MAP

class VendorService:
    def __init__(self):
        self.vendors = self._load_vendors()
    
    def _load_vendors(self) -> List[Dict]:
        """Load vendor data from JSON file"""
        try:
            with open(VENDOR_DATA_FILE, 'r') as f:
                data = json.load(f)
                return data['vendors']
        except FileNotFoundError:
            print(f"Vendor data file not found: {VENDOR_DATA_FILE}")
            return []
        except json.JSONDecodeError:
            print("Error decoding vendor data file")
            return []
    
    def get_vendors_by_medicine(self, disease: str) -> List[Dict]:
        """
        Get vendors that sell medicine for the specific disease
        
        Args:
            disease: Disease name (e.g., 'Tomato___Early_blight')
            
        Returns:
            List of vendors with required medicine
        """
        # Get required medicines for the disease
        required_medicines = DISEASE_MEDICINE_MAP.get(disease, [])
        
        if not required_medicines:
            return []
        
        # Find vendors that sell any of the required medicines
        matching_vendors = []
        for vendor in self.vendors:
            vendor_medicines = vendor.get('medicines', [])
            # Check if vendor sells any of the required medicines
            if any(med in vendor_medicines for med in required_medicines):
                matching_vendors.append({
                    **vendor,
                    'available_medicines': [med for med in required_medicines if med in vendor_medicines]
                })
        
        return matching_vendors
    
    def get_nearest_vendor(self, disease: str, user_lat: float = None, user_lon: float = None) -> Optional[Dict]:
        """
        Get the nearest vendor for the disease medicine
        
        Args:
            disease: Disease name
            user_lat: User latitude (optional)
            user_lon: User longitude (optional)
            
        Returns:
            Nearest vendor information or None
        """
        vendors = self.get_vendors_by_medicine(disease)
        
        if not vendors:
            return None
        
        # If no user location provided, return highest rated vendor
        if user_lat is None or user_lon is None:
            return max(vendors, key=lambda v: v.get('rating', 0))
        
        # Calculate distances and find nearest
        nearest_vendor = None
        min_distance = float('inf')
        
        for vendor in vendors:
            vendor_lat = vendor.get('latitude')
            vendor_lon = vendor.get('longitude')
            
            if vendor_lat is None or vendor_lon is None:
                continue
            
            # Calculate distance using Haversine formula
            distance = self._calculate_distance(user_lat, user_lon, vendor_lat, vendor_lon)
            
            if distance < min_distance:
                min_distance = distance
                nearest_vendor = vendor
        
        if nearest_vendor:
            nearest_vendor['distance_km'] = round(min_distance, 2)
        
        return nearest_vendor
    
    def _calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate distance between two points using Haversine formula
        
        Args:
            lat1, lon1: First point coordinates
            lat2, lon2: Second point coordinates
            
        Returns:
            Distance in kilometers
        """
        # Earth radius in kilometers
        R = 6371.0
        
        # Convert degrees to radians
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)
        
        # Differences
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad
        
        # Haversine formula
        a = (math.sin(dlat / 2)**2 + 
             math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        distance = R * c
        return distance
    
    def get_all_vendors(self) -> List[Dict]:
        """Get all vendors"""
        return self.vendors
    
    def get_vendor_by_id(self, vendor_id: str) -> Optional[Dict]:
        """Get vendor by ID"""
        for vendor in self.vendors:
            if vendor.get('id') == vendor_id:
                return vendor
        return None
    
    def search_vendors_by_location(self, location: str) -> List[Dict]:
        """Search vendors by location name"""
        location_lower = location.lower()
        matching_vendors = []
        
        for vendor in self.vendors:
            vendor_location = vendor.get('location', '').lower()
            if location_lower in vendor_location:
                matching_vendors.append(vendor)
        
        return matching_vendors
    
    def get_vendor_coordinates(self, disease: str, user_lat: float = None, user_lon: float = None) -> List[Dict]:
        """
        Get vendor coordinates for map display
        
        Args:
            disease: Disease name
            user_lat: User latitude (optional)
            user_lon: User longitude (optional)
            
        Returns:
            List of vendor coordinates with information
        """
        vendors = self.get_vendors_by_medicine(disease)
        
        coordinates = []
        for vendor in vendors:
            coord_data = {
                'id': vendor.get('id'),
                'name': vendor.get('name'),
                'latitude': vendor.get('latitude'),
                'longitude': vendor.get('longitude'),
                'location': vendor.get('location'),
                'contact': vendor.get('contact'),
                'rating': vendor.get('rating'),
                'available_medicines': vendor.get('available_medicines', [])
            }
            
            # Add distance if user location is provided
            if user_lat is not None and user_lon is not None:
                vendor_lat = vendor.get('latitude')
                vendor_lon = vendor.get('longitude')
                if vendor_lat is not None and vendor_lon is not None:
                    distance = self._calculate_distance(user_lat, user_lon, vendor_lat, vendor_lon)
                    coord_data['distance_km'] = round(distance, 2)
            
            coordinates.append(coord_data)
        
        # Sort by distance if available, otherwise by rating
        if user_lat is not None and user_lon is not None:
            coordinates.sort(key=lambda x: x.get('distance_km', float('inf')))
        else:
            coordinates.sort(key=lambda x: x.get('rating', 0), reverse=True)
        
        return coordinates

# Singleton instance
vendor_service = VendorService()
