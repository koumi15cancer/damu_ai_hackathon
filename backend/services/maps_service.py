import os
import googlemaps
from config import GOOGLE_MAPS_API_KEY

class MapsService:
    def __init__(self):
        self.use_dummy = not GOOGLE_MAPS_API_KEY or GOOGLE_MAPS_API_KEY == 'your_google_maps_api_key_here'
        if not self.use_dummy:
            self.gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)
        else:
            self.gmaps = None

    def geocode_address(self, address):
        if self.use_dummy:
            # Return a dummy location
            return {
                'address': address,
                'location': {'lat': 37.7749, 'lng': -122.4194},
                'formatted_address': f"Dummy Address for {address}"
            }
        # Real API call
        geocode_result = self.gmaps.geocode(address)
        if not geocode_result:
            return None
        result = geocode_result[0]
        return {
            'address': address,
            'location': result['geometry']['location'],
            'formatted_address': result.get('formatted_address', address)
        }

    def find_central_location(self, locations):
        if self.use_dummy:
            # Return a dummy central location
            return {
                'location': {'lat': 37.7749, 'lng': -122.4194},
                'formatted_address': 'Dummy Central Location, San Francisco, CA'
            }
        # Real implementation: average lat/lng
        if not locations:
            return None
        lat = sum(loc['location']['lat'] for loc in locations) / len(locations)
        lng = sum(loc['location']['lng'] for loc in locations) / len(locations)
        return {
            'location': {'lat': lat, 'lng': lng},
            'formatted_address': 'Central Location (calculated)'
        }

    def calculate_travel_time(self, origin, destination, mode='driving'):
        """Calculate travel time between two locations."""
        try:
            result = self.gmaps.distance_matrix(
                origin,
                destination,
                mode=mode
            )
            if result['status'] == 'OK':
                duration = result['rows'][0]['elements'][0]['duration']
                return duration['value']  # Duration in seconds
            return None
        except Exception as e:
            print(f"Distance matrix error: {str(e)}")
            return None

    def find_nearby_places(self, location, keyword):
        if self.use_dummy:
            # Return dummy places
            return [
                {'name': f'Dummy Place 1 for {keyword}', 'address': '123 Dummy St'},
                {'name': f'Dummy Place 2 for {keyword}', 'address': '456 Dummy Ave'},
                {'name': f'Dummy Place 3 for {keyword}', 'address': '789 Dummy Blvd'}
            ]
        # Real API call
        places_result = self.gmaps.places_nearby(
            location=location,
            keyword=keyword,
            radius=5000
        )
        return [
            {
                'name': place['name'],
                'address': place.get('vicinity', '')
            }
            for place in places_result.get('results', [])
        ] 