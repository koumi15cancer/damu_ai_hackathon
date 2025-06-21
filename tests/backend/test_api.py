#!/usr/bin/env python3
"""
Test script for the new Team Bonding Event Planner API
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_health_check():
    """Test the health check endpoint."""
    print("Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_get_team_members():
    """Test getting team members."""
    print("\nTesting GET /team-members...")
    try:
        response = requests.get(f"{BASE_URL}/team-members")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            members = response.json()
            print(f"Found {len(members)} team members")
            for member in members[:3]:  # Show first 3
                print(f"  - {member['name']} ({member['vibe']})")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_create_team_member():
    """Test creating a new team member."""
    print("\nTesting POST /team-members...")
    try:
        new_member = {
            "name": "Test User",
            "location": "District 1, Ho Chi Minh City",
            "preferences": ["Cafe", "Games", "Outdoor activities"],
            "vibe": "Mixed"
        }
        response = requests.post(f"{BASE_URL}/team-members", json=new_member)
        print(f"Status: {response.status_code}")
        if response.status_code == 201:
            created_member = response.json()
            print(f"Created member: {created_member['name']} (ID: {created_member['id']})")
            return created_member['id']
        else:
            print(f"Error response: {response.json()}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def test_update_team_member(member_id):
    """Test updating a team member."""
    print(f"\nTesting PUT /team-members/{member_id}...")
    try:
        update_data = {
            "name": "Updated Test User",
            "location": "District 2, Ho Chi Minh City",
            "preferences": ["Cafe", "Games", "Indoor activities"],
            "vibe": "Chill"
        }
        response = requests.put(f"{BASE_URL}/team-members/{member_id}", json=update_data)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            updated_member = response.json()
            print(f"Updated member: {updated_member['name']}")
            return True
        else:
            print(f"Error response: {response.json()}")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_delete_team_member(member_id):
    """Test deleting a team member."""
    print(f"\nTesting DELETE /team-members/{member_id}...")
    try:
        response = requests.delete(f"{BASE_URL}/team-members/{member_id}")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Delete result: {result['message']}")
            return True
        else:
            print(f"Error response: {response.json()}")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_generate_plans():
    """Test generating team bonding plans."""
    print("\nTesting POST /generate-plans...")
    try:
        plan_request = {
            "theme": "fun 🎉",
            "budget_contribution": "Yes, up to 150,000 VND",
            "available_members": ["Ben", "Cody", "Big Thanh"],
            "date_time": "2023-12-15 18:00",
            "location_zone": "District 1"
        }
        response = requests.post(f"{BASE_URL}/generate-plans", json=plan_request)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            plans = response.json()
            print(f"Generated {len(plans)} plans")
            for i, plan in enumerate(plans[:2]):  # Show first 2 plans
                print(f"  Plan {i+1}:")
                print(f"    Total cost: {plan['total_cost']:,} VND")
                print(f"    Contribution needed: {plan['contribution_needed']:,} VND")
                print(f"    Rating: {plan['rating']} stars")
                print(f"    Phases: {len(plan['phases'])}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    """Run all tests."""
    print("=== Team Bonding Event Planner API Tests ===\n")
    
    # Test health check
    if not test_health_check():
        print("Health check failed. Make sure the server is running.")
        return
    
    # Test team member operations
    test_get_team_members()
    
    # Test CRUD operations
    member_id = test_create_team_member()
    if member_id:
        test_update_team_member(member_id)
        test_delete_team_member(member_id)
    
    # Test plan generation
    test_generate_plans()
    
    print("\n=== Tests completed ===")

if __name__ == "__main__":
    main() 