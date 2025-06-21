#!/usr/bin/env python3
"""
Test script for analytics functionality
"""

import requests
import json


def test_analytics_endpoint():
    """Test the analytics suggestions endpoint"""
    print("🧪 Testing Analytics Endpoint...")
    print("=" * 50)

    try:
        # Test basic analytics request
        print("📊 Testing basic analytics request...")
        response = requests.get("http://localhost:5000/analytics/suggestions")

        if response.status_code == 200:
            data = response.json()
            print("✅ Analytics endpoint working!")
            print(
                f"   Total events analyzed: {data['analytics_summary']['total_events']}"
            )
            print(f"   Suggestions generated: {len(data['suggestions'])}")
            print(
                f"   Most popular theme: {data['analytics_summary']['most_popular_theme']}"
            )
            print(
                f"   Average cost: {data['analytics_summary']['average_cost']:,.0f} VND"
            )

            # Show suggestions
            if data["suggestions"]:
                print("\n📝 Generated Suggestions:")
                for i, suggestion in enumerate(data["suggestions"], 1):
                    print(f"   {i}. {suggestion['title']}")
                    print(f"      Category: {suggestion['category']}")
                    print(f"      Confidence: {suggestion['confidence']:.1%}")
                    print(f"      Description: {suggestion['description'][:100]}...")
                    print()
        else:
            print(f"❌ Failed to get analytics: {response.status_code}")
            print(f"   Response: {response.text}")
            return

        # Test with different limits
        print("🔢 Testing with different limits...")
        for limit in [5, 10, 20]:
            response = requests.get(
                f"http://localhost:5000/analytics/suggestions?limit={limit}"
            )
            if response.status_code == 200:
                data = response.json()
                print(
                    f"   ✅ Limit {limit}: {data['analytics_summary']['total_events']} events analyzed"
                )
            else:
                print(f"   ❌ Limit {limit}: Failed")

        # Test theme filtering
        print("\n🎨 Testing theme filtering...")
        themes = ["fun 🎉", "chill 🧘", "outdoor 🌤"]
        for theme in themes:
            response = requests.get(
                f"http://localhost:5000/analytics/suggestions?theme={theme}"
            )
            if response.status_code == 200:
                data = response.json()
                print(
                    f"   ✅ Theme '{theme}': {data['analytics_summary']['total_events']} events"
                )
            else:
                print(f"   ❌ Theme '{theme}': Failed")

        # Check if analytics data file was created
        print("\n💾 Checking analytics data file...")
        try:
            with open("backend/tmp/analytics_data.json", "r") as f:
                analytics_data = json.load(f)
                history_count = len(analytics_data.get("analytics_history", []))
                print(f"   ✅ Analytics data file exists with {history_count} entries")
        except FileNotFoundError:
            print("   ⚠️  Analytics data file not found in backend/tmp/")
        except Exception as e:
            print(f"   ❌ Error reading analytics data: {e}")

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    test_analytics_endpoint()
