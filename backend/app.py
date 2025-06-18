from flask import Flask, request, jsonify
from flask_cors import CORS
from services.calendar_service import CalendarService
from services.maps_service import MapsService
from services.ai_service import AIService
from config import CALENDAR_SCOPES

app = Flask(__name__)
CORS(app)

calendar_service = CalendarService()
maps_service = MapsService()
ai_service = AIService(provider='auto')

@app.route('/api/auth/url', methods=['GET'])
def get_auth_url():
    """Get Google Calendar authentication URL."""
    try:
        flow = calendar_service.authenticate()
        auth_url = flow.authorization_url()[0]
        return jsonify({'auth_url': auth_url})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/callback', methods=['POST'])
def auth_callback():
    """Handle Google Calendar authentication callback."""
    try:
        code = request.json.get('code')
        if not code:
            return jsonify({'error': 'No authorization code provided'}), 400
            
        flow = calendar_service.authenticate()
        flow.fetch_token(code=code)
        credentials = flow.credentials
        
        # Store credentials for future use
        calendar_service.store_credentials(credentials)
        
        return jsonify({'message': 'Authentication successful'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/suggestions', methods=['POST'])
def get_suggestions():
    """Get activity suggestions based on team data."""
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        # Get team members' locations
        locations = []
        for member in data.get('team_members', []):
            if 'address' in member:
                location = maps_service.geocode_address(member['address'])
                if location:
                    locations.append(location)
        
        # Find central location
        central_location = maps_service.find_central_location(locations) if locations else None
        
        # Get free time slots from calendars
        calendar_ids = [member.get('calendar_id') for member in data.get('team_members', []) if member.get('calendar_id')]
        free_slots = calendar_service.get_free_time_slots(calendar_ids) if calendar_ids else []
        
        # Generate suggestions using AI
        team_data = {
            'interests': data.get('interests', []),
            'budget': data.get('budget', 0),
            'group_size': len(data.get('team_members', []))
        }
        
        suggestions = ai_service.generate_activity_suggestions(
            team_data,
            free_slots,
            central_location or {'formatted_address': 'Unknown location'}
        )
        
        # Enhance suggestions with nearby places
        if central_location:
            for suggestion in suggestions:
                if 'name' in suggestion:
                    nearby_places = maps_service.find_nearby_places(
                        central_location['location'],
                        suggestion['name']
                    )
                    if nearby_places:
                        suggestion['nearby_places'] = nearby_places[:3]
        
        return jsonify({
            'suggestions': suggestions,
            'free_slots': free_slots,
            'central_location': central_location
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 