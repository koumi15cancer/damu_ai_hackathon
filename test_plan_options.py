#!/usr/bin/env python3
"""
Test script to demonstrate differences between the three plan generation options:
1. Reuse previous plan structure
2. Generate similar plan  
3. Create brand new plan
"""

import requests
import json
import time

BASE_URL = "http://localhost:5000"


def setup_test_data():
    """Create test event history."""
    print("📝 Setting up test data...")

    test_events = [
        {
            "date": "2024-01-15",
            "theme": "fun 🎉",
            "location": "District 1",
            "participants": ["Alice", "Bob", "Charlie"],
            "activities": ["Hotpot Dinner", "Karaoke", "Bar Hopping"],
            "total_cost": 450000,
            "rating": 5,
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
            "rating": 4,
            "phases": [
                {"activity": "Cafe Meeting", "cost": 150000},
                {"activity": "Board Games", "cost": 50000},
            ],
        },
    ]

    for event in test_events:
        try:
            response = requests.post(f"{BASE_URL}/event-history", json=event)
            if response.status_code == 200:
                print(f"✅ Saved: {event['theme']} - {event['total_cost']:,} VND")
        except Exception as e:
            print(f"⚠️ Event exists or error: {e}")


def test_option(option_name, description):
    """Test a specific generation option."""
    print(f"\n🔄 Testing: {description}")
    print("-" * 40)

    request_data = {
        "theme": "fun 🎉",
        "budget_contribution": "No",
        "available_members": ["Alice", "Bob", "Charlie"],
        "plan_generation_mode": option_name,
    }

    try:
        start_time = time.time()
        response = requests.post(f"{BASE_URL}/generate-plans", json=request_data)
        response_time = time.time() - start_time

        if response.status_code == 200:
            plans = response.json()
            print(f"✅ Generated {len(plans)} plans in {response_time:.2f}s")

            # Analyze plans
            costs = [plan.get("total_cost", 0) for plan in plans]
            phase_counts = [len(plan.get("phases", [])) for plan in plans]

            print(f"💰 Average cost: {sum(costs)/len(costs):,.0f} VND")
            print(f"📋 Average phases: {sum(phase_counts)/len(phase_counts):.1f}")

            # Show first plan details
            if plans:
                plan = plans[0]
                print(f"📋 Sample plan:")
                for i, phase in enumerate(plan.get("phases", [])):
                    print(
                        f"  Phase {i+1}: {phase.get('activity', 'Unknown')} ({phase.get('cost', 0):,.0f} VND)"
                    )

            return plans
        else:
            print(f"❌ Failed: {response.text}")
            return []

    except Exception as e:
        print(f"❌ Error: {e}")
        return []


def main():
    """Run the test."""
    print("🧪 PLAN GENERATION OPTIONS TEST")
    print("=" * 50)

    # Setup test data
    setup_test_data()

    # Test all three options
    results = {}

    results["new"] = test_option("new", "Create brand new plan")
    results["similar"] = test_option("similar", "Generate similar plan")
    results["reuse"] = test_option("reuse", "Reuse previous plan structure")

    # Compare results
    print(f"\n🔍 COMPARISON")
    print("=" * 50)

    for option, plans in results.items():
        if plans:
            costs = [plan.get("total_cost", 0) for plan in plans]
            phase_counts = [len(plan.get("phases", [])) for plan in plans]
            avg_cost = sum(costs) / len(costs)
            avg_phases = sum(phase_counts) / len(phase_counts)

            print(
                f"{option.upper()}: {len(plans)} plans, {avg_cost:,.0f} VND avg, {avg_phases:.1f} phases avg"
            )

    print(f"\n📚 EXPECTED DIFFERENCES:")
    print("• NEW: Highest variety, unpredictable")
    print("• SIMILAR: Moderate variety, uses history")
    print("• REUSE: Most consistent, follows patterns")


if __name__ == "__main__":
    main()
