#!/usr/bin/env python3
"""
Test script to demonstrate the analytics trigger flow with comprehensive logging.
This script simulates the complete flow from plan generation to analytics updates.
"""

import requests
import json
import time
import logging
from datetime import datetime, timedelta
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("analytics_flow_test.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

BASE_URL = "http://localhost:5000"


def test_analytics_flow():
    """Test the complete analytics trigger flow."""
    logger.info("🚀 Starting Analytics Flow Test")
    logger.info("=" * 60)

    try:
        # Step 1: Check initial analytics state
        logger.info("📊 Step 1: Checking initial analytics state")
        initial_analytics = get_analytics()
        logger.info(
            f"✅ Initial analytics loaded: {len(initial_analytics.get('suggestions', []))} suggestions"
        )

        # Step 2: Generate and save a new plan
        logger.info("📋 Step 2: Generating and saving a new plan")
        plan_data = generate_test_plan()
        saved_plan = save_plan(plan_data)
        logger.info(f"✅ Plan saved successfully: {saved_plan.get('id')}")

        # Step 3: Wait a moment for processing
        logger.info("⏳ Step 3: Waiting for processing...")
        time.sleep(2)

        # Step 4: Check analytics after plan save
        logger.info("📊 Step 4: Checking analytics after plan save")
        updated_analytics = get_analytics()
        logger.info(
            f"✅ Updated analytics loaded: {len(updated_analytics.get('suggestions', []))} suggestions"
        )

        # Step 5: Test manual analytics trigger
        logger.info("🔄 Step 5: Testing manual analytics trigger")
        trigger_result = trigger_analytics()
        logger.info(f"✅ Analytics trigger completed: {trigger_result.get('message')}")

        # Step 6: Check analytics after manual trigger
        logger.info("📊 Step 6: Checking analytics after manual trigger")
        final_analytics = get_analytics()
        logger.info(
            f"✅ Final analytics loaded: {len(final_analytics.get('suggestions', []))} suggestions"
        )

        # Step 7: Test cache behavior
        logger.info("💾 Step 7: Testing cache behavior")
        test_cache_behavior()

        # Step 8: Generate summary
        logger.info("📈 Step 8: Generating test summary")
        generate_test_summary(initial_analytics, updated_analytics, final_analytics)

        logger.info("🎉 Analytics Flow Test completed successfully!")

    except Exception as e:
        logger.error(f"❌ Test failed: {e}")
        raise


def get_analytics(
    limit: int = 5, theme: Optional[str] = None, force_refresh: bool = False
):
    """Get analytics suggestions."""
    params: dict = {"limit": limit}
    if theme:
        params["theme"] = theme
    if force_refresh:
        params["force_refresh"] = "true"

    logger.debug(f"📡 GET /analytics/suggestions with params: {params}")

    response = requests.get(f"{BASE_URL}/analytics/suggestions", params=params)
    response.raise_for_status()

    data = response.json()
    logger.debug(
        f"✅ Analytics response: {len(data.get('suggestions', []))} suggestions"
    )
    return data


def generate_test_plan():
    """Generate a test plan for saving."""
    return {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "theme": "fun 🎉",
        "location": "District 1, Ho Chi Minh City",
        "participants": ["Alice", "Bob", "Charlie"],
        "activities": ["Team Dinner", "Karaoke Night", "Bar Hopping"],
        "total_cost": 450000,
        "phases": [
            {
                "activity": "Team Dinner",
                "location": "Pho 24, District 1",
                "cost": 250000,
            },
            {
                "activity": "Karaoke Night",
                "location": "Karaoke Bar, District 1",
                "cost": 150000,
            },
            {
                "activity": "Bar Hopping",
                "location": "Bui Vien Street, District 1",
                "cost": 50000,
            },
        ],
        "fit_analysis": "Perfect for energetic team members who enjoy social activities",
        "rating": 4.5,
        "contribution_needed": 0,
    }


def save_plan(plan_data):
    """Save a plan to event history."""
    logger.debug(f"📤 POST /event-history with plan: {plan_data['theme']}")

    response = requests.post(f"{BASE_URL}/event-history", json=plan_data)
    response.raise_for_status()

    data = response.json()
    logger.debug(f"✅ Plan saved: {data.get('id')}")
    return data


def trigger_analytics(limit=5, theme=None, reason="test"):
    """Trigger analytics update."""
    trigger_data = {"limit": limit, "theme": theme or "", "reason": reason}

    logger.debug(f"📤 POST /analytics/trigger with data: {trigger_data}")

    response = requests.post(f"{BASE_URL}/analytics/trigger", json=trigger_data)
    response.raise_for_status()

    data = response.json()
    logger.debug(f"✅ Analytics triggered: {data.get('message')}")
    return data


def test_cache_behavior():
    """Test cache behavior with multiple requests."""
    logger.info("🧪 Testing cache behavior...")

    # First request (should generate fresh data)
    start_time = time.time()
    data1 = get_analytics(limit=3, force_refresh=True)
    time1 = time.time() - start_time

    # Second request (should use cache)
    start_time = time.time()
    data2 = get_analytics(limit=3, force_refresh=False)
    time2 = time.time() - start_time

    logger.info(f"⏱️ First request (fresh): {time1:.3f}s")
    logger.info(f"⏱️ Second request (cached): {time2:.3f}s")
    logger.info(f"🚀 Cache speedup: {time1/time2:.1f}x faster")

    # Verify data consistency
    if data1.get("suggestions") == data2.get("suggestions"):
        logger.info("✅ Cache data consistency verified")
    else:
        logger.warning("⚠️ Cache data inconsistency detected")


def generate_test_summary(initial, updated, final):
    """Generate a summary of the test results."""
    logger.info("📊 Test Summary:")
    logger.info("-" * 40)

    initial_count = len(initial.get("suggestions", []))
    updated_count = len(updated.get("suggestions", []))
    final_count = len(final.get("suggestions", []))

    logger.info(f"📈 Suggestions count:")
    logger.info(f"  - Initial: {initial_count}")
    logger.info(f"  - After plan save: {updated_count}")
    logger.info(f"  - After manual trigger: {final_count}")

    if updated_count > initial_count:
        logger.info("✅ Analytics updated after plan save")
    else:
        logger.info("⚠️ Analytics unchanged after plan save")

    if final_count >= updated_count:
        logger.info("✅ Manual trigger successful")
    else:
        logger.info("⚠️ Manual trigger may have failed")

    # Check analytics summary
    summary = final.get("analytics_summary", {})
    logger.info(f"📊 Analytics Summary:")
    logger.info(f"  - Total events: {summary.get('total_events', 0)}")
    logger.info(f"  - Average cost: {summary.get('average_cost', 0):,.0f} VND")
    logger.info(f"  - Most popular theme: {summary.get('most_popular_theme', 'N/A')}")


def test_error_scenarios():
    """Test error scenarios and edge cases."""
    logger.info("🧪 Testing error scenarios...")

    # Test invalid parameters
    try:
        response = requests.get(
            f"{BASE_URL}/analytics/suggestions", params={"limit": -1}
        )
        if response.status_code == 400:
            logger.info("✅ Invalid limit parameter handled correctly")
        else:
            logger.warning(
                f"⚠️ Unexpected response for invalid limit: {response.status_code}"
            )
    except Exception as e:
        logger.error(f"❌ Error testing invalid parameters: {e}")

    # Test non-existent theme
    try:
        data = get_analytics(theme="non_existent_theme")
        if len(data.get("suggestions", [])) == 0:
            logger.info("✅ Non-existent theme handled correctly")
        else:
            logger.warning("⚠️ Unexpected suggestions for non-existent theme")
    except Exception as e:
        logger.error(f"❌ Error testing non-existent theme: {e}")


def main():
    """Main test function."""
    logger.info("🎯 Analytics Flow Logging Test")
    logger.info("=" * 60)

    try:
        # Test the main flow
        test_analytics_flow()

        # Test error scenarios
        test_error_scenarios()

        logger.info("🎉 All tests completed successfully!")
        logger.info("📝 Check 'analytics_flow_test.log' for detailed logs")

    except requests.exceptions.ConnectionError:
        logger.error(
            "❌ Cannot connect to backend server. Make sure it's running on http://localhost:5000"
        )
    except Exception as e:
        logger.error(f"❌ Test failed: {e}")


if __name__ == "__main__":
    main()
