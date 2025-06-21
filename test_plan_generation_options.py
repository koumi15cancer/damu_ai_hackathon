#!/usr/bin/env python3
"""
Comprehensive test to demonstrate the differences between the three plan generation options:
1. Reuse previous plan structure
2. Generate similar plan  
3. Create brand new plan

This test shows how each option uses analytics data differently and produces distinct results.
"""

import requests
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any

BASE_URL = "http://localhost:5000"


class PlanGenerationTester:
    def __init__(self):
        self.test_events = []
        self.results = {}

    def setup_test_data(self):
        """Create comprehensive test event history with different patterns."""
        print("📝 Setting up comprehensive test data...")

        # Create diverse event history with clear patterns
        self.test_events = [
            # High-rated fun events (3-phase structure)
            {
                "date": "2024-01-10",
                "theme": "fun 🎉",
                "location": "District 1",
                "participants": ["Alice", "Bob", "Charlie", "David"],
                "activities": ["Hotpot Dinner", "Karaoke", "Bar Hopping"],
                "total_cost": 450000,
                "rating": 5,
                "phases": [
                    {
                        "activity": "Hotpot Dinner at Pho 24",
                        "cost": 250000,
                        "location": "123 Nguyen Hue",
                    },
                    {
                        "activity": "Karaoke at Music Box",
                        "cost": 100000,
                        "location": "456 Le Loi",
                    },
                    {
                        "activity": "Bar Hopping",
                        "cost": 100000,
                        "location": "789 Bui Vien",
                    },
                ],
            },
            # Successful chill event (2-phase structure)
            {
                "date": "2024-01-15",
                "theme": "chill 🧘",
                "location": "District 2",
                "participants": ["Alice", "Bob", "Eve"],
                "activities": ["Cafe Meeting", "Board Games"],
                "total_cost": 200000,
                "rating": 4,
                "phases": [
                    {
                        "activity": "Cafe Meeting at Highlands",
                        "cost": 150000,
                        "location": "321 Thao Dien",
                    },
                    {
                        "activity": "Board Games at Home",
                        "cost": 50000,
                        "location": "654 Crescent",
                    },
                ],
            },
            # Outdoor adventure (2-phase structure)
            {
                "date": "2024-01-20",
                "theme": "outdoor 🌤",
                "location": "District 7",
                "participants": ["Alice", "Charlie", "Frank"],
                "activities": ["Park Walk", "Outdoor Dining"],
                "total_cost": 300000,
                "rating": 4,
                "phases": [
                    {
                        "activity": "Park Walk at Crescent Mall",
                        "cost": 0,
                        "location": "Park Area",
                    },
                    {
                        "activity": "Outdoor Dining at The Deck",
                        "cost": 300000,
                        "location": "789 Crescent",
                    },
                ],
            },
            # Another successful fun event (3-phase structure)
            {
                "date": "2024-01-25",
                "theme": "fun 🎉",
                "location": "District 3",
                "participants": ["Bob", "Charlie", "David", "Eve"],
                "activities": ["BBQ Dinner", "Escape Room", "Pub Crawl"],
                "total_cost": 500000,
                "rating": 5,
                "phases": [
                    {
                        "activity": "BBQ Dinner at Korean BBQ",
                        "cost": 300000,
                        "location": "123 Pasteur",
                    },
                    {
                        "activity": "Escape Room Challenge",
                        "cost": 150000,
                        "location": "456 Hai Ba Trung",
                    },
                    {
                        "activity": "Pub Crawl",
                        "cost": 50000,
                        "location": "789 Dong Khoi",
                    },
                ],
            },
            # Budget-friendly chill event (2-phase structure)
            {
                "date": "2024-01-30",
                "theme": "chill 🧘",
                "location": "District 1",
                "participants": ["Alice", "David", "Frank"],
                "activities": ["Tea House", "Movie Night"],
                "total_cost": 150000,
                "rating": 3,
                "phases": [
                    {
                        "activity": "Tea House at Tien Phat",
                        "cost": 100000,
                        "location": "321 Le Thanh Ton",
                    },
                    {
                        "activity": "Movie Night at CGV",
                        "cost": 50000,
                        "location": "654 Vincom",
                    },
                ],
            },
        ]

        # Save all test events
        for event in self.test_events:
            try:
                response = requests.post(f"{BASE_URL}/event-history", json=event)
                if response.status_code == 200:
                    print(
                        f"✅ Saved: {event['theme']} on {event['date']} (Rating: {event['rating']}/5)"
                    )
                else:
                    print(f"⚠️ Already exists: {event['theme']} on {event['date']}")
            except Exception as e:
                print(f"❌ Error saving event: {e}")

        print(f"\n📊 Test data setup complete: {len(self.test_events)} events created")
        self._print_analytics_summary()

    def _print_analytics_summary(self):
        """Print analytics summary of test data."""
        print("\n📈 ANALYTICS SUMMARY OF TEST DATA:")
        print("=" * 50)

        themes = [e["theme"] for e in self.test_events]
        costs = [e["total_cost"] for e in self.test_events]
        ratings = [e["rating"] for e in self.test_events]
        phase_counts = [len(e["phases"]) for e in self.test_events]

        # Theme analysis
        theme_counts = {}
        for theme in themes:
            theme_counts[theme] = theme_counts.get(theme, 0) + 1

        print(
            f"🎯 Most popular theme: {max(theme_counts, key=theme_counts.get)} ({theme_counts[max(theme_counts, key=theme_counts.get)]} events)"
        )
        print(f"💰 Average cost: {sum(costs)/len(costs):,.0f} VND")
        print(f"⭐ Average rating: {sum(ratings)/len(ratings):.1f}/5")
        print(f"📋 Average phases: {sum(phase_counts)/len(phase_counts):.1f}")

        # Structure patterns
        print(f"\n📋 STRUCTURE PATTERNS:")
        for theme in set(themes):
            theme_events = [e for e in self.test_events if e["theme"] == theme]
            avg_phases = sum(len(e["phases"]) for e in theme_events) / len(theme_events)
            avg_cost = sum(e["total_cost"] for e in theme_events) / len(theme_events)
            avg_rating = sum(e["rating"] for e in theme_events) / len(theme_events)
            print(
                f"• {theme}: {avg_phases:.0f} phases, {avg_cost:,.0f} VND avg, {avg_rating:.1f}/5 avg rating"
            )

    def test_generation_options(self):
        """Test all three generation options with the same input."""
        print("\n🧪 TESTING ALL THREE GENERATION OPTIONS")
        print("=" * 60)

        # Common test parameters
        test_params = {
            "theme": "fun 🎉",
            "budget_contribution": "No",
            "available_members": ["Alice", "Bob", "Charlie", "David"],
            "date_time": "2024-02-15 18:00",
            "location_zone": "District 1",
        }

        options = [
            ("new", "Create brand new plan"),
            ("similar", "Generate similar plan"),
            ("reuse", "Reuse previous plan structure"),
        ]

        for option, description in options:
            print(f"\n🔄 Testing: {description}")
            print("-" * 40)

            request_data = {**test_params, "plan_generation_mode": option}

            try:
                start_time = time.time()
                response = requests.post(
                    f"{BASE_URL}/generate-plans", json=request_data
                )
                response_time = time.time() - start_time

                if response.status_code == 200:
                    plans = response.json()
                    self.results[option] = {
                        "plans": plans,
                        "response_time": response_time,
                        "count": len(plans),
                    }

                    print(f"✅ Generated {len(plans)} plans in {response_time:.2f}s")
                    self._analyze_plans(option, plans)

                else:
                    print(f"❌ Failed: {response.text}")

            except Exception as e:
                print(f"❌ Error: {e}")

    def _analyze_plans(self, option: str, plans: List[Dict]):
        """Analyze the characteristics of generated plans."""
        print(f"\n📊 ANALYSIS FOR '{option.upper()}' OPTION:")

        if not plans:
            print("❌ No plans generated")
            return

        # Cost analysis
        costs = [plan.get("total_cost", 0) for plan in plans]
        avg_cost = sum(costs) / len(costs)
        print(
            f"💰 Average cost: {avg_cost:,.0f} VND (range: {min(costs):,.0f} - {max(costs):,.0f})"
        )

        # Phase analysis
        phase_counts = [len(plan.get("phases", [])) for plan in plans]
        avg_phases = sum(phase_counts) / len(phase_counts)
        print(
            f"📋 Average phases: {avg_phases:.1f} (range: {min(phase_counts)} - {max(phase_counts)})"
        )

        # Activity analysis
        all_activities = []
        for plan in plans:
            for phase in plan.get("phases", []):
                activity = phase.get("activity", "Unknown")
                all_activities.append(activity)

        # Show unique activities
        unique_activities = list(set(all_activities))
        print(f"🎯 Unique activities: {len(unique_activities)}")
        print(f"   Sample: {', '.join(unique_activities[:5])}")

        # Show plan details
        print(f"\n📋 PLAN DETAILS:")
        for i, plan in enumerate(plans[:2]):  # Show first 2 plans
            phases = plan.get("phases", [])
            print(
                f"  Plan {i+1}: {len(phases)} phases, {plan.get('total_cost', 0):,.0f} VND"
            )
            for j, phase in enumerate(phases):
                print(
                    f"    Phase {j+1}: {phase.get('activity', 'Unknown')} ({phase.get('cost', 0):,.0f} VND)"
                )

    def compare_results(self):
        """Compare results across all three options."""
        print("\n🔍 COMPARISON OF ALL THREE OPTIONS")
        print("=" * 60)

        if not self.results:
            print("❌ No results to compare")
            return

        # Create comparison table
        print(
            f"{'Option':<15} {'Plans':<8} {'Avg Cost':<12} {'Avg Phases':<12} {'Response Time':<15}"
        )
        print("-" * 70)

        for option in ["new", "similar", "reuse"]:
            if option in self.results:
                result = self.results[option]
                plans = result["plans"]

                if plans:
                    costs = [plan.get("total_cost", 0) for plan in plans]
                    phase_counts = [len(plan.get("phases", [])) for plan in plans]

                    avg_cost = sum(costs) / len(costs)
                    avg_phases = sum(phase_counts) / len(phase_counts)

                    print(
                        f"{option.upper():<15} {len(plans):<8} {avg_cost:,.0f} VND{'':<4} {avg_phases:.1f}{'':<8} {result['response_time']:.2f}s"
                    )

        # Detailed analysis
        print(f"\n📈 DETAILED ANALYSIS:")
        print("=" * 40)

        # Cost comparison
        print(f"\n💰 COST COMPARISON:")
        for option in ["new", "similar", "reuse"]:
            if option in self.results and self.results[option]["plans"]:
                costs = [
                    plan.get("total_cost", 0) for plan in self.results[option]["plans"]
                ]
                avg_cost = sum(costs) / len(costs)
                print(f"• {option.upper()}: {avg_cost:,.0f} VND average")

        # Structure comparison
        print(f"\n📋 STRUCTURE COMPARISON:")
        for option in ["new", "similar", "reuse"]:
            if option in self.results and self.results[option]["plans"]:
                phase_counts = [
                    len(plan.get("phases", []))
                    for plan in self.results[option]["plans"]
                ]
                avg_phases = sum(phase_counts) / len(phase_counts)
                print(f"• {option.upper()}: {avg_phases:.1f} phases average")

        # Activity variety
        print(f"\n🎯 ACTIVITY VARIETY:")
        for option in ["new", "similar", "reuse"]:
            if option in self.results and self.results[option]["plans"]:
                all_activities = []
                for plan in self.results[option]["plans"]:
                    for phase in plan.get("phases", []):
                        all_activities.append(phase.get("activity", "Unknown"))
                unique_count = len(set(all_activities))
                print(f"• {option.upper()}: {unique_count} unique activities")

    def explain_differences(self):
        """Explain the expected differences between options."""
        print("\n📚 EXPLANATION OF DIFFERENCES")
        print("=" * 50)

        print(f"\n🆕 NEW MODE:")
        print("• No analytics data used")
        print("• Completely fresh, innovative ideas")
        print("• May have higher cost variation")
        print("• More diverse activity types")
        print("• Independent of past success patterns")

        print(f"\n🔄 SIMILAR MODE:")
        print("• Uses event history for inspiration")
        print("• Variations of successful activities")
        print("• Cost patterns similar to historical average")
        print("• Activity types based on high-rated past events")
        print("• Incorporates most popular themes")

        print(f"\n🔄 REUSE MODE:")
        print("• Follows exact structure patterns")
        print("• Reuses successful phase combinations")
        print("• Cost structure similar to past events")
        print("• Maintains proven activity flows")
        print("• Highest consistency with historical data")

        print(f"\n🎯 EXPECTED PATTERNS:")
        print("• NEW: Highest variety, unpredictable costs")
        print("• SIMILAR: Moderate variety, predictable costs")
        print("• REUSE: Lowest variety, most predictable costs")


def main():
    """Run the comprehensive test."""
    print("🧪 COMPREHENSIVE PLAN GENERATION OPTIONS TEST")
    print("=" * 70)
    print("This test demonstrates the differences between:")
    print("1. Reuse previous plan structure")
    print("2. Generate similar plan")
    print("3. Create brand new plan")
    print("=" * 70)

    tester = PlanGenerationTester()

    # Step 1: Setup test data
    tester.setup_test_data()

    # Step 2: Test all options
    tester.test_generation_options()

    # Step 3: Compare results
    tester.compare_results()

    # Step 4: Explain differences
    tester.explain_differences()

    print(f"\n✅ Test completed successfully!")
    print(
        f"📊 Check the results above to see how each option produces different plans."
    )


if __name__ == "__main__":
    main()
