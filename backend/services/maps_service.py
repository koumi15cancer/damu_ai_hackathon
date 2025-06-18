import googlemaps
from config import GOOGLE_MAPS_API_KEY

class MapsService:
    def __init__(self):
        self.gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)

    def geocode_address(self, address):
        """Convert address to coordinates."""
        try:
            result = self.gmaps.geocode(address)
            if result:
                location = result[0]['geometry']['location']
                return {
                    'lat': location['lat'],
                    'lng': location['lng'],
                    'formatted_address': result[0]['formatted_address']
                }
            return None
        except Exception as e:
            print(f"Geocoding error: {str(e)}")
            return None

    def find_central_location(self, locations):
        """Find a central location between multiple points."""
        if not locations:
            return None

        # Calculate average coordinates
        total_lat = sum(loc['lat'] for loc in locations)
        total_lng = sum(loc['lng'] for loc in locations)
        count = len(locations)

        central_point = {
            'lat': total_lat / count,
            'lng': total_lng / count
        }

        # Find the nearest address to the central point
        try:
            result = self.gmaps.reverse_geocode((central_point['lat'], central_point['lng']))
            if result:
                return {
                    'lat': central_point['lat'],
                    'lng': central_point['lng'],
                    'formatted_address': result[0]['formatted_address']
                }
        except Exception as e:
            print(f"Reverse geocoding error: {str(e)}")

        return central_point

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

    def find_nearby_places(self, location, radius=5000, type=None):
        """Find places near a location."""
        try:
            result = self.gmaps.places_nearby(
                location=(location['lat'], location['lng']),
                radius=radius,
                type=type
            )
            return result.get('results', [])
        except Exception as e:
            print(f"Places nearby error: {str(e)}")
            return [] 