from flask import Flask, request, jsonify
from flask_cors import CORS
from services.calendar_service import CalendarService
from services.maps_service import MapsService
from services.ai_service import AIService
from config import SCOPES, AI_CONFIG
import time

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

@app.route('/api/ai/providers', methods=['GET'])
def get_ai_providers():
    """Get available AI providers and current provider."""
    try:
        available_providers = ai_service.get_available_providers()
        current_provider = ai_service.provider_name
        
        return jsonify({
            'available_providers': available_providers,
            'current_provider': current_provider,
            'providers_info': {
                'openai': {
                    'name': 'OpenAI GPT',
                    'models': ['gpt-4', 'gpt-4-turbo', 'gpt-3.5-turbo', 'gpt-4o'],
                    'description': 'Advanced language model with strong reasoning capabilities'
                },
                'anthropic': {
                    'name': 'Anthropic Claude',
                    'models': ['claude-3-sonnet-20240229', 'claude-3-haiku-20240307', 'claude-3-opus-20240229'],
                    'description': 'Safety-focused AI with excellent analysis skills'
                },
                'google': {
                    'name': 'Google Gemini',
                    'models': ['gemini-1.5-pro', 'gemini-1.5-flash', 'gemini-1.0-pro'],
                    'description': 'Multimodal AI with strong creative capabilities'
                }
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai/switch-provider', methods=['POST'])
def switch_ai_provider():
    """Switch to a different AI provider."""
    try:
        data = request.json
        provider = data.get('provider')
        
        if not provider:
            return jsonify({'error': 'Provider not specified'}), 400
        
        success = ai_service.switch_provider(provider)
        
        if success:
            return jsonify({
                'message': f'Switched to {provider}',
                'current_provider': ai_service.provider_name
            })
        else:
            return jsonify({'error': f'Provider {provider} not available'}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai/performance', methods=['GET'])
def get_ai_performance():
    """Get AI performance statistics."""
    try:
        time_window = request.args.get('time_window', 24, type=int)
        stats = ai_service.get_performance_stats(time_window)
        
        return jsonify({
            'performance_stats': stats,
            'time_window_hours': time_window,
            'current_provider': ai_service.provider_name
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai/recommendations', methods=['GET'])
def get_ai_recommendations():
    """Get AI model recommendations."""
    try:
        use_case = request.args.get('use_case', 'general')
        recommendations = ai_service.get_model_recommendations(use_case)
        
        return jsonify({
            'recommendations': recommendations,
            'use_case': use_case,
            'current_provider': ai_service.provider_name
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai/ab-test/setup', methods=['POST'])
def setup_ab_test():
    """Setup A/B testing configuration."""
    try:
        data = request.json
        test_name = data.get('test_name')
        providers = data.get('providers', [])
        traffic_split = data.get('traffic_split')
        
        if not test_name or not providers:
            return jsonify({'error': 'Test name and providers are required'}), 400
        
        ai_service.setup_ab_test(test_name, providers, traffic_split)
        
        return jsonify({
            'message': f'A/B test "{test_name}" setup successfully',
            'test_name': test_name,
            'providers': providers,
            'traffic_split': traffic_split
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai/ab-test/results/<test_name>', methods=['GET'])
def get_ab_test_results(test_name):
    """Get A/B test results."""
    try:
        results = ai_service.get_ab_test_results(test_name)
        
        if not results:
            return jsonify({'error': f'A/B test "{test_name}" not found'}), 404
        
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai/ab-test/provider/<test_name>', methods=['GET'])
def get_ab_test_provider(test_name):
    """Get provider for A/B testing."""
    try:
        provider = ai_service.get_ab_test_provider(test_name)
        
        if not provider:
            return jsonify({'error': f'A/B test "{test_name}" not found'}), 404
        
        return jsonify({
            'test_name': test_name,
            'selected_provider': provider
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/suggestions', methods=['POST'])
def get_suggestions():
    """Get activity suggestions based on team data."""
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Check if this is an A/B test request
        ab_test_name = data.get('ab_test_name')
        if ab_test_name:
            ab_provider = ai_service.get_ab_test_provider(ab_test_name)
            if ab_provider:
                ai_service.switch_provider(ab_provider)
            
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
        
        # Record A/B test result if applicable
        if ab_test_name:
            ai_service.model_manager.record_ab_test_result(
                ab_test_name, 
                ai_service.provider_name, 
                len(suggestions) > 0
            )
        
        return jsonify({
            'suggestions': suggestions,
            'free_slots': free_slots,
            'central_location': central_location,
            'ai_provider_used': ai_service.provider_name,
            'ab_test_name': ab_test_name if ab_test_name else None
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai/test', methods=['POST'])
def test_ai_provider():
    """Test the current AI provider with a simple prompt."""
    try:
        data = request.json
        test_prompt = data.get('prompt', 'Hello, can you provide a brief response to test the AI service?')
        
        if not ai_service.current_provider:
            return jsonify({'error': 'No AI provider available'}), 400
        
        try:
            start_time = time.time()
            response = ai_service.current_provider.generate_response(
                prompt=test_prompt,
                system_prompt="You are a helpful AI assistant. Provide a brief, friendly response.",
                temperature=0.7,
                max_tokens=100
            )
            response_time = time.time() - start_time
            
            # Record performance
            ai_service.model_manager.record_performance(
                provider=ai_service.provider_name,
                model=AI_CONFIG['models'][ai_service.provider_name]['default'],
                response_time=response_time,
                success=True
            )
            
            return jsonify({
                'success': True,
                'response': response,
                'provider': ai_service.provider_name,
                'response_time': response_time
            })
        except Exception as ai_error:
            response_time = time.time() - start_time if 'start_time' in locals() else 0
            
            # Record failed performance
            ai_service.model_manager.record_performance(
                provider=ai_service.provider_name,
                model=AI_CONFIG['models'][ai_service.provider_name]['default'],
                response_time=response_time,
                success=False,
                error_message=str(ai_error)
            )
            
            return jsonify({
                'success': False,
                'error': str(ai_error),
                'provider': ai_service.provider_name,
                'response_time': response_time
            }), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 