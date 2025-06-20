import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Google Calendar API configuration
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')

# AI Provider API Keys
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
GOOGLE_AI_API_KEY = os.getenv('GOOGLE_AI_API_KEY', '')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY', '')

# AI Configuration
AI_CONFIG = {
    'default_provider': os.getenv('DEFAULT_AI_PROVIDER', 'anthropic'),
    'fallback_provider': os.getenv('FALLBACK_AI_PROVIDER', 'google'),
    'models': {
        'anthropic': {
            'default': 'claude-3-5-sonnet-20241022',
            'fallback': 'claude-3-haiku-20240307',
            'available': ['claude-3-5-sonnet-20241022', 'claude-3-5-haiku-20241022', 'claude-3-opus-20240229', 'claude-3-sonnet-20240229', 'claude-3-haiku-20240307']
        },
        'google': {
            'default': 'gemini-1.5-pro',
            'fallback': 'gemini-1.5-flash',
            'available': ['gemini-1.5-pro', 'gemini-1.5-flash', 'gemini-1.0-pro']
        },
        'openai': {
            'default': 'gpt-4o',
            'fallback': 'gpt-3.5-turbo',
            'available': ['gpt-4', 'gpt-4-turbo', 'gpt-3.5-turbo', 'gpt-4o']
        }
    },
    'settings': {
        'temperature': 0.7,
        'max_tokens': 500,
        'timeout': 30
    }
}

# Google Maps API configuration
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')

# Scopes for Google Calendar API
SCOPES = [
    'https://www.googleapis.com/auth/calendar.readonly',
    'https://www.googleapis.com/auth/calendar.events.readonly'
]

# Calendar settings
CALENDAR_SETTINGS = {
    'timezone': 'UTC',
    'max_results': 100,
    'look_ahead_days': 30
} 