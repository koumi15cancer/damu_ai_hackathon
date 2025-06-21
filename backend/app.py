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
TEAM_MEMBERS_FILE = 'team_profiles.json'
EVENT_HISTORY_FILE = 'event_history.json'

def load_team_members():
    """Load team members from JSON file."""
    try:
        with open(TEAM_MEMBERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_team_members(team_members):
    """Save team members to JSON file."""
    with open(TEAM_MEMBERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(team_members, f, indent=2, ensure_ascii=False)

def load_event_history():
    """Load event history from JSON file."""
    try:
        with open(EVENT_HISTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_event_history(events):
    """Save event history to JSON file."""
    with open(EVENT_HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(events, f, indent=2, ensure_ascii=False)

@app.route('/generate-plans', methods=['POST'])
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
            return jsonify({'error': 'No data provided'}), 400
        
        # Extract request parameters
        theme = data.get('theme', 'fun 🎉')
        budget_contribution = data.get('budget_contribution', 'No')
        available_members = data.get('available_members', [])
        date_time = data.get('date_time')
        location_zone = data.get('location_zone')
        
        # Load team members
        all_team_members = load_team_members()
        
        # Filter by available members if specified
        if available_members:
            team_members = [member for member in all_team_members if member['name'] in available_members]
        else:
            team_members = all_team_members
        
        # Extract budget contribution amount
        contribution_amount = 0
        if 'Yes' in budget_contribution:
            # Extract number from string like "Yes, up to 150,000 VND"
            match = re.search(r'(\d+(?:,\d+)*)', budget_contribution)
            if match:
                contribution_amount = int(match.group(1).replace(',', ''))
        
        # Generate plans using AI service
        try:
            plans = ai_service.generate_team_bonding_plans(
                team_profiles=team_members,
                monthly_theme=theme,
                optional_contribution=contribution_amount,
                preferred_date=date_time,
                preferred_location_zone=location_zone
            )
        except Exception as e:
            print(f"AI generation failed: {e}")
            # Fallback to sample plans
            plans = generate_sample_plans(team_members, theme, contribution_amount, location_zone)
        
        # Process and validate plans
        processed_plans = []
        for plan in plans:
            processed_plan = process_plan(plan, team_members, contribution_amount)
            if processed_plan:
                processed_plans.append(processed_plan)
        
        return jsonify(processed_plans)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def process_plan(plan, team_members, contribution_amount):
    """Process and validate a single plan."""
    try:
        # Extract phases from the plan
        phases = []
        total_cost = 0
        
        # Handle different plan formats
        if 'phases' in plan:
            phases_data = plan['phases']
        elif 'activities' in plan:
            phases_data = plan['activities']
        else:
            # Try to extract phases from the plan structure
            phases_data = []
            for key, value in plan.items():
                if isinstance(value, dict) and 'activity' in value:
                    phases_data.append(value)
        
        for i, phase_data in enumerate(phases_data):
            # Extract phase information
            activity = phase_data.get('activity', phase_data.get('name', 'Unknown Activity'))
            location = phase_data.get('location', phase_data.get('address', 'Unknown Location'))
            cost = phase_data.get('cost', 0)
            
            # Use LocationService to enhance the phase with location data
            enhanced_phase = location_service.enhance_event_phase({
                'activity': activity,
                'location': location,
                'cost': cost,
                'isIndoor': phase_data.get('isIndoor', True),
                'isOutdoor': phase_data.get('isOutdoor', False),
                'isVegetarianFriendly': phase_data.get('isVegetarianFriendly', False),
                'isAlcoholFriendly': phase_data.get('isAlcoholFriendly', False)
            })
            
            # Determine indicators
            indicators = []
            if phase_data.get('isIndoor', True):
                indicators.append('indoor')
            if phase_data.get('isOutdoor', False):
                indicators.append('outdoor')
            if phase_data.get('isVegetarianFriendly', False):
                indicators.append('vegetarian-friendly')
            if phase_data.get('isAlcoholFriendly', False):
                indicators.append('alcohol-friendly')
            
            # Add indicators to enhanced phase
            enhanced_phase['indicators'] = indicators
            
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
        rating = plan.get('rating', 3)
        
        return {
            'phases': phases,
            'total_cost': total_cost,
            'contribution_needed': contribution_needed,
            'fit_analysis': fit_analysis,
            'rating': rating,
            'location_validation': location_validation,
            'travel_summary': travel_summary
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
        encoded_location = location.replace(' ', '+')
        return f"https://www.google.com/maps/search/{encoded_location}"

def generate_fit_analysis(plan, team_members):
    """Generate fit analysis for the plan."""
    try:
        # Extract best for members if available
        best_for = plan.get('bestFor', [])
        if best_for:
            return f"Suits team members: {', '.join(best_for)}"
        
        # Generate based on theme and preferences
        theme = plan.get('theme', 'general')
        if theme == 'fun 🎉':
            return "Perfect for energetic team members who enjoy social activities"
        elif theme == 'chill 🧘':
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
                    "indicators": ["indoor", "vegetarian-friendly"]
                },
                {
                    "activity": "Karaoke Session",
                    "location": "456 Le Loi, District 1, Ho Chi Minh City",
                    "map_link": "https://maps.google.com/?q=456+Le+Loi+District+1",
                    "cost": 150000,
                    "indicators": ["indoor"]
                }
            ],
            "total_cost": 400000,
            "contribution_needed": 100000,
            "fit_analysis": "Suits team members in District 1",
            "rating": 4
        },
        {
            "phases": [
                {
                    "activity": "Cafe Hopping",
                    "location": "789 Dong Khoi, District 1, Ho Chi Minh City",
                    "map_link": "https://maps.google.com/?q=789+Dong+Khoi+District+1",
                    "cost": 200000,
                    "indicators": ["indoor", "vegetarian-friendly"]
                }
            ],
            "total_cost": 200000,
            "contribution_needed": 0,
            "fit_analysis": "Perfect for chill team members",
            "rating": 3
        }
    ]

@app.route('/team-members', methods=['GET'])
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
        return jsonify({'error': str(e)}), 500

@app.route('/team-members', methods=['POST'])
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
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate required fields
        required_fields = ['name', 'location', 'preferences', 'vibe']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Load existing team members
        team_members = load_team_members()
        
        # Generate new ID
        new_id = str(uuid.uuid4())
        
        # Create new team member
        new_member = {
            'id': new_id,
            'name': data['name'],
            'location': data['location'],
            'preferences': data['preferences'],
            'vibe': data['vibe']
        }
        
        # Add to list and save
        team_members.append(new_member)
        save_team_members(team_members)
        
        return jsonify(new_member), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/team-members/<member_id>', methods=['PUT'])
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
            return jsonify({'error': 'No data provided'}), 400
        
        # Load existing team members
        team_members = load_team_members()
        
        # Find the member to update
        member_index = None
        for i, member in enumerate(team_members):
            if member['id'] == member_id:
                member_index = i
                break
        
        if member_index is None:
            return jsonify({'error': 'Team member not found'}), 404
        
        # Update member data
        team_members[member_index].update({
            'name': data.get('name', team_members[member_index]['name']),
            'location': data.get('location', team_members[member_index]['location']),
            'preferences': data.get('preferences', team_members[member_index]['preferences']),
            'vibe': data.get('vibe', team_members[member_index]['vibe'])
        })
        
        # Save updated data
        save_team_members(team_members)
        
        return jsonify(team_members[member_index])
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/team-members/<member_id>', methods=['DELETE'])
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
            if member['id'] == member_id:
                member_index = i
                break
        
        if member_index is None:
            return jsonify({'error': 'Team member not found'}), 404
        
        # Remove member
        team_members.pop(member_index)
        
        # Save updated data
        save_team_members(team_members)
        
        return jsonify({'message': 'Team member deleted successfully'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/event-history', methods=['GET'])
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
        return jsonify({'error': str(e)}), 500

@app.route('/event-history', methods=['POST'])
def save_event():
    """
    Save a new event to the history.
    
    Request Body:
    {
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
    """
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Load existing events
        events = load_event_history()
        
        # Check for duplicates based on key attributes
        theme = data.get('theme', 'general')
        date = data.get('date', datetime.now().strftime('%Y-%m-%d'))
        total_cost = data.get('total_cost', 0)
        activities = data.get('activities', [])
        
        # Check if a similar event already exists
        for existing_event in events:
            if (existing_event.get('theme') == theme and
                existing_event.get('date') == date and
                existing_event.get('total_cost') == total_cost and
                existing_event.get('activities') == activities):
                return jsonify({
                    'error': 'A similar event already exists in the history',
                    'duplicate_id': existing_event.get('id')
                }), 409  # Conflict status code
        
        # Generate new ID
        new_id = max([event.get('id', 0) for event in events], default=0) + 1
        
        # Create new event
        new_event = {
            'id': new_id,
            'date': date,
            'theme': theme,
            'location': data.get('location', 'Ho Chi Minh City'),
            'participants': data.get('participants', []),
            'activities': activities,
            'total_cost': total_cost,
            'phases': data.get('phases', []),
            'fit_analysis': data.get('fit_analysis', ''),
            'rating': data.get('rating', 3),  # AI rating
            'ai_rating': data.get('rating', 3),  # Explicit AI rating field
            'contribution_needed': data.get('contribution_needed', 0)
        }
        
        # Add to list and save
        events.append(new_event)
        save_event_history(events)
        
        return jsonify(new_event), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/event-history/<int:event_id>', methods=['DELETE'])
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
            if event.get('id') == event_id:
                event_index = i
                break
        
        if event_index is None:
            return jsonify({'error': 'Event not found'}), 404
        
        # Remove event
        events.pop(event_index)
        
        # Save updated data
        save_event_history(events)
        
        return jsonify({'message': 'Event deleted successfully'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/event-history/<int:event_id>/rate', methods=['POST'])
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
            return jsonify({'error': 'No data provided'}), 400
        
        # Load existing events
        events = load_event_history()
        
        # Find the event to rate
        event_index = None
        for i, event in enumerate(events):
            if event.get('id') == event_id:
                event_index = i
                break
        
        if event_index is None:
            return jsonify({'error': 'Event not found'}), 404
        
        event = events[event_index]
        member_name = data.get('member_name', '')
        
        # Validate member name is in participants list
        if member_name not in event.get('participants', []):
            return jsonify({'error': 'Member not found in event participants'}), 400
        
        # Check if member has already rated this event
        if 'member_ratings' not in event:
            event['member_ratings'] = []
        
        for rating in event['member_ratings']:
            if rating.get('member_name') == member_name:
                return jsonify({'error': 'Member has already rated this event'}), 409
        
        # Create new rating
        new_rating = {
            'member_name': member_name,
            'rating': data.get('rating', 0),
            'feedback': data.get('feedback', ''),
            'categories': data.get('categories', {
                'fun': 0,
                'organization': 0,
                'value': 0,
                'overall': 0
            }),
            'submitted_at': data.get('submitted_at', datetime.now().isoformat())
        }
        
        # Add rating to event
        event['member_ratings'].append(new_rating)
        
        # Calculate average rating from all member ratings (preserve AI rating)
        if event['member_ratings']:
            total_rating = sum(r['rating'] for r in event['member_ratings'])
            member_average = round(total_rating / len(event['member_ratings']), 1)
            # Keep the original AI rating in 'ai_rating' field
            if 'ai_rating' not in event:
                event['ai_rating'] = event.get('rating', 3)
            # Update 'rating' field with member average (for backward compatibility)
            event['rating'] = member_average
        else:
            # If no member ratings, keep AI rating
            if 'ai_rating' not in event:
                event['ai_rating'] = event.get('rating', 3)
        
        # Save updated events
        save_event_history(events)
        
        return jsonify({
            'message': 'Rating submitted successfully',
            'rating': new_rating,
            'member_average': event.get('rating', 0),
            'ai_rating': event.get('ai_rating', 0)
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'ai_provider': ai_service.provider_name if hasattr(ai_service, 'provider_name') else 'unknown'
    })

@app.route('/analytics/suggestions', methods=['GET'])
def get_activity_suggestions():
    """
    Analyze recent saved activities and generate AI-powered suggestions.
    
    Query Parameters:
    - limit: Number of recent events to analyze (default: 10)
    - theme: Filter by specific theme (optional)
    
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
    try:
        # Get query parameters
        limit = request.args.get('limit', 10, type=int)
        theme_filter = request.args.get('theme', None)
        
        # Load recent events
        events = load_event_history()
        
        # Sort by date (most recent first) and apply limit
        events.sort(key=lambda x: x.get('date', ''), reverse=True)
        recent_events = events[:limit]
        
        # Apply theme filter if specified
        if theme_filter:
            recent_events = [e for e in recent_events if e.get('theme') == theme_filter]
        
        if not recent_events:
            return jsonify({
                'suggestions': [],
                'analytics_summary': {
                    'total_events': 0,
                    'message': 'No recent events found for analysis'
                }
            })
        
        # Prepare analytics data for AI analysis
        analytics_data = {
            'events': recent_events,
            'total_events': len(recent_events),
            'themes': [e.get('theme') for e in recent_events],
            'activities': [activity for e in recent_events for activity in e.get('activities', [])],
            'costs': [e.get('total_cost', 0) for e in recent_events],
            'ratings': [e.get('rating', 0) for e in recent_events if e.get('rating')],
            'locations': [e.get('location') for e in recent_events],
            'participant_counts': [len(e.get('participants', [])) for e in recent_events]
        }
        
        # Generate AI-powered suggestions
        suggestions = generate_activity_suggestions(analytics_data)
        
        # Create analytics summary
        analytics_summary = create_analytics_summary(analytics_data)
        
        # Save analytics data
        save_analytics_data(analytics_data, suggestions, analytics_summary)
        
        return jsonify({
            'suggestions': suggestions,
            'analytics_summary': analytics_summary
        })
        
    except Exception as e:
        logger.error(f"Error generating suggestions: {e}")
        return jsonify({'error': str(e)}), 500

def load_analytics_data():
    """Load analytics data from JSON file."""
    try:
        with open('analytics_data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {'analytics_history': [], 'suggestions_history': []}
    except Exception as e:
        logger.error(f"Error loading analytics data: {e}")
        return {'analytics_history': [], 'suggestions_history': []}

def save_analytics_data(analytics_data, suggestions, analytics_summary):
    """Save analytics data to JSON file."""
    try:
        existing_data = load_analytics_data()
        
        # Add new analytics entry
        new_entry = {
            'timestamp': datetime.now().isoformat(),
            'analytics_data': analytics_data,
            'suggestions': suggestions,
            'analytics_summary': analytics_summary
        }
        
        existing_data['analytics_history'].append(new_entry)
        
        # Keep only last 50 entries to prevent file from growing too large
        if len(existing_data['analytics_history']) > 50:
            existing_data['analytics_history'] = existing_data['analytics_history'][-50:]
        
        with open('analytics_data.json', 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, indent=2, ensure_ascii=False)
            
    except Exception as e:
        logger.error(f"Error saving analytics data: {e}")

def create_analytics_summary(analytics_data):
    """Create a summary of analytics data."""
    try:
        events = analytics_data['events']
        themes = analytics_data['themes']
        activities = analytics_data['activities']
        costs = analytics_data['costs']
        ratings = analytics_data['ratings']
        
        # Calculate statistics
        theme_counts = {}
        for theme in themes:
            theme_counts[theme] = theme_counts.get(theme, 0) + 1
        
        most_popular_theme = max(theme_counts.items(), key=lambda x: x[1])[0] if theme_counts else "No data"
        average_cost = sum(costs) / len(costs) if costs else 0
        
        # Find common activities
        activity_counts = {}
        for activity in activities:
            activity_counts[activity] = activity_counts.get(activity, 0) + 1
        
        common_activities = sorted(activity_counts.items(), key=lambda x: x[1], reverse=True)[:5]
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
            'total_events': len(events),
            'most_popular_theme': most_popular_theme,
            'average_cost': round(average_cost, 2),
            'common_activities': common_activities,
            'rating_trends': rating_trend,
            'theme_distribution': theme_counts
        }
        
    except Exception as e:
        logger.error(f"Error creating analytics summary: {e}")
        return {'error': str(e)}

def generate_activity_suggestions(analytics_data):
    """Generate AI-powered suggestions based on analytics data."""
    try:
        events = analytics_data['events']
        themes = analytics_data['themes']
        activities = analytics_data['activities']
        costs = analytics_data['costs']
        ratings = analytics_data['ratings']
        
        if not events:
            return []
        
        # Prepare data for AI analysis
        analysis_prompt = f"""
        Analyze the following team bonding event data and provide actionable suggestions:

        Recent Events Analysis:
        - Total events analyzed: {len(events)}
        - Themes used: {', '.join(set(themes))}
        - Activities performed: {', '.join(set(activities))}
        - Cost range: {min(costs) if costs else 0} - {max(costs) if costs else 0} VND
        - Average rating: {sum(ratings)/len(ratings) if ratings else 'No data'}/5

        Event Details:
        {json.dumps([{
            'theme': e.get('theme'),
            'activities': e.get('activities', []),
            'cost': e.get('total_cost'),
            'rating': e.get('rating'),
            'participants': len(e.get('participants', []))
        } for e in events[:5]], indent=2)}

        Please provide 3-5 specific suggestions in JSON format:
        {{
            "suggestions": [
                {{
                    "type": "theme_preference|activity_suggestion|cost_optimization|timing_insight",
                    "title": "Brief title",
                    "description": "Detailed explanation with actionable advice",
                    "confidence": 0.85,
                    "data_points": 5,
                    "category": "theme|activity|cost|timing"
                }}
            ]
        }}

        Focus on:
        1. Theme preferences and patterns
        2. Most successful activities
        3. Cost optimization opportunities
        4. Timing and scheduling insights
        5. Participant engagement patterns
        """
        
        # Get AI response
        response = ai_service.generate_response(analysis_prompt)
        
        # Parse AI response
        try:
            # Try to extract JSON from response
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                suggestions_data = json.loads(json_match.group())
                return suggestions_data.get('suggestions', [])
            else:
                # Fallback: create basic suggestions
                return create_fallback_suggestions(analytics_data)
                
        except json.JSONDecodeError:
            # Fallback: create basic suggestions
            return create_fallback_suggestions(analytics_data)
            
    except Exception as e:
        logger.error(f"Error generating AI suggestions: {e}")
        return create_fallback_suggestions(analytics_data)

def create_fallback_suggestions(analytics_data):
    """Create fallback suggestions when AI analysis fails."""
    suggestions = []
    
    try:
        themes = analytics_data['themes']
        activities = analytics_data['activities']
        costs = analytics_data['costs']
        ratings = analytics_data['ratings']
        
        # Theme preference suggestion
        if themes:
            theme_counts = {}
            for theme in themes:
                theme_counts[theme] = theme_counts.get(theme, 0) + 1
            
            most_popular = max(theme_counts.items(), key=lambda x: x[1])
            suggestions.append({
                'type': 'theme_preference',
                'title': f'Popular Theme: {most_popular[0]}',
                'description': f'Your team shows a strong preference for {most_popular[0]} events ({most_popular[1]} times). Consider exploring variations of this theme.',
                'confidence': 0.8,
                'data_points': len(themes),
                'category': 'theme'
            })
        
        # Activity suggestion
        if activities:
            activity_counts = {}
            for activity in activities:
                activity_counts[activity] = activity_counts.get(activity, 0) + 1
            
            top_activity = max(activity_counts.items(), key=lambda x: x[1])
            suggestions.append({
                'type': 'activity_suggestion',
                'title': f'Successful Activity: {top_activity[0]}',
                'description': f'"{top_activity[0]}" appears {top_activity[1]} times in your events. This activity seems to work well for your team.',
                'confidence': 0.75,
                'data_points': len(activities),
                'category': 'activity'
            })
        
        # Cost optimization
        if costs:
            avg_cost = sum(costs) / len(costs)
            if avg_cost > 200000:
                suggestions.append({
                    'type': 'cost_optimization',
                    'title': 'Cost Optimization Opportunity',
                    'description': f'Average event cost is {avg_cost:,.0f} VND. Consider mixing high and low-cost activities to balance budget.',
                    'confidence': 0.7,
                    'data_points': len(costs),
                    'category': 'cost'
                })
        
        # Rating insight
        if ratings:
            avg_rating = sum(ratings) / len(ratings)
            if avg_rating < 3.5:
                suggestions.append({
                    'type': 'rating_insight',
                    'title': 'Improve Event Satisfaction',
                    'description': f'Average rating is {avg_rating:.1f}/5. Consider gathering more feedback to understand preferences better.',
                    'confidence': 0.6,
                    'data_points': len(ratings),
                    'category': 'rating'
                })
        
    except Exception as e:
        logger.error(f"Error creating fallback suggestions: {e}")
    
    return suggestions

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 