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

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'ai_provider': ai_service.provider_name if hasattr(ai_service, 'provider_name') else 'unknown'
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 