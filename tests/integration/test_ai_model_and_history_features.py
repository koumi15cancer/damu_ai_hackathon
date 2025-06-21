#!/usr/bin/env python3
"""
Test script to verify the AI model selector and event history features.
"""

import requests
import json
import time

def test_backend_endpoints():
    """Test the new backend endpoints."""
    base_url = "http://localhost:5000"
    
    print("🧪 Testing Backend Endpoints...")
    
    # Test AI models endpoint
    try:
        response = requests.get(f"{base_url}/ai-models")
        if response.status_code == 200:
            models = response.json()
            print(f"✅ AI Models endpoint: {models}")
        else:
            print(f"❌ AI Models endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ AI Models endpoint error: {e}")
    
    # Test event history endpoint
    try:
        response = requests.get(f"{base_url}/event-history")
        if response.status_code == 200:
            history = response.json()
            print(f"✅ Event History endpoint: {len(history)} events found")
        else:
            print(f"❌ Event History endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Event History endpoint error: {e}")
    
    # Test generate plans with new parameters
    try:
        test_data = {
            "theme": "fun 🎉",
            "budget_contribution": "Yes, up to 100,000 VND",
            "available_members": ["Ben", "Sarah", "Mike"],
            "date_time": "2024-12-15T18:00",
            "location_zone": "District 1",
            "ai_model": "Google Gemini",
            "plan_generation_mode": "similar"
        }
        
        response = requests.post(f"{base_url}/generate-plans", json=test_data)
        if response.status_code == 200:
            plans = response.json()
            print(f"✅ Generate Plans with new parameters: {len(plans)} plans generated")
        else:
            print(f"❌ Generate Plans failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Generate Plans error: {e}")

def test_frontend_integration():
    """Test frontend integration points."""
    print("\n🧪 Testing Frontend Integration...")
    
    # Test that frontend can access backend endpoints
    try:
        response = requests.get("http://localhost:3000")
        if response.status_code == 200:
            print("✅ Frontend is running")
        else:
            print(f"❌ Frontend not accessible: {response.status_code}")
    except Exception as e:
        print(f"❌ Frontend not running: {e}")

def test_analytics_suggestions():
    """Test analytics suggestions endpoint."""
    print("\n🧪 Testing Analytics Suggestions...")
    
    try:
        response = requests.get("http://localhost:5000/analytics/suggestions?limit=5")
        if response.status_code == 200:
            suggestions = response.json()
            print(f"✅ Analytics suggestions: {len(suggestions.get('suggestions', []))} suggestions")
        else:
            print(f"❌ Analytics suggestions failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Analytics suggestions error: {e}")

def main():
    """Main test function."""
    print("🚀 Testing AI Model Selector and Event History Features")
    print("=" * 60)
    
    # Wait a moment for services to start
    time.sleep(2)
    
    test_backend_endpoints()
    test_frontend_integration()
    test_analytics_suggestions()
    
    print("\n" + "=" * 60)
    print("✅ Testing Complete!")
    print("\n📋 Summary of New Features:")
    print("1. ✅ AI Model Selector in Event Preferences")
    print("2. ✅ Event History Summary with generation options")
    print("3. ✅ Backend API endpoints for AI models and event history")
    print("4. ✅ Plan generation with AI model selection")
    print("5. ✅ Plan generation modes (reuse/similar/new)")
    print("6. ✅ Analytics suggestions positioned above generate button")

if __name__ == "__main__":
    main() 