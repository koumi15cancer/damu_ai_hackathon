#!/usr/bin/env python3
"""
Simple test to verify rating endpoint
"""

import requests
import json

def test_rating_endpoint():
    """Test the rating endpoint"""
    print("🧪 Testing Rating Endpoint...")
    
    # Test data
    test_rating = {
        "member_name": "Sarah",
        "rating": 4,
        "feedback": "Great event!",
        "categories": {
            "fun": 5,
            "organization": 4,
            "value": 4,
            "overall": 4
        }
    }
    
    try:
        # Get events first
        print("📚 Getting events...")
        response = requests.get("http://localhost:5000/event-history")
        
        if response.status_code != 200:
            print(f"❌ Failed to get events: {response.status_code}")
            return
        
        events = response.json()
        if not events:
            print("❌ No events found")
            return
        
        event_id = events[0]['id']
        print(f"🎯 Testing with event ID: {event_id}")
        
        # Submit rating
        print("📝 Submitting rating...")
        response = requests.post(
            f"http://localhost:5000/event-history/{event_id}/rate",
            json=test_rating
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 201:
            print("✅ Rating submitted successfully!")
        else:
            print("❌ Rating submission failed")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    test_rating_endpoint() 