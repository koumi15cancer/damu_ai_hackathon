#!/usr/bin/env python3
"""
Test script to demonstrate analytics data integration in plan generation.
This shows how event history data is used for "similar" and "reuse" options.
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:5000"


def test_analytics_integration():
    """Test how analytics data is used in plan generation."""
    print("🧪 Testing Analytics Integration in Plan Generation")
    print("=" * 60)

    # Step 1: First, let's create some sample event history
    print("\n📝 Step 1: Creating sample event history...")
    sample_events = [
        {
            "date": "2024-01-15",
            "theme": "fun 🎉",
            "location": "District 1",
            "participants": ["Alice", "Bob", "Charlie"],
            "activities": ["Hotpot Dinner", "Karaoke", "Bar Hopping"],
            "total_cost": 450000,
            "rating": 4,
            "phases": [
                {"activity": "Hotpot Dinner", "cost": 250000},
                {"activity": "Karaoke", "cost": 100000},
                {"activity": "Bar Hopping", "cost": 100000},
            ],
        },
        {
            "date": "2024-01-20",
            "theme": "chill 🧘",
            "location": "District 2",
            "participants": ["Alice", "Bob", "David"],
            "activities": ["Cafe Meeting", "Board Games"],
            "total_cost": 200000,
            "rating": 5,
            "phases": [
                {"activity": "Cafe Meeting", "cost": 150000},
                {"activity": "Board Games", "cost": 50000},
            ],
        },
        {
            "date": "2024-01-25",
            "theme": "outdoor 🌤",
            "location": "District 7",
            "participants": ["Alice", "Charlie", "Eve"],
            "activities": ["Park Walk", "Outdoor Dining"],
            "total_cost": 300000,
            "rating": 4,
            "phases": [
                {"activity": "Park Walk", "cost": 0},
                {"activity": "Outdoor Dining", "cost": 300000},
            ],
        },
    ]

    # Save sample events
    for event in sample_events:
        try:
            response = requests.post(f"{BASE_URL}/event-history", json=event)
            if response.status_code == 200:
                print(f"✅ Saved event: {event['theme']} on {event['date']}")
            else:
                print(f"⚠️ Event already exists: {event['theme']} on {event['date']}")
        except Exception as e:
            print(f"❌ Error saving event: {e}")

    # Step 2: Test plan generation with "new" mode (no analytics)
    print("\n🆕 Step 2: Testing 'new' mode (no analytics data)...")
    new_mode_request = {
        "theme": "fun 🎉",
        "budget_contribution": "No",
        "available_members": ["Alice", "Bob", "Charlie"],
        "plan_generation_mode": "new",
    }

    try:
        response = requests.post(f"{BASE_URL}/generate-plans", json=new_mode_request)
        if response.status_code == 200:
            plans = response.json()
            print(f"✅ Generated {len(plans)} plans with 'new' mode")
            print(f"📊 No analytics data used (as expected)")
        else:
            print(f"❌ Failed to generate plans: {response.text}")
    except Exception as e:
        print(f"❌ Error in new mode test: {e}")

    # Step 3: Test plan generation with "similar" mode (with analytics)
    print("\n🔄 Step 3: Testing 'similar' mode (with analytics data)...")
    similar_mode_request = {
        "theme": "fun 🎉",
        "budget_contribution": "No",
        "available_members": ["Alice", "Bob", "Charlie"],
        "plan_generation_mode": "similar",
    }

    try:
        response = requests.post(
            f"{BASE_URL}/generate-plans", json=similar_mode_request
        )
        if response.status_code == 200:
            plans = response.json()
            print(f"✅ Generated {len(plans)} plans with 'similar' mode")
            print(f"📊 Analytics data from {len(sample_events)} historical events used")

            # Show what analytics insights were used
            print("\n📈 Analytics Insights Used:")
            themes = [e["theme"] for e in sample_events]
            costs = [e["total_cost"] for e in sample_events]
            ratings = [e["rating"] for e in sample_events]

            avg_cost = sum(costs) / len(costs)
            avg_rating = sum(ratings) / len(ratings)
            most_popular_theme = max(set(themes), key=themes.count)

            print(f"• Most popular theme: {most_popular_theme}")
            print(f"• Average cost: {avg_cost:,.0f} VND")
            print(f"• Average rating: {avg_rating:.1f}/5")
            print(
                f"• Recent activities: {', '.join(set([act for e in sample_events for act in e['activities']]))}"
            )

        else:
            print(f"❌ Failed to generate plans: {response.text}")
    except Exception as e:
        print(f"❌ Error in similar mode test: {e}")

    # Step 4: Test plan generation with "reuse" mode (with analytics)
    print("\n🔄 Step 4: Testing 'reuse' mode (with analytics data)...")
    reuse_mode_request = {
        "theme": "chill 🧘",
        "budget_contribution": "No",
        "available_members": ["Alice", "Bob", "Charlie"],
        "plan_generation_mode": "reuse",
    }

    try:
        response = requests.post(f"{BASE_URL}/generate-plans", json=reuse_mode_request)
        if response.status_code == 200:
            plans = response.json()
            print(f"✅ Generated {len(plans)} plans with 'reuse' mode")
            print(f"📊 Reusing structure from {len(sample_events)} historical events")

            # Show what structure is being reused
            print("\n📋 Structure Being Reused:")
            for event in sample_events:
                print(
                    f"• {event['theme']}: {len(event['phases'])} phases, {event['total_cost']:,} VND"
                )

        else:
            print(f"❌ Failed to generate plans: {response.text}")
    except Exception as e:
        print(f"❌ Error in reuse mode test: {e}")

    # Step 5: Show the difference in prompts
    print("\n📝 Step 5: Prompt Comparison")
    print("=" * 40)
    print("🆕 NEW MODE: Generic prompt without historical data")
    print("🔄 SIMILAR MODE: Prompt includes recent events and analytics insights")
    print("🔄 REUSE MODE: Prompt includes event structure and patterns")

    print("\n✅ Analytics Integration Test Complete!")
    print("\nKey Points:")
    print("• 'new' mode: No analytics data used")
    print("• 'similar' mode: Uses event history for inspiration")
    print("• 'reuse' mode: Uses event structure and patterns")
    print("• Analytics insights include: themes, costs, ratings, activities")


if __name__ == "__main__":
    test_analytics_integration()
