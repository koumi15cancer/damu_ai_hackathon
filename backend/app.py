from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import uuid
from datetime import datetime
from services.ai_service import AIService
from services.maps_service import MapsService
from services.location_service import LocationService
from services.calendar_service import CalendarService
from config import AI_CONFIG
import re
import os
import logging
import time
from typing import Optional, List

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Initialize services
ai_service = AIService()
maps_service = MapsService()
location_service = LocationService()
calendar_service = CalendarService()

# Data storage (in production, use a proper database)
TEAM_MEMBERS_FILE = "team_profiles.json"
EVENT_HISTORY_FILE = "event_history.json"


def load_team_members():
    """Load team members from JSON file."""
    try:
        with open(TEAM_MEMBERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_team_members(team_members):
    """Save team members to JSON file."""
    with open(TEAM_MEMBERS_FILE, "w", encoding="utf-8") as f:
        json.dump(team_members, f, indent=2, ensure_ascii=False)


def load_event_history():
    """Load event history from JSON file."""
    try:
        with open(EVENT_HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_event_history(events):
    """Save event history to JSON file."""
    with open(EVENT_HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(events, f, indent=2, ensure_ascii=False)


@app.route("/generate-plans", methods=["POST"])
def generate_plans():
    """
    Generate 3-5 team bonding event plans based on user inputs, team member profiles, and constraints.

    Request Body:
    {
        "theme": "string", // e.g., "fun 🎉", "chill 🧘"
        "budget_contribution": "string", // e.g., "Yes, up to 150,000 VND"
        "available_members": ["string"], // List of team member names (optional)
        "date_time": "string", // e.g., "2023-12-15 18:00" (optional)
        "location_zone": "string" // e.g., "District 1" (optional)
    }
    """
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Extract request parameters
        theme = data.get("theme", "fun 🎉")
        budget_contribution = data.get("budget_contribution", "No")
        available_members = data.get("available_members", [])
        date_time = data.get("date_time")
        location_zone = data.get("location_zone")
        ai_model = data.get("ai_model")  # New: AI model selection
        plan_generation_mode = data.get(
            "plan_generation_mode", "new"
        )  # New: plan generation mode

        # Load team members
        all_team_members = load_team_members()

        # Filter by available members if specified
        if available_members:
            team_members = [
                member
                for member in all_team_members
                if member["name"] in available_members
            ]
        else:
            team_members = all_team_members

        # Extract budget contribution amount
        contribution_amount = 0
        if "Yes" in budget_contribution:
            # Extract number from string like "Yes, up to 150,000 VND"
            match = re.search(r"(\d+(?:,\d+)*)", budget_contribution)
            if match:
                contribution_amount = int(match.group(1).replace(",", ""))

        # Load event history for analytics-based generation modes
        event_history = []
        if plan_generation_mode in ["reuse", "similar"]:
            event_history = load_event_history()
            logger.info(
                f"📊 Loaded {len(event_history)} events from history for {plan_generation_mode} mode"
            )

        # Generate plans using AI service
        try:
            ai_model = data.get("ai_model")
            plan_generation_mode = data.get("plan_generation_mode", "new")
            plans = ai_service.generate_team_bonding_plans(
                team_profiles=team_members,
                monthly_theme=theme,
                optional_contribution=contribution_amount,
                preferred_date=date_time,
                preferred_location_zone=location_zone,
                ai_model=ai_model,
                plan_generation_mode=plan_generation_mode,
                event_history=event_history,  # Pass event history data
            )
        except Exception as e:
            print(f"AI generation failed: {e}")
            # Fallback to sample plans
            plans = generate_sample_plans(
                team_members, theme, contribution_amount, location_zone
            )

        # Process and validate plans
        processed_plans = []
        for plan in plans:
            processed_plan = process_plan(plan, team_members, contribution_amount)
            if processed_plan:
                processed_plans.append(processed_plan)

        return jsonify(processed_plans)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def process_plan(plan, team_members, contribution_amount):
    """Process and validate a single plan."""
    try:
        # Extract phases from the plan
        phases = []
        total_cost = 0

        # Handle different plan formats
        if "phases" in plan:
            phases_data = plan["phases"]
        elif "activities" in plan:
            phases_data = plan["activities"]
        else:
            # Try to extract phases from the plan structure
            phases_data = []
            for key, value in plan.items():
                if isinstance(value, dict) and "activity" in value:
                    phases_data.append(value)

        for i, phase_data in enumerate(phases_data):
            # Extract phase information
            activity = phase_data.get(
                "activity", phase_data.get("name", "Unknown Activity")
            )
            location = phase_data.get(
                "location", phase_data.get("address", "Unknown Location")
            )
            cost = phase_data.get("cost", 0)

            # Use LocationService to enhance the phase with location data
            enhanced_phase = location_service.enhance_event_phase(
                {
                    "activity": activity,
                    "location": location,
                    "cost": cost,
                    "isIndoor": phase_data.get("isIndoor", True),
                    "isOutdoor": phase_data.get("isOutdoor", False),
                    "isVegetarianFriendly": phase_data.get(
                        "isVegetarianFriendly", False
                    ),
                    "isAlcoholFriendly": phase_data.get("isAlcoholFriendly", False),
                }
            )

            # Determine indicators
            indicators = []
            if phase_data.get("isIndoor", True):
                indicators.append("indoor")
            if phase_data.get("isOutdoor", False):
                indicators.append("outdoor")
            if phase_data.get("isVegetarianFriendly", False):
                indicators.append("vegetarian-friendly")
            if phase_data.get("isAlcoholFriendly", False):
                indicators.append("alcohol-friendly")

            # Add indicators to enhanced phase
            enhanced_phase["indicators"] = indicators

            phases.append(enhanced_phase)
            total_cost += cost

        # Validate locations and get travel information
        location_validation = location_service.validate_event_locations(phases)
        travel_summary = location_service.get_travel_summary(phases)

        # Calculate contribution needed
        contribution_needed = max(0, total_cost - 300000)

        # Generate fit analysis
        fit_analysis = generate_fit_analysis(plan, team_members)

        # Get rating
        rating = plan.get("rating", 3)

        return {
            "phases": phases,
            "total_cost": total_cost,
            "contribution_needed": contribution_needed,
            "fit_analysis": fit_analysis,
            "rating": rating,
            "location_validation": location_validation,
            "travel_summary": travel_summary,
        }

    except Exception as e:
        logger.error(f"Error processing plan: {e}")
        return None


def generate_map_link(location):
    """Generate Google Maps link for a location."""
    try:
        # Use the enhanced maps service to generate map link
        return maps_service.generate_map_link(location)
    except Exception as e:
        print(f"Error generating map link for '{location}': {e}")
        # Fallback to search query
        encoded_location = location.replace(" ", "+")
        return f"https://www.google.com/maps/search/{encoded_location}"


def generate_fit_analysis(plan, team_members):
    """Generate fit analysis for the plan."""
    try:
        # Extract best for members if available
        best_for = plan.get("bestFor", [])
        if best_for:
            return f"Suits team members: {', '.join(best_for)}"

        # Generate based on theme and preferences
        theme = plan.get("theme", "general")
        if theme == "fun 🎉":
            return "Perfect for energetic team members who enjoy social activities"
        elif theme == "chill 🧘":
            return "Ideal for team members who prefer relaxed, low-key gatherings"
        else:
            return "Suitable for most team members with balanced preferences"

    except:
        return "Suitable for team bonding activities"


def generate_sample_plans(team_members, theme, contribution_amount, location_zone):
    """Generate sample plans when AI is not available."""
    return [
        {
            "phases": [
                {
                    "activity": "Hotpot Dinner",
                    "location": "123 Le Lai, District 1, Ho Chi Minh City",
                    "map_link": "https://maps.google.com/?q=123+Le+Lai+District+1",
                    "cost": 250000,
                    "indicators": ["indoor", "vegetarian-friendly"],
                },
                {
                    "activity": "Karaoke Session",
                    "location": "456 Le Loi, District 1, Ho Chi Minh City",
                    "map_link": "https://maps.google.com/?q=456+Le+Loi+District+1",
                    "cost": 150000,
                    "indicators": ["indoor"],
                },
            ],
            "total_cost": 400000,
            "contribution_needed": 100000,
            "fit_analysis": "Suits team members in District 1",
            "rating": 4,
        },
        {
            "phases": [
                {
                    "activity": "Cafe Hopping",
                    "location": "789 Dong Khoi, District 1, Ho Chi Minh City",
                    "map_link": "https://maps.google.com/?q=789+Dong+Khoi+District+1",
                    "cost": 200000,
                    "indicators": ["indoor", "vegetarian-friendly"],
                }
            ],
            "total_cost": 200000,
            "contribution_needed": 0,
            "fit_analysis": "Perfect for chill team members",
            "rating": 3,
        },
    ]


@app.route("/team-members", methods=["GET"])
def get_team_members():
    """
    Retrieve the list of all team member profiles.

    Response:
    [
        {
            "id": "string",
            "name": "string",
            "location": "string",
            "preferences": ["string"],
            "vibe": "string"
        }
    ]
    """
    try:
        team_members = load_team_members()
        return jsonify(team_members)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/team-members", methods=["POST"])
def create_team_member():
    """
    Create a new team member profile.

    Request Body:
    {
        "name": "string",
        "location": "string",
        "preferences": ["string"],
        "vibe": "string"
    }
    """
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Validate required fields
        required_fields = ["name", "location", "preferences", "vibe"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        # Load existing team members
        team_members = load_team_members()

        # Generate new ID
        new_id = str(uuid.uuid4())

        # Create new team member
        new_member = {
            "id": new_id,
            "name": data["name"],
            "location": data["location"],
            "preferences": data["preferences"],
            "vibe": data["vibe"],
        }

        # Add to list and save
        team_members.append(new_member)
        save_team_members(team_members)

        return jsonify(new_member), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/team-members/<member_id>", methods=["PUT"])
def update_team_member(member_id):
    """
    Update an existing team member profile.

    Request Body:
    {
        "name": "string",
        "location": "string",
        "preferences": ["string"],
        "vibe": "string"
    }
    """
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Load existing team members
        team_members = load_team_members()

        # Find the member to update
        member_index = None
        for i, member in enumerate(team_members):
            if member["id"] == member_id:
                member_index = i
                break

        if member_index is None:
            return jsonify({"error": "Team member not found"}), 404

        # Update member data
        team_members[member_index].update(
            {
                "name": data.get("name", team_members[member_index]["name"]),
                "location": data.get(
                    "location", team_members[member_index]["location"]
                ),
                "preferences": data.get(
                    "preferences", team_members[member_index]["preferences"]
                ),
                "vibe": data.get("vibe", team_members[member_index]["vibe"]),
            }
        )

        # Save updated data
        save_team_members(team_members)

        return jsonify(team_members[member_index])

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/team-members/<member_id>", methods=["DELETE"])
def delete_team_member(member_id):
    """
    Delete a team member profile.

    Response:
    {
        "message": "Team member deleted successfully"
    }
    """
    try:
        # Load existing team members
        team_members = load_team_members()

        # Find the member to delete
        member_index = None
        for i, member in enumerate(team_members):
            if member["id"] == member_id:
                member_index = i
                break

        if member_index is None:
            return jsonify({"error": "Team member not found"}), 404

        # Remove member
        team_members.pop(member_index)

        # Save updated data
        save_team_members(team_members)

        return jsonify({"message": "Team member deleted successfully"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/event-history", methods=["GET"])
def get_event_history():
    """
    Retrieve the list of all saved events.

    Response:
    [
        {
            "id": number,
            "date": "string",
            "theme": "string",
            "location": "string",
            "participants": ["string"],
            "activities": ["string"],
            "total_cost": number,
            "phases": [...],
            "fit_analysis": "string",
            "rating": number,
            "contribution_needed": number
        }
    ]
    """
    try:
        events = load_event_history()
        return jsonify(events)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/event-history", methods=["POST"])
def save_event():
    """Save a new event to the history."""
    start_time = time.time()
    request_id = f"save_{int(start_time * 1000)}"

    logger.info(f"[{request_id}] 🚀 Event save request started")

    try:
        data = request.get_json()

        if not data:
            logger.error(f"[{request_id}] ❌ No data provided in request")
            return jsonify({"error": "No data provided"}), 400

        logger.info(
            f"[{request_id}] 📋 Event data received: theme={data.get('theme')}, activities={len(data.get('activities', []))}, cost={data.get('total_cost')}"
        )

        # Validate required fields
        required_fields = ["date", "theme", "activities", "total_cost"]
        missing_fields = [field for field in required_fields if not data.get(field)]

        if missing_fields:
            logger.error(f"[{request_id}] ❌ Missing required fields: {missing_fields}")
            return jsonify({"error": f"Missing required fields: {missing_fields}"}), 400

        # Check for duplicate events (same date, theme, and activities)
        logger.debug(f"[{request_id}] 🔍 Checking for duplicate events")
        events = load_event_history()

        # Create a unique identifier for the event
        event_signature = {
            "date": data["date"],
            "theme": data["theme"],
            "activities": sorted(data["activities"]),
            "total_cost": data["total_cost"],
        }

        # Check if similar event already exists
        for existing_event in events:
            existing_signature = {
                "date": existing_event.get("date"),
                "theme": existing_event.get("theme"),
                "activities": sorted(existing_event.get("activities", [])),
                "total_cost": existing_event.get("total_cost"),
            }

            if event_signature == existing_signature:
                logger.warning(f"[{request_id}] ⚠️ Duplicate event detected")
                return jsonify({"error": "Similar event already exists"}), 409

        logger.info(f"[{request_id}] ✅ No duplicates found, proceeding with save")

        # Add metadata
        event_data = {
            "id": str(uuid.uuid4()),
            "created_at": datetime.now().isoformat(),
            **data,
        }

        # Save to file
        logger.debug(f"[{request_id}] 💾 Saving event to history file")
        events.append(event_data)

        with open("event_history.json", "w", encoding="utf-8") as f:
            json.dump(events, f, indent=2, ensure_ascii=False)

        logger.info(f"[{request_id}] ✅ Event saved successfully: {event_data['id']}")

        # Clear analytics cache to trigger refresh
        logger.info(f"[{request_id}] 🧹 Clearing analytics cache for refresh")
        clear_analytics_cache()

        response_time = time.time() - start_time
        logger.info(
            f"[{request_id}] 🎉 Event save completed successfully (time={response_time:.3f}s)"
        )

        return (
            jsonify({"message": "Event saved successfully", "id": event_data["id"]}),
            201,
        )

    except Exception as e:
        response_time = time.time() - start_time
        logger.error(
            f"[{request_id}] ❌ Error saving event: {e} (time={response_time:.3f}s)"
        )
        return jsonify({"error": str(e)}), 500


@app.route("/event-history/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    """
    Delete an event from the history.

    Response:
    {
        "message": "Event deleted successfully"
    }
    """
    try:
        # Load existing events
        events = load_event_history()

        # Find the event to delete
        event_index = None
        for i, event in enumerate(events):
            if event.get("id") == event_id:
                event_index = i
                break

        if event_index is None:
            return jsonify({"error": "Event not found"}), 404

        # Remove event
        events.pop(event_index)

        # Save updated data
        save_event_history(events)

        return jsonify({"message": "Event deleted successfully"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/event-history/<int:event_id>/rate", methods=["POST"])
def rate_event(event_id):
    """
    Rate an event (one rating per member per event).

    Request Body:
    {
        "member_name": "string",
        "rating": number,
        "feedback": "string",
        "categories": {
            "fun": number,
            "organization": number,
            "value": number,
            "overall": number
        }
    }
    """
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Load existing events
        events = load_event_history()

        # Find the event to rate
        event_index = None
        for i, event in enumerate(events):
            if event.get("id") == event_id:
                event_index = i
                break

        if event_index is None:
            return jsonify({"error": "Event not found"}), 404

        event = events[event_index]
        member_name = data.get("member_name", "")

        # Validate member name is in participants list
        if member_name not in event.get("participants", []):
            return jsonify({"error": "Member not found in event participants"}), 400

        # Check if member has already rated this event
        if "member_ratings" not in event:
            event["member_ratings"] = []

        for rating in event["member_ratings"]:
            if rating.get("member_name") == member_name:
                return jsonify({"error": "Member has already rated this event"}), 409

        # Create new rating
        new_rating = {
            "member_name": member_name,
            "rating": data.get("rating", 0),
            "feedback": data.get("feedback", ""),
            "categories": data.get(
                "categories", {"fun": 0, "organization": 0, "value": 0, "overall": 0}
            ),
            "submitted_at": data.get("submitted_at", datetime.now().isoformat()),
        }

        # Add rating to event
        event["member_ratings"].append(new_rating)

        # Calculate average rating from all member ratings (preserve AI rating)
        if event["member_ratings"]:
            total_rating = sum(r["rating"] for r in event["member_ratings"])
            member_average = round(total_rating / len(event["member_ratings"]), 1)
            # Keep the original AI rating in 'ai_rating' field
            if "ai_rating" not in event:
                event["ai_rating"] = event.get("rating", 3)
            # Update 'rating' field with member average (for backward compatibility)
            event["rating"] = member_average
        else:
            # If no member ratings, keep AI rating
            if "ai_rating" not in event:
                event["ai_rating"] = event.get("rating", 3)

        # Save updated events
        save_event_history(events)

        return (
            jsonify(
                {
                    "message": "Rating submitted successfully",
                    "rating": new_rating,
                    "member_average": event.get("rating", 0),
                    "ai_rating": event.get("ai_rating", 0),
                }
            ),
            201,
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return jsonify(
        {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "ai_provider": (
                ai_service.provider_name
                if hasattr(ai_service, "provider_name")
                else "unknown"
            ),
        }
    )


@app.route("/analytics/suggestions", methods=["GET"])
def get_activity_suggestions():
    """
    Analyze recent saved activities and generate AI-powered suggestions.

    Query Parameters:
    - limit: Number of recent events to analyze (default: 10)
    - theme: Filter by specific theme (optional)
    - force_refresh: Force refresh analytics (optional, default: false)

    Response:
    {
        "suggestions": [
            {
                "type": "theme_preference",
                "title": "string",
                "description": "string",
                "confidence": number,
                "data_points": number
            }
        ],
        "analytics_summary": {
            "total_events": number,
            "most_popular_theme": "string",
            "average_cost": number,
            "common_activities": ["string"],
            "rating_trends": "string"
        }
    }
    """
    start_time = time.time()
    request_id = f"analytics_{int(start_time * 1000)}"

    logger.info(f"[{request_id}] 🚀 Analytics request started")

    try:
        # Get query parameters
        limit = request.args.get("limit", 10, type=int)
        theme_filter = request.args.get("theme", None)
        force_refresh = request.args.get("force_refresh", "false").lower() == "true"

        logger.info(
            f"[{request_id}] 📋 Request parameters: limit={limit}, theme={theme_filter}, force_refresh={force_refresh}"
        )

        # Check if we should use cached data
        if not force_refresh:
            logger.info(f"[{request_id}] 🔍 Checking cache for analytics data")
            cached_data = get_cached_analytics(limit, theme_filter)
            if cached_data:
                response_time = time.time() - start_time
                logger.info(
                    f"[{request_id}] ✅ Returning cached analytics data (response_time={response_time:.3f}s)"
                )
                return jsonify(cached_data)
            else:
                logger.info(
                    f"[{request_id}] ❌ No cached data found, generating fresh analytics"
                )

        # Load recent events
        logger.info(f"[{request_id}] 📂 Loading event history")
        events = load_event_history()
        logger.info(f"[{request_id}] 📊 Loaded {len(events)} total events from history")

        # Sort by date (most recent first) and apply limit
        events.sort(key=lambda x: x.get("date", ""), reverse=True)
        recent_events = events[:limit]
        logger.info(
            f"[{request_id}] 📅 Selected {len(recent_events)} recent events (limit={limit})"
        )

        # Apply theme filter if specified
        if theme_filter:
            original_count = len(recent_events)
            recent_events = [e for e in recent_events if e.get("theme") == theme_filter]
            logger.info(
                f"[{request_id}] 🎨 Theme filter applied: {original_count} -> {len(recent_events)} events"
            )

        if not recent_events:
            logger.warning(f"[{request_id}] ⚠️ No recent events found for analysis")
            return jsonify(
                {
                    "suggestions": [],
                    "analytics_summary": {
                        "total_events": 0,
                        "message": "No recent events found for analysis",
                    },
                }
            )

        # Prepare analytics data for AI analysis
        logger.info(f"[{request_id}] 🔧 Preparing analytics data for AI analysis")
        analytics_data = {
            "events": recent_events,
            "total_events": len(recent_events),
            "themes": [e.get("theme") for e in recent_events],
            "activities": [
                activity for e in recent_events for activity in e.get("activities", [])
            ],
            "costs": [e.get("total_cost", 0) for e in recent_events],
            "ratings": [e.get("rating", 0) for e in recent_events if e.get("rating")],
            "locations": [e.get("location") for e in recent_events],
            "participant_counts": [
                len(e.get("participants", [])) for e in recent_events
            ],
        }

        logger.info(
            f"[{request_id}] 📈 Analytics data prepared: themes={len(set(analytics_data['themes']))}, activities={len(analytics_data['activities'])}, ratings={len(analytics_data['ratings'])}"
        )

        # Generate AI-powered suggestions
        logger.info(
            f"[{request_id}] 🤖 Starting AI-powered activity suggestions generation"
        )
        start_time = time.time()
        suggestions = generate_activity_suggestions(analytics_data)
        ai_time = time.time() - start_time
        logger.info(
            f"✅ AI suggestions generated: {len(suggestions)} suggestions in {ai_time:.3f}s"
        )

        # Create analytics summary
        logger.info(f"[{request_id}] 📊 Creating analytics summary")
        analytics_summary = create_analytics_summary(analytics_data)
        logger.info(
            f"✅ Analytics summary created: total_events={analytics_summary['total_events']}, avg_cost={analytics_summary['average_cost']}"
        )

        # Save analytics data
        logger.info(f"[{request_id}] 💾 Saving analytics data to history")
        save_analytics_data(analytics_data, suggestions, analytics_summary)

        # Cache the result
        result = {"suggestions": suggestions, "analytics_summary": analytics_summary}
        logger.info(f"[{request_id}] 💾 Caching analytics result")
        cache_analytics_result(limit, result, theme_filter)

        response_time = time.time() - start_time
        logger.info(
            f"[{request_id}] 🎉 Analytics request completed successfully (total_time={response_time:.3f}s)"
        )

        return jsonify(result)

    except Exception as e:
        response_time = time.time() - start_time
        logger.error(
            f"[{request_id}] ❌ Error generating suggestions: {e} (time={response_time:.3f}s)"
        )
        return jsonify({"error": str(e)}), 500


@app.route("/analytics/trigger", methods=["POST"])
def trigger_analytics_update():
    """
    Trigger analytics update for specific parameters.

    Request Body:
    {
        "limit": 10,
        "theme": "fun",
        "reason": "plan_saved|tab_switch|manual"
    }
    """
    start_time = time.time()
    request_id = f"trigger_{int(start_time * 1000)}"

    logger.info(f"[{request_id}] 🚀 Analytics trigger request started")

    try:
        data = request.get_json() or {}
        limit = data.get("limit", 10)
        theme = data.get("theme", "")
        reason = data.get("reason", "manual")

        logger.info(
            f"[{request_id}] 📋 Trigger parameters: limit={limit}, theme={theme}, reason={reason}"
        )

        # Clear cache for these parameters
        logger.info(f"[{request_id}] 🧹 Clearing analytics cache")
        clear_analytics_cache(limit, theme)

        response_time = time.time() - start_time
        logger.info(
            f"[{request_id}] ✅ Analytics trigger completed successfully (time={response_time:.3f}s)"
        )

        # Return success response
        return jsonify(
            {
                "message": "Analytics update triggered successfully",
                "cache_cleared": True,
                "reason": reason,
                "request_id": request_id,
            }
        )

    except Exception as e:
        response_time = time.time() - start_time
        logger.error(
            f"[{request_id}] ❌ Error triggering analytics update: {e} (time={response_time:.3f}s)"
        )
        return jsonify({"error": str(e)}), 500


def get_cached_analytics(
    limit: int, theme_filter: Optional[str] = None
) -> Optional[dict]:
    """Get cached analytics data if available and fresh."""
    try:
        tmp_dir = "tmp"
        cache_key = f"analytics_{limit}_{theme_filter or 'all'}"
        cache_file = os.path.join(tmp_dir, f"cache_{cache_key}.json")

        logger.debug(f"🔍 Checking cache file: {cache_file}")

        if os.path.exists(cache_file):
            # Check if cache is less than 30 minutes old
            cache_age = time.time() - os.path.getmtime(cache_file)
            logger.debug(f"🕒 Cache age: {cache_age:.1f}s (max: 1800s)")

            if cache_age < 30 * 60:  # 30 minutes
                with open(cache_file, "r", encoding="utf-8") as f:
                    cached_data = json.load(f)
                logger.info(
                    f"✅ Using cached analytics data: {cache_file} (age: {cache_age:.1f}s)"
                )
                return cached_data
            else:
                logger.info(f"⏰ Cache expired: {cache_file} (age: {cache_age:.1f}s)")
        else:
            logger.debug(f"❌ Cache file not found: {cache_file}")

        return None
    except Exception as e:
        logger.error(f"❌ Error reading analytics cache: {e}")
        return None


def cache_analytics_result(
    limit: int, result: dict, theme_filter: Optional[str] = None
):
    """Cache analytics result for future use."""
    try:
        # Ensure tmp directory exists
        tmp_dir = "tmp"
        os.makedirs(tmp_dir, exist_ok=True)

        cache_key = f"analytics_{limit}_{theme_filter or 'all'}"
        cache_file = os.path.join(tmp_dir, f"cache_{cache_key}.json")

        logger.debug(f"💾 Caching analytics result: {cache_file}")

        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        logger.info(f"✅ Analytics result cached successfully: {cache_file}")
    except Exception as e:
        logger.error(f"❌ Error caching analytics result: {e}")


def clear_analytics_cache(
    limit: Optional[int] = None, theme_filter: Optional[str] = None
):
    """Clear analytics cache for specific parameters or all."""
    try:
        tmp_dir = "tmp"
        if not os.path.exists(tmp_dir):
            logger.debug(
                f"📁 Cache directory {tmp_dir} does not exist, nothing to clear"
            )
            return

        if limit is None and theme_filter is None:
            # Clear all cache files
            logger.info("🧹 Clearing all analytics cache files")
            cleared_count = 0
            for file in os.listdir(tmp_dir):
                if file.startswith("cache_analytics_") and file.endswith(".json"):
                    file_path = os.path.join(tmp_dir, file)
                    os.remove(file_path)
                    cleared_count += 1
                    logger.debug(f"🗑️ Cleared cache file: {file}")
            logger.info(f"✅ Cleared {cleared_count} analytics cache files")
        else:
            # Clear specific cache
            cache_key = f"analytics_{limit or 'all'}_{theme_filter or 'all'}"
            cache_file = os.path.join(tmp_dir, f"cache_{cache_key}.json")
            if os.path.exists(cache_file):
                os.remove(cache_file)
                logger.info(f"✅ Cleared specific cache file: {cache_file}")
            else:
                logger.debug(f"⚠️ Cache file not found for clearing: {cache_file}")
    except Exception as e:
        logger.error(f"❌ Error clearing analytics cache: {e}")


def load_analytics_data():
    """Load analytics data from JSON file."""
    try:
        with open("analytics_data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"analytics_history": [], "suggestions_history": []}
    except Exception as e:
        logger.error(f"Error loading analytics data: {e}")
        return {"analytics_history": [], "suggestions_history": []}


def save_analytics_data(analytics_data, suggestions, analytics_summary):
    """Save analytics data to JSON file."""
    try:
        existing_data = load_analytics_data()

        # Add new analytics entry
        new_entry = {
            "timestamp": datetime.now().isoformat(),
            "analytics_data": analytics_data,
            "suggestions": suggestions,
            "analytics_summary": analytics_summary,
        }

        existing_data["analytics_history"].append(new_entry)

        # Keep only last 50 entries to prevent file from growing too large
        if len(existing_data["analytics_history"]) > 50:
            existing_data["analytics_history"] = existing_data["analytics_history"][
                -50:
            ]

        with open("analytics_data.json", "w", encoding="utf-8") as f:
            json.dump(existing_data, f, indent=2, ensure_ascii=False)

    except Exception as e:
        logger.error(f"Error saving analytics data: {e}")


def create_analytics_summary(analytics_data):
    """Create a summary of analytics data."""
    try:
        events = analytics_data["events"]
        themes = analytics_data["themes"]
        activities = analytics_data["activities"]
        costs = analytics_data["costs"]
        ratings = analytics_data["ratings"]

        # Calculate statistics
        theme_counts = {}
        for theme in themes:
            theme_counts[theme] = theme_counts.get(theme, 0) + 1

        most_popular_theme = (
            max(theme_counts.items(), key=lambda x: x[1])[0]
            if theme_counts
            else "No data"
        )
        average_cost = sum(costs) / len(costs) if costs else 0

        # Find common activities
        activity_counts = {}
        for activity in activities:
            activity_counts[activity] = activity_counts.get(activity, 0) + 1

        common_activities = sorted(
            activity_counts.items(), key=lambda x: x[1], reverse=True
        )[:5]
        common_activities = [activity for activity, count in common_activities]

        # Analyze rating trends
        if ratings:
            avg_rating = sum(ratings) / len(ratings)
            if avg_rating >= 4.0:
                rating_trend = "Excellent - High satisfaction with recent events"
            elif avg_rating >= 3.0:
                rating_trend = "Good - Generally positive feedback"
            else:
                rating_trend = "Needs improvement - Consider different activities"
        else:
            rating_trend = "No rating data available"

        return {
            "total_events": len(events),
            "most_popular_theme": most_popular_theme,
            "average_cost": round(average_cost, 2),
            "common_activities": common_activities,
            "rating_trends": rating_trend,
            "theme_distribution": theme_counts,
        }

    except Exception as e:
        logger.error(f"Error creating analytics summary: {e}")
        return {"error": str(e)}


def generate_activity_suggestions(analytics_data: dict) -> List[dict]:
    """Generate AI-powered activity suggestions based on analytics data."""
    logger.info("🤖 Starting AI-powered activity suggestions generation")

    try:
        # Initialize AI service
        logger.debug("🔧 Initializing AI service for suggestions")
        ai_service = AIService()

        if not ai_service.current_provider:
            logger.warning("⚠️ No AI provider available, using fallback suggestions")
            return generate_fallback_suggestions(analytics_data)

        logger.info(f"✅ Using AI provider: {ai_service.provider_name}")

        # Prepare prompt for AI analysis
        logger.debug("📝 Preparing AI prompt for analytics")
        prompt = create_analytics_prompt(analytics_data)
        logger.debug(f"📝 AI prompt prepared (length: {len(prompt)} characters)")

        # Generate AI response
        logger.info("🔄 Sending analytics data to AI for analysis")
        start_time = time.time()

        response = ai_service.generate_response(
            prompt=prompt,
            system_prompt="You are an expert team bonding analyst. Analyze the provided data and give actionable suggestions.",
            temperature=0.7,
            max_tokens=1000,
        )

        ai_time = time.time() - start_time
        logger.info(
            f"✅ AI response received in {ai_time:.3f}s (length: {len(response)} characters)"
        )

        # Parse AI response into structured suggestions
        logger.debug("🔍 Parsing AI response into structured suggestions")
        suggestions = parse_ai_suggestions(response, analytics_data)
        logger.info(f"✅ Parsed {len(suggestions)} suggestions from AI response")

        return suggestions

    except Exception as e:
        logger.error(f"❌ Error generating AI suggestions: {e}")
        logger.info("🔄 Falling back to rule-based suggestions")
        return generate_fallback_suggestions(analytics_data)


def create_analytics_prompt(analytics_data: dict) -> str:
    """Create a comprehensive prompt for AI analytics analysis."""
    logger.debug("📝 Creating analytics prompt")

    events = analytics_data.get("events", [])
    themes = analytics_data.get("themes", [])
    activities = analytics_data.get("activities", [])
    costs = analytics_data.get("costs", [])
    ratings = analytics_data.get("ratings", [])

    # Calculate statistics
    theme_counts = {}
    for theme in themes:
        theme_counts[theme] = theme_counts.get(theme, 0) + 1

    activity_counts = {}
    for activity in activities:
        activity_counts[activity] = activity_counts.get(activity, 0) + 1

    avg_cost = sum(costs) / len(costs) if costs else 0
    avg_rating = sum(ratings) / len(ratings) if ratings else 0

    logger.debug(
        f"📊 Analytics statistics: themes={len(set(themes))}, activities={len(set(activities))}, avg_cost={avg_cost:.0f}, avg_rating={avg_rating:.1f}"
    )

    prompt = f"""
Analyze this team bonding event data and provide 3-5 actionable suggestions for improving future events:

EVENT DATA SUMMARY:
- Total events analyzed: {len(events)}
- Most popular themes: {', '.join([f'{theme} ({count})' for theme, count in sorted(theme_counts.items(), key=lambda x: x[1], reverse=True)[:3]])}
- Most common activities: {', '.join([f'{activity} ({count})' for activity, count in sorted(activity_counts.items(), key=lambda x: x[1], reverse=True)[:5]])}
- Average cost per event: {avg_cost:,.0f} VND
- Average rating: {avg_rating:.1f}/5

RECENT EVENTS:
{chr(10).join([f"- {e.get('date', 'Unknown date')}: {e.get('theme', 'Unknown theme')} theme, {len(e.get('activities', []))} activities, {e.get('total_cost', 0):,} VND, Rating: {e.get('rating', 'N/A')}/5" for e in events[:5]])}

Please provide suggestions in this JSON format:
{{
  "suggestions": [
    {{
      "type": "theme_preference|cost_optimization|activity_variety|timing|location",
      "title": "Suggestion title",
      "description": "Detailed explanation with actionable steps",
      "confidence": 0.85,
      "data_points": 5,
      "impact": "high|medium|low"
    }}
  ]
}}

Focus on:
1. Theme preferences and patterns
2. Cost optimization opportunities
3. Activity variety and engagement
4. Timing and scheduling insights
5. Location and logistics improvements

Make suggestions specific, actionable, and data-driven.
"""

    logger.debug(f"📝 Analytics prompt created (length: {len(prompt)} characters)")
    return prompt


def parse_ai_suggestions(ai_response: str, analytics_data: dict) -> List[dict]:
    """Parse AI response into structured suggestions."""
    logger.debug("🔍 Parsing AI suggestions response")

    try:
        # Try to extract JSON from the response
        import re

        json_match = re.search(r"```json\s*(.*?)\s*```", ai_response, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
            logger.debug("✅ Found JSON in markdown code blocks")
        else:
            # Try to find JSON in the response
            json_start = ai_response.find("{")
            json_end = ai_response.rfind("}") + 1
            if json_start != -1 and json_end != 0:
                json_str = ai_response[json_start:json_end]
                logger.debug("✅ Found JSON in response body")
            else:
                logger.warning("⚠️ No JSON found in AI response, using fallback parsing")
                return parse_fallback_suggestions(ai_response, analytics_data)

        # Parse JSON
        parsed_data = json.loads(json_str)
        suggestions = parsed_data.get("suggestions", [])

        logger.info(
            f"✅ Successfully parsed {len(suggestions)} suggestions from AI response"
        )

        # Validate and enhance suggestions
        validated_suggestions = []
        for i, suggestion in enumerate(suggestions):
            validated_suggestion = {
                "type": suggestion.get("type", "general"),
                "title": suggestion.get("title", f"Suggestion {i+1}"),
                "description": suggestion.get("description", ""),
                "confidence": min(max(suggestion.get("confidence", 0.5), 0), 1),
                "data_points": suggestion.get(
                    "data_points", len(analytics_data.get("events", []))
                ),
                "impact": suggestion.get("impact", "medium"),
            }
            validated_suggestions.append(validated_suggestion)
            logger.debug(
                f"✅ Validated suggestion {i+1}: {validated_suggestion['title']}"
            )

        return validated_suggestions

    except Exception as e:
        logger.error(f"❌ Error parsing AI suggestions: {e}")
        logger.info("🔄 Falling back to rule-based parsing")
        return parse_fallback_suggestions(ai_response, analytics_data)


def parse_fallback_suggestions(ai_response: str, analytics_data: dict) -> List[dict]:
    """Fallback parsing for AI suggestions when JSON parsing fails."""
    logger.debug("🔄 Using fallback suggestion parsing")

    suggestions = []

    # Extract suggestions from text response
    lines = ai_response.split("\n")
    current_suggestion = {}

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Look for numbered suggestions
        if re.match(r"^\d+\.", line):
            if current_suggestion:
                suggestions.append(current_suggestion)
            current_suggestion = {
                "type": "general",
                "title": line.split(".", 1)[1].strip(),
                "description": "",
                "confidence": 0.6,
                "data_points": len(analytics_data.get("events", [])),
                "impact": "medium",
            }
        elif current_suggestion and line:
            current_suggestion["description"] += line + " "

    # Add the last suggestion
    if current_suggestion:
        suggestions.append(current_suggestion)

    logger.info(f"✅ Fallback parsing completed: {len(suggestions)} suggestions")
    return suggestions


def generate_fallback_suggestions(analytics_data: dict) -> List[dict]:
    """Generate rule-based suggestions when AI is unavailable."""
    logger.info("🔄 Generating rule-based fallback suggestions")

    events = analytics_data.get("events", [])
    themes = analytics_data.get("themes", [])
    costs = analytics_data.get("costs", [])
    ratings = analytics_data.get("ratings", [])

    suggestions = []

    # Theme preference suggestion
    if themes:
        theme_counts = {}
        for theme in themes:
            theme_counts[theme] = theme_counts.get(theme, 0) + 1

        most_popular_theme = max(theme_counts.items(), key=lambda x: x[1])
        suggestions.append(
            {
                "type": "theme_preference",
                "title": f"Consider {most_popular_theme[0]} theme more often",
                "description": f"Your team has chosen {most_popular_theme[0]} theme {most_popular_theme[1]} times, indicating a strong preference for this type of activity.",
                "confidence": 0.8,
                "data_points": len(events),
                "impact": "high",
            }
        )

    # Cost optimization suggestion
    if costs:
        avg_cost = sum(costs) / len(costs)
        if avg_cost > 400000:  # High cost threshold
            suggestions.append(
                {
                    "type": "cost_optimization",
                    "title": "Consider more budget-friendly options",
                    "description": f"Your average event cost is {avg_cost:,.0f} VND. Consider exploring more affordable venues or activities to stay within budget.",
                    "confidence": 0.7,
                    "data_points": len(costs),
                    "impact": "medium",
                }
            )

    # Rating improvement suggestion
    if ratings:
        avg_rating = sum(ratings) / len(ratings)
        if avg_rating < 4.0:
            suggestions.append(
                {
                    "type": "activity_variety",
                    "title": "Explore new activity types",
                    "description": f"Your average rating is {avg_rating:.1f}/5. Try different activity types or venues to improve team satisfaction.",
                    "confidence": 0.6,
                    "data_points": len(ratings),
                    "impact": "high",
                }
            )

    # General suggestion
    suggestions.append(
        {
            "type": "general",
            "title": "Plan events in advance",
            "description": "Based on your event history, planning events 1-2 weeks in advance tends to result in better attendance and satisfaction.",
            "confidence": 0.5,
            "data_points": len(events),
            "impact": "medium",
        }
    )

    logger.info(f"✅ Generated {len(suggestions)} fallback suggestions")
    return suggestions


@app.route("/ai-models", methods=["GET"])
def get_ai_models():
    """Get available AI models."""
    try:
        available_providers = ai_service.get_available_providers()
        provider_display_names = {
            "openai": "OpenAI GPT-4",
            "google": "Google Gemini",
            "anthropic": "Anthropic Claude",
        }
        models = [provider_display_names.get(p, p.title()) for p in available_providers]
        return jsonify({"models": models})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
