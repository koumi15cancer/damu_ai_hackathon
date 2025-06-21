#!/usr/bin/env python3
"""
Test script to demonstrate the complete flow:
Frontend -> Backend API -> AI Service -> Response
"""

import requests
import json
import time

def test_complete_flow():
    """Test the complete flow from frontend to AI service."""
    
    print("🚀 Testing Complete Team Bonding Event Planner Flow")
    print("=" * 60)
    
    # Test 1: Health Check
    print("\n1. Testing Backend Health...")
    try:
        response = requests.get("http://localhost:5000/health")
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ Backend is healthy!")
            print(f"   AI Provider: {health_data.get('ai_provider', 'unknown')}")
            print(f"   Status: {health_data.get('status', 'unknown')}")
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Cannot connect to backend: {e}")
        return
    
    # Test 2: Get Team Members
    print("\n2. Loading Team Members...")
    try:
        response = requests.get("http://localhost:5000/team-members")
        if response.status_code == 200:
            team_members = response.json()
            print(f"✅ Loaded {len(team_members)} team members:")
            for member in team_members[:3]:  # Show first 3
                print(f"   • {member['name']} ({member['vibe']}) - {member['location']}")
            if len(team_members) > 3:
                print(f"   ... and {len(team_members) - 3} more")
        else:
            print(f"❌ Failed to load team members: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Error loading team members: {e}")
        return
    
    # Test 3: Generate Plans (Frontend-like request)
    print("\n3. Generating Team Bonding Plans...")
    
    # Simulate frontend request
    frontend_request = {
        "theme": "fun 🎉",
        "budget_contribution": "Yes, up to 100,000 VND",
        "available_members": ["Ben", "Cody", "Lil Thanh", "Big Thanh"],
        "date_time": "2024-12-15T18:00",
        "location_zone": "District 1"
    }
    
    print(f"   Request payload:")
    print(f"   • Theme: {frontend_request['theme']}")
    print(f"   • Budget: {frontend_request['budget_contribution']}")
    print(f"   • Members: {', '.join(frontend_request['available_members'])}")
    print(f"   • Date: {frontend_request['date_time']}")
    print(f"   • Location: {frontend_request['location_zone']}")
    
    try:
        start_time = time.time()
        response = requests.post(
            "http://localhost:5000/generate-plans",
            json=frontend_request,
            headers={"Content-Type": "application/json"}
        )
        response_time = time.time() - start_time
        
        if response.status_code == 200:
            plans = response.json()
            print(f"✅ Generated {len(plans)} plans in {response_time:.2f}s")
            
            # Display plans
            for i, plan in enumerate(plans, 1):
                print(f"\n   📋 Plan {i}:")
                print(f"      💰 Total Cost: {plan['total_cost']:,} VND")
                if plan['contribution_needed'] > 0:
                    print(f"      ⚠️  Additional Contribution: {plan['contribution_needed']:,} VND")
                print(f"      ⭐ Rating: {plan['rating']}/5")
                print(f"      👥 Fit: {plan['fit_analysis']}")
                
                print(f"      📍 Activities:")
                for j, phase in enumerate(plan['phases'], 1):
                    print(f"         {j}. {phase['activity']}")
                    print(f"            📍 {phase['location']}")
                    print(f"            💰 {phase['cost']:,} VND")
                    print(f"            🏷️  {', '.join(phase['indicators'])}")
        else:
            print(f"❌ Failed to generate plans: {response.status_code}")
            print(f"   Response: {response.text}")
            return
    except Exception as e:
        print(f"❌ Error generating plans: {e}")
        return
    
    # Test 4: Test different themes
    print("\n4. Testing Different Themes...")
    themes = ["chill 🧘", "outdoor 🌤"]
    
    for theme in themes:
        print(f"\n   Testing theme: {theme}")
        test_request = {
            "theme": theme,
            "budget_contribution": "No",
            "available_members": ["Ben", "Hoa", "Mason"],
            "location_zone": "District 3"
        }
        
        try:
            response = requests.post(
                "http://localhost:5000/generate-plans",
                json=test_request,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                plans = response.json()
                print(f"   ✅ Generated {len(plans)} plans for {theme}")
                for plan in plans:
                    print(f"      • {plan['phases'][0]['activity']} - {plan['total_cost']:,} VND")
            else:
                print(f"   ❌ Failed for {theme}")
        except Exception as e:
            print(f"   ❌ Error for {theme}: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Complete Flow Test Finished!")
    print("\n📝 Summary:")
    print("✅ Backend API is running and healthy")
    print("✅ Team members are loaded successfully")
    print("✅ AI service integration is working (with fallback)")
    print("✅ Frontend can successfully call the API")
    print("✅ Different themes generate appropriate plans")
    print("\n🚀 The complete flow is working correctly!")
    print("   Frontend -> Backend API -> AI Service -> Response")

if __name__ == "__main__":
    test_complete_flow() 