import os
import googlemaps
import logging
from config import GOOGLE_MAPS_API_KEY
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

class MapsService:
    def __init__(self):
        self.use_dummy = not GOOGLE_MAPS_API_KEY or GOOGLE_MAPS_API_KEY == 'your_google_maps_api_key_here'
        if not self.use_dummy:
            try:
                self.gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)
                # Test the API key with a simple geocoding request
                test_result = self.gmaps.geocode("Ho Chi Minh City, Vietnam")
                if test_result:
                    logger.info("✅ Google Maps API initialized successfully")
                else:
                    logger.warning("⚠️ Google Maps API key may not have required permissions")
                    self.use_dummy = True
            except Exception as e:
                logger.error(f"❌ Failed to initialize Google Maps API: {e}")
                self.use_dummy = True
                self.gmaps = None
        else:
            logger.warning("⚠️ Using dummy Google Maps data - set GOOGLE_MAPS_API_KEY for real data")
            self.gmaps = None

    def geocode_address(self, address: str) -> Optional[Dict]:
        """
        Geocode an address to get coordinates and formatted address.
        
        Args:
            address: The address to geocode
            
        Returns:
            Dict with location data or None if geocoding fails
        """
        if self.use_dummy:
            # Return realistic dummy data for Ho Chi Minh City
            return self._get_dummy_location(address)
        
        try:
            # Add "Ho Chi Minh City" to improve geocoding accuracy if not present
            search_address = address
            if "Ho Chi Minh City" not in address and "HCMC" not in address:
                search_address = f"{address}, Ho Chi Minh City, Vietnam"
            
            geocode_result = self.gmaps.geocode(search_address)
            
            if not geocode_result:
                logger.warning(f"⚠️ No geocoding results for: {address}")
                return None
                
            result = geocode_result[0]
            location = result['geometry']['location']
            formatted_address = result.get('formatted_address', address)
            
            logger.info(f"✅ Geocoded '{address}' to {formatted_address} at {location}")
            
            return {
                'address': address,
                'location': location,
                'formatted_address': formatted_address,
                'place_id': result.get('place_id'),
                'types': result.get('types', [])
            }
            
        except Exception as e:
            error_msg = str(e)
            if "REQUEST_DENIED" in error_msg:
                logger.error(f"❌ Google Maps API access denied. Please check API key and enabled services: {error_msg}")
                # Fall back to dummy data
                return self._get_dummy_location(address)
            else:
                logger.error(f"❌ Geocoding error for '{address}': {e}")
                return None

    def generate_map_link(self, location: str) -> str:
        """
        Generate a Google Maps link for a location.
        
        Args:
            location: The location string
            
        Returns:
            Google Maps URL
        """
        try:
            # First try to geocode the address
            geocode_result = self.geocode_address(location)
            
            if geocode_result and geocode_result.get('location'):
                lat, lng = geocode_result['location']['lat'], geocode_result['location']['lng']
                # Use coordinates for more accurate map links
                return f"https://www.google.com/maps?q={lat},{lng}"
            else:
                # Fallback to search query
                encoded_location = location.replace(' ', '+')
                return f"https://www.google.com/maps/search/{encoded_location}"
                
        except Exception as e:
            logger.error(f"❌ Error generating map link for '{location}': {e}")
            # Fallback to search query
            encoded_location = location.replace(' ', '+')
            return f"https://www.google.com/maps/search/{encoded_location}"

    def calculate_travel_time(self, origin: str, destination: str, mode: str = 'driving') -> Optional[int]:
        """
        Calculate travel time between two locations using Routes API.
        
        Args:
            origin: Starting location
            destination: Ending location
            mode: Travel mode (driving, walking, bicycling, transit)
            
        Returns:
            Travel time in seconds or None if calculation fails
        """
        if self.use_dummy:
            # Return realistic dummy travel times for Ho Chi Minh City
            return self._get_dummy_travel_time(origin, destination, mode)
        
        try:
            # Use the newer Routes API instead of deprecated Distance Matrix API
            result = self.gmaps.distance_matrix(
                origins=[origin],
                destinations=[destination],
                mode=mode,
                units='metric',
                avoid='tolls'  # Avoid toll roads for better user experience
            )
            
            if result['status'] == 'OK' and result['rows'][0]['elements'][0]['status'] == 'OK':
                duration = result['rows'][0]['elements'][0]['duration']
                distance = result['rows'][0]['elements'][0]['distance']
                
                logger.info(f"✅ Travel time: {origin} → {destination} = {duration['text']} ({distance['text']})")
                return duration['value']  # Duration in seconds
            else:
                logger.warning(f"⚠️ No travel time data for {origin} → {destination}")
                return None
                
        except Exception as e:
            error_msg = str(e)
            if "REQUEST_DENIED" in error_msg:
                logger.error(f"❌ Google Maps API access denied for travel time. Please enable Routes API: {error_msg}")
                # Fall back to dummy data
                return self._get_dummy_travel_time(origin, destination, mode)
            else:
                logger.error(f"❌ Travel time calculation error: {e}")
                return None

    def calculate_distance(self, origin: str, destination: str, mode: str = 'driving') -> Optional[float]:
        """
        Calculate distance between two locations using Routes API.
        
        Args:
            origin: Starting location
            destination: Ending location
            mode: Travel mode
            
        Returns:
            Distance in kilometers or None if calculation fails
        """
        if self.use_dummy:
            return self._get_dummy_distance(origin, destination)
        
        try:
            result = self.gmaps.distance_matrix(
                origins=[origin],
                destinations=[destination],
                mode=mode,
                units='metric',
                avoid='tolls'
            )
            
            if result['status'] == 'OK' and result['rows'][0]['elements'][0]['status'] == 'OK':
                distance = result['rows'][0]['elements'][0]['distance']
                return distance['value'] / 1000  # Convert meters to kilometers
            else:
                return None
                
        except Exception as e:
            error_msg = str(e)
            if "REQUEST_DENIED" in error_msg:
                logger.error(f"❌ Google Maps API access denied for distance calculation. Please enable Routes API: {error_msg}")
                # Fall back to dummy data
                return self._get_dummy_distance(origin, destination)
            else:
                logger.error(f"❌ Distance calculation error: {e}")
                return None

    def find_nearby_places(self, location: str, keyword: str, radius: int = 5000) -> List[Dict]:
        """
        Find nearby places using Google Places API (New).
        
        Args:
            location: Center location
            keyword: Search keyword
            radius: Search radius in meters
            
        Returns:
            List of nearby places
        """
        if self.use_dummy:
            return self._get_dummy_nearby_places(keyword)
        
        try:
            # First geocode the location to get coordinates
            geocode_result = self.geocode_address(location)
            if not geocode_result:
                return []
            
            lat_lng = geocode_result['location']
            
            # Use Places API (New) for better results
            places_result = self.gmaps.places_nearby(
                location=lat_lng,
                keyword=keyword,
                radius=radius,
                type='establishment'
            )
            
            places = []
            for place in places_result.get('results', []):
                places.append({
                    'name': place['name'],
                    'address': place.get('vicinity', ''),
                    'place_id': place.get('place_id'),
                    'rating': place.get('rating'),
                    'types': place.get('types', [])
                })
            
            logger.info(f"✅ Found {len(places)} nearby places for '{keyword}' near {location}")
            return places
            
        except Exception as e:
            error_msg = str(e)
            if "REQUEST_DENIED" in error_msg:
                logger.error(f"❌ Google Maps API access denied for nearby places. Please enable Places API: {error_msg}")
                # Fall back to dummy data
                return self._get_dummy_nearby_places(keyword)
            else:
                logger.error(f"❌ Nearby places search error: {e}")
                return []

    def find_central_location(self, locations: List[str]) -> Optional[Dict]:
        """
        Find a central location from a list of addresses.
        
        Args:
            locations: List of location addresses
            
        Returns:
            Central location data or None if calculation fails
        """
        if self.use_dummy:
            return self._get_dummy_central_location()
        
        try:
            # Geocode all locations
            geocoded_locations = []
            for location in locations:
                result = self.geocode_address(location)
                if result:
                    geocoded_locations.append(result)
            
            if not geocoded_locations:
                return None
            
            # Calculate average coordinates
            avg_lat = sum(loc['location']['lat'] for loc in geocoded_locations) / len(geocoded_locations)
            avg_lng = sum(loc['location']['lng'] for loc in geocoded_locations) / len(geocoded_locations)
            
            # Reverse geocode to get address
            reverse_result = self.gmaps.reverse_geocode((avg_lat, avg_lng))
            
            formatted_address = "Central Location (calculated)"
            if reverse_result:
                formatted_address = reverse_result[0].get('formatted_address', formatted_address)
            
            return {
                'location': {'lat': avg_lat, 'lng': avg_lng},
                'formatted_address': formatted_address
            }
            
        except Exception as e:
            logger.error(f"❌ Central location calculation error: {e}")
            return None

    def _get_dummy_location(self, address: str) -> Dict:
        """Generate realistic dummy location data for Ho Chi Minh City."""
        # Realistic coordinates for different districts in Ho Chi Minh City
        district_coords = {
            'district 1': (10.7769, 106.7009),
            'district 2': (10.7873, 106.7498),
            'district 3': (10.7826, 106.6881),
            'district 4': (10.7663, 106.7049),
            'district 5': (10.7540, 106.6634),
            'district 6': (10.7465, 106.6352),
            'district 7': (10.7323, 106.7267),
            'district 8': (10.7243, 106.6286),
            'district 9': (10.8428, 106.8281),
            'district 10': (10.7628, 106.6602),
            'district 11': (10.7639, 106.6439),
            'district 12': (10.8633, 106.6544),
            'binh thanh': (10.7979, 106.7110),
            'phu nhuan': (10.7948, 106.6754),
            'tan binh': (10.8011, 106.6526),
            'tan phu': (10.7769, 106.6000),
            'go vap': (10.8384, 106.6659),
            'thu duc': (10.8494, 106.7537),
        }
        
        # Try to match district from address
        address_lower = address.lower()
        for district, coords in district_coords.items():
            if district in address_lower:
                lat, lng = coords
                return {
                    'address': address,
                    'location': {'lat': lat, 'lng': lng},
                    'formatted_address': f"{address}, Ho Chi Minh City, Vietnam",
                    'place_id': 'dummy_place_id',
                    'types': ['establishment']
                }
        
        # Default to District 1 if no match
        return {
            'address': address,
            'location': {'lat': 10.7769, 'lng': 106.7009},
            'formatted_address': f"{address}, District 1, Ho Chi Minh City, Vietnam",
            'place_id': 'dummy_place_id',
            'types': ['establishment']
        }

    def _get_dummy_travel_time(self, origin: str, destination: str, mode: str) -> int:
        """Generate realistic dummy travel times for Ho Chi Minh City."""
        # Base travel times in seconds for different modes
        base_times = {
            'driving': 900,  # 15 minutes
            'walking': 1800,  # 30 minutes
            'bicycling': 1200,  # 20 minutes
            'transit': 1200,  # 20 minutes
        }
        
        # Add some randomness
        import random
        base_time = base_times.get(mode, 900)
        variation = random.uniform(0.7, 1.3)  # ±30% variation
        
        return int(base_time * variation)

    def _get_dummy_distance(self, origin: str, destination: str) -> float:
        """Generate realistic dummy distances for Ho Chi Minh City."""
        import random
        # Typical distances between locations in HCMC (1-5 km)
        return round(random.uniform(1.0, 5.0), 1)

    def _get_dummy_nearby_places(self, keyword: str) -> List[Dict]:
        """Generate realistic dummy nearby places."""
        return [
            {
                'name': f'{keyword.title()} Place 1',
                'address': '123 Nguyen Hue, District 1, Ho Chi Minh City',
                'place_id': 'dummy_place_1',
                'rating': 4.2,
                'types': ['establishment']
            },
            {
                'name': f'{keyword.title()} Place 2',
                'address': '456 Le Loi, District 1, Ho Chi Minh City',
                'place_id': 'dummy_place_2',
                'rating': 4.0,
                'types': ['establishment']
            },
            {
                'name': f'{keyword.title()} Place 3',
                'address': '789 Dong Khoi, District 1, Ho Chi Minh City',
                'place_id': 'dummy_place_3',
                'rating': 4.5,
                'types': ['establishment']
            }
        ]

    def _get_dummy_central_location(self) -> Dict:
        """Generate realistic dummy central location."""
        return {
            'location': {'lat': 10.7769, 'lng': 106.7009},
            'formatted_address': 'Central Location, District 1, Ho Chi Minh City, Vietnam'
        } 