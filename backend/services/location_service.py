import logging
from typing import Dict, List, Optional, Tuple
from .maps_service import MapsService

logger = logging.getLogger(__name__)

class LocationService:
    """
    Service for handling location-related operations for EventPhase.
    Provides geocoding, map link generation, travel time calculations,
    and location validation for team bonding events.
    """
    
    def __init__(self):
        self.maps_service = MapsService()
    
    def get_location_info(self, address: str) -> Dict:
        """
        Get comprehensive location information for an address.
        
        Args:
            address: The address to process
            
        Returns:
            Dict containing location data, formatted address, and map link
        """
        try:
            # Geocode the address
            geocode_result = self.maps_service.geocode_address(address)
            
            if geocode_result:
                # Generate map link
                map_link = self.maps_service.generate_map_link(address)
                
                return {
                    'original_address': address,
                    'formatted_address': geocode_result.get('formatted_address', address),
                    'coordinates': geocode_result.get('location'),
                    'map_link': map_link,
                    'place_id': geocode_result.get('place_id'),
                    'types': geocode_result.get('types', []),
                    'is_valid': True
                }
            else:
                # Fallback for invalid addresses
                map_link = self.maps_service.generate_map_link(address)
                return {
                    'original_address': address,
                    'formatted_address': address,
                    'coordinates': None,
                    'map_link': map_link,
                    'place_id': None,
                    'types': [],
                    'is_valid': False
                }
                
        except Exception as e:
            logger.error(f"❌ Error getting location info for '{address}': {e}")
            return {
                'original_address': address,
                'formatted_address': address,
                'coordinates': None,
                'map_link': f"https://www.google.com/maps/search/{address.replace(' ', '+')}",
                'place_id': None,
                'types': [],
                'is_valid': False
            }
    
    def validate_event_locations(self, phases: List[Dict]) -> Dict:
        """
        Validate locations for an event plan against constraints.
        
        Args:
            phases: List of event phases with location data
            
        Returns:
            Dict containing validation results and recommendations
        """
        validation_result = {
            'is_valid': True,
            'issues': [],
            'recommendations': [],
            'travel_times': [],
            'distances': []
        }
        
        if len(phases) < 2:
            return validation_result
        
        try:
            for i in range(len(phases) - 1):
                current_phase = phases[i]
                next_phase = phases[i + 1]
                
                current_location = current_phase.get('location', '')
                next_location = next_phase.get('location', '')
                
                if not current_location or not next_location:
                    continue
                
                # Calculate travel time and distance
                travel_time = self.maps_service.calculate_travel_time(
                    current_location, next_location, 'driving'
                )
                distance = self.maps_service.calculate_distance(
                    current_location, next_location, 'driving'
                )
                
                travel_info = {
                    'from_phase': i + 1,
                    'to_phase': i + 2,
                    'from_location': current_location,
                    'to_location': next_location,
                    'travel_time_minutes': travel_time // 60 if travel_time else None,
                    'distance_km': distance
                }
                
                validation_result['travel_times'].append(travel_info)
                
                # Check constraints
                if travel_time and travel_time > 900:  # 15 minutes = 900 seconds
                    validation_result['is_valid'] = False
                    validation_result['issues'].append(
                        f"Travel time from Phase {i+1} to Phase {i+2} exceeds 15 minutes "
                        f"({travel_time // 60} minutes)"
                    )
                
                if distance and distance > 2.0:  # 2 km constraint
                    validation_result['is_valid'] = False
                    validation_result['issues'].append(
                        f"Distance from Phase {i+1} to Phase {i+2} exceeds 2 km "
                        f"({distance:.1f} km)"
                    )
                
                # Add recommendations
                if travel_time and travel_time > 600:  # 10 minutes
                    validation_result['recommendations'].append(
                        f"Consider alternative locations for Phase {i+2} to reduce travel time"
                    )
        
        except Exception as e:
            logger.error(f"❌ Error validating event locations: {e}")
            validation_result['is_valid'] = False
            validation_result['issues'].append(f"Error during validation: {str(e)}")
        
        return validation_result
    
    def find_central_location(self, team_member_locations: List[str]) -> Optional[Dict]:
        """
        Find a central location for team members.
        
        Args:
            team_member_locations: List of team member location addresses
            
        Returns:
            Central location data or None if calculation fails
        """
        try:
            return self.maps_service.find_central_location(team_member_locations)
        except Exception as e:
            logger.error(f"❌ Error finding central location: {e}")
            return None
    
    def suggest_nearby_places(self, location: str, activity_type: str, radius: int = 2000) -> List[Dict]:
        """
        Suggest nearby places for a specific activity type.
        
        Args:
            location: Center location
            activity_type: Type of activity (restaurant, cafe, karaoke, etc.)
            radius: Search radius in meters
            
        Returns:
            List of suggested places
        """
        try:
            # Map activity types to search keywords
            keyword_mapping = {
                'restaurant': 'restaurant',
                'cafe': 'cafe',
                'karaoke': 'karaoke',
                'bar': 'bar',
                'bowling': 'bowling',
                'escape_room': 'escape room',
                'movie': 'cinema',
                'park': 'park',
                'shopping': 'shopping mall',
                'hotpot': 'hotpot restaurant',
                'bbq': 'bbq restaurant',
                'yoga': 'yoga studio',
                'gym': 'gym',
                'spa': 'spa',
                'massage': 'massage'
            }
            
            keyword = keyword_mapping.get(activity_type.lower(), activity_type)
            places = self.maps_service.find_nearby_places(location, keyword, radius)
            
            # Add activity type to each place
            for place in places:
                place['activity_type'] = activity_type
            
            return places
            
        except Exception as e:
            logger.error(f"❌ Error suggesting nearby places: {e}")
            return []
    
    def get_location_zone(self, address: str) -> str:
        """
        Extract the district/zone from an address.
        
        Args:
            address: The address to analyze
            
        Returns:
            District/zone name
        """
        address_lower = address.lower()
        
        # Ho Chi Minh City districts
        districts = [
            'district 1', 'district 2', 'district 3', 'district 4', 'district 5',
            'district 6', 'district 7', 'district 8', 'district 9', 'district 10',
            'district 11', 'district 12', 'binh thanh', 'phu nhuan', 'tan binh',
            'tan phu', 'go vap', 'thu duc'
        ]
        
        for district in districts:
            if district in address_lower:
                return district.replace('district ', 'D').title()
        
        return 'Unknown Zone'
    
    def format_location_for_display(self, location_info: Dict) -> Dict:
        """
        Format location information for frontend display.
        
        Args:
            location_info: Raw location information
            
        Returns:
            Formatted location data for display
        """
        try:
            formatted = {
                'display_address': location_info.get('formatted_address', location_info.get('original_address')),
                'map_link': location_info.get('map_link'),
                'zone': self.get_location_zone(location_info.get('formatted_address', '')),
                'is_valid': location_info.get('is_valid', False)
            }
            
            # Add coordinates if available
            coordinates = location_info.get('coordinates')
            if coordinates:
                formatted['latitude'] = coordinates.get('lat')
                formatted['longitude'] = coordinates.get('lng')
            
            return formatted
            
        except Exception as e:
            logger.error(f"❌ Error formatting location for display: {e}")
            return {
                'display_address': location_info.get('original_address', 'Unknown Location'),
                'map_link': location_info.get('map_link', ''),
                'zone': 'Unknown Zone',
                'is_valid': False
            }
    
    def enhance_event_phase(self, phase: Dict) -> Dict:
        """
        Enhance an event phase with location information.
        
        Args:
            phase: Event phase data
            
        Returns:
            Enhanced phase with location data
        """
        try:
            location = phase.get('location', phase.get('address', ''))
            if not location:
                return phase
            
            # Get comprehensive location info
            location_info = self.get_location_info(location)
            
            # Format for display
            display_info = self.format_location_for_display(location_info)
            
            # Enhance the phase
            enhanced_phase = phase.copy()
            enhanced_phase.update({
                'location': display_info['display_address'],
                'map_link': display_info['map_link'],
                'zone': display_info['zone'],
                'location_valid': display_info['is_valid'],
                'coordinates': location_info.get('coordinates')
            })
            
            return enhanced_phase
            
        except Exception as e:
            logger.error(f"❌ Error enhancing event phase: {e}")
            return phase
    
    def get_travel_summary(self, phases: List[Dict]) -> Dict:
        """
        Get a summary of travel information for an event.
        
        Args:
            phases: List of event phases
            
        Returns:
            Travel summary with total time, distance, and recommendations
        """
        try:
            total_travel_time = 0
            total_distance = 0
            travel_segments = []
            
            for i in range(len(phases) - 1):
                current_location = phases[i].get('location', '')
                next_location = phases[i + 1].get('location', '')
                
                if current_location and next_location:
                    travel_time = self.maps_service.calculate_travel_time(
                        current_location, next_location
                    )
                    distance = self.maps_service.calculate_distance(
                        current_location, next_location
                    )
                    
                    if travel_time:
                        total_travel_time += travel_time
                    if distance:
                        total_distance += distance
                    
                    travel_segments.append({
                        'from': current_location,
                        'to': next_location,
                        'time_minutes': travel_time // 60 if travel_time else None,
                        'distance_km': distance
                    })
            
            return {
                'total_travel_time_minutes': total_travel_time // 60,
                'total_distance_km': round(total_distance, 1),
                'travel_segments': travel_segments,
                'recommendations': self._generate_travel_recommendations(total_travel_time, total_distance)
            }
            
        except Exception as e:
            logger.error(f"❌ Error getting travel summary: {e}")
            return {
                'total_travel_time_minutes': 0,
                'total_distance_km': 0,
                'travel_segments': [],
                'recommendations': []
            }
    
    def _generate_travel_recommendations(self, total_time: int, total_distance: float) -> List[str]:
        """Generate travel recommendations based on time and distance."""
        recommendations = []
        
        if total_time > 1800:  # 30 minutes
            recommendations.append("Consider reducing the number of phases or choosing closer locations")
        
        if total_distance > 5.0:  # 5 km
            recommendations.append("Total travel distance is quite high - consider more centralized locations")
        
        if total_time > 900:  # 15 minutes
            recommendations.append("Total travel time exceeds recommended limits for team bonding events")
        
        return recommendations 