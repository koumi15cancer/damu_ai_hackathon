#!/usr/bin/env python3
"""
Test to verify AI ratings are preserved when member ratings are added
"""

import requests
import json

def test_ai_member_ratings():
    """Test that AI ratings are preserved when member ratings are added"""
    print("🧪 Testing AI Rating Preservation...")
    print("=" * 50)
    
    try:
        # Get existing events
        print("📚 Getting events...")
        response = requests.get("http://localhost:5000/event-history")
        
        if response.status_code != 200:
            print(f"❌ Failed to get events: {response.status_code}")
            return
        
        events = response.json()
        if not events:
            print("❌ No events found")
            return
        
        # Find an event with AI rating but no member ratings
        target_event = None
        for event in events:
            if event.get('rating') and not event.get('member_ratings'):
                target_event = event
                break
        
        if not target_event:
            print("❌ No suitable event found (need one with AI rating but no member ratings)")
            return
        
        event_id = target_event['id']
        ai_rating = target_event['rating']
        
        print(f"🎯 Testing with event ID: {event_id}")
        print(f"   AI Rating: {ai_rating}/5")
        print(f"   Theme: {target_event['theme']}")
        
        # Submit a member rating
        test_rating = {
            "member_name": "TestUser",
            "rating": 4,
            "feedback": "Testing AI rating preservation",
            "categories": {
                "fun": 4,
                "organization": 5,
                "value": 4,
                "overall": 4
            }
        }
        
        print(f"\n📝 Submitting member rating...")
        response = requests.post(
            f"http://localhost:5000/event-history/{event_id}/rate",
            json=test_rating
        )
        
        if response.status_code == 201:
            result = response.json()
            print("✅ Member rating submitted successfully!")
            print(f"   Member rating: {result['rating']['rating']}/5")
            print(f"   Member average: {result['member_average']}/5")
            print(f"   AI rating preserved: {result['ai_rating']}/5")
            
            # Verify the AI rating is preserved
            if result['ai_rating'] == ai_rating:
                print("✅ AI rating correctly preserved!")
            else:
                print(f"❌ AI rating not preserved! Expected: {ai_rating}, Got: {result['ai_rating']}")
        else:
            print(f"❌ Failed to submit rating: {response.status_code}")
            print(f"   Response: {response.text}")
            return
        
        # Get updated event to verify
        print(f"\n📊 Verifying updated event...")
        response = requests.get("http://localhost:5000/event-history")
        events = response.json()
        
        for event in events:
            if event['id'] == event_id:
                print(f"✅ Event updated successfully!")
                print(f"   AI Rating: {event.get('ai_rating', 'N/A')}/5")
                print(f"   Member Average: {event.get('rating', 'N/A')}/5")
                print(f"   Member ratings count: {len(event.get('member_ratings', []))}")
                
                # Verify both ratings exist
                if event.get('ai_rating') and event.get('rating'):
                    print("✅ Both AI rating and member average are present!")
                else:
                    print("❌ Missing ratings!")
                break
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    test_ai_member_ratings() 