#!/usr/bin/env python3
"""
Test script for the enhanced location service.
Tests geocoding, map link generation, and location validation.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.location_service import LocationService
from services.maps_service import MapsService
import json

def test_location_service():
    """Test the LocationService functionality."""
    print("🧪 Testing LocationService...")
    
    # Initialize services
    location_service = LocationService()
    maps_service = MapsService()
    
    # Test addresses in Ho Chi Minh City
    test_addresses = [
        "123 Nguyen Hue, District 1, Ho Chi Minh City",
        "456 Le Loi, District 1, Ho Chi Minh City", 
        "789 Dong Khoi, District 1, Ho Chi Minh City",
        "Landmark 81, Vinhomes Central Park, Binh Thanh",
        "Saigon Centre, Le Loi, District 1",
        "Bitexco Financial Tower, District 1"
    ]
    
    print("\n📍 Testing geocoding and map link generation:")
    print("=" * 60)
    
    for address in test_addresses:
        print(f"\n🔍 Testing address: {address}")
        
        # Test location info
        location_info = location_service.get_location_info(address)
        print(f"   ✅ Location info: {json.dumps(location_info, indent=2)}")
        
        # Test map link generation
        map_link = maps_service.generate_map_link(address)
        print(f"   🗺️  Map link: {map_link}")
        
        # Test zone extraction
        zone = location_service.get_location_zone(address)
        print(f"   🏘️  Zone: {zone}")
    
    print("\n🚗 Testing travel time and distance calculations:")
    print("=" * 60)
    
    # Test travel calculations between locations
    origins = [
        "123 Nguyen Hue, District 1, Ho Chi Minh City",
        "Landmark 81, Vinhomes Central Park, Binh Thanh"
    ]
    
    destinations = [
        "456 Le Loi, District 1, Ho Chi Minh City",
        "Saigon Centre, Le Loi, District 1"
    ]
    
    for origin in origins:
        for destination in destinations:
            if origin != destination:
                print(f"\n🚶‍♀️ {origin} → {destination}")
                
                travel_time = maps_service.calculate_travel_time(origin, destination)
                distance = maps_service.calculate_distance(origin, destination)
                
                print(f"   ⏱️  Travel time: {travel_time // 60 if travel_time else 'Unknown'} minutes")
                print(f"   📏 Distance: {distance:.1f} km" if distance else "   📏 Distance: Unknown")
    
    print("\n🎯 Testing event phase enhancement:")
    print("=" * 60)
    
    # Test event phase enhancement
    test_phases = [
        {
            'activity': 'Hotpot Dinner',
            'location': '123 Nguyen Hue, District 1, Ho Chi Minh City',
            'cost': 250000,
            'isIndoor': True,
            'isOutdoor': False,
            'isVegetarianFriendly': True,
            'isAlcoholFriendly': False
        },
        {
            'activity': 'Karaoke Session',
            'location': '456 Le Loi, District 1, Ho Chi Minh City',
            'cost': 150000,
            'isIndoor': True,
            'isOutdoor': False,
            'isVegetarianFriendly': False,
            'isAlcoholFriendly': True
        }
    ]
    
    enhanced_phases = []
    for phase in test_phases:
        enhanced = location_service.enhance_event_phase(phase)
        enhanced_phases.append(enhanced)
        print(f"\n🎉 Enhanced phase: {json.dumps(enhanced, indent=2)}")
    
    print("\n✅ Testing location validation:")
    print("=" * 60)
    
    # Test location validation
    validation = location_service.validate_event_locations(enhanced_phases)
    print(f"Validation result: {json.dumps(validation, indent=2)}")
    
    print("\n📊 Testing travel summary:")
    print("=" * 60)
    
    # Test travel summary
    travel_summary = location_service.get_travel_summary(enhanced_phases)
    print(f"Travel summary: {json.dumps(travel_summary, indent=2)}")
    
    print("\n🔍 Testing nearby places search:")
    print("=" * 60)
    
    # Test nearby places search
    test_location = "123 Nguyen Hue, District 1, Ho Chi Minh City"
    activity_types = ['restaurant', 'cafe', 'karaoke']
    
    for activity_type in activity_types:
        places = location_service.suggest_nearby_places(test_location, activity_type)
        print(f"\n🏪 Nearby {activity_type} places:")
        for place in places[:3]:  # Show first 3 results
            print(f"   • {place['name']} - {place['address']}")
    
    print("\n🎯 Testing central location calculation:")
    print("=" * 60)
    
    # Test central location calculation
    team_locations = [
        "123 Nguyen Hue, District 1, Ho Chi Minh City",
        "456 Le Loi, District 1, Ho Chi Minh City",
        "Landmark 81, Vinhomes Central Park, Binh Thanh"
    ]
    
    central_location = location_service.find_central_location(team_locations)
    print(f"Central location: {json.dumps(central_location, indent=2)}")
    
    print("\n✅ All tests completed!")

def test_maps_service_directly():
    """Test the MapsService directly."""
    print("\n🧪 Testing MapsService directly...")
    
    maps_service = MapsService()
    
    # Test geocoding
    test_address = "123 Nguyen Hue, District 1, Ho Chi Minh City"
    print(f"\n🔍 Testing geocoding for: {test_address}")
    
    geocode_result = maps_service.geocode_address(test_address)
    print(f"Geocode result: {json.dumps(geocode_result, indent=2)}")
    
    # Test map link generation
    map_link = maps_service.generate_map_link(test_address)
    print(f"Map link: {map_link}")

if __name__ == "__main__":
    print("🚀 Starting Location Service Tests")
    print("=" * 60)
    
    try:
        test_location_service()
        test_maps_service_directly()
        print("\n🎉 All tests passed successfully!")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc() 