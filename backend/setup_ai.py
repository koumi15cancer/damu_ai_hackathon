#!/usr/bin/env python3
"""
AI Integration Setup Script
Helps you configure and test AI API integration for the Team Bonding Event Planner
"""

import os
import sys
import json
import requests
from pathlib import Path

def check_env_file():
    """Check if .env file exists and has API keys"""
    env_path = Path('.env')
    
    if not env_path.exists():
        print("❌ No .env file found. Creating one...")
        create_env_file()
        return False
    
    with open(env_path, 'r') as f:
        content = f.read()
    
    # Check for API keys
    has_openai = 'OPENAI_API_KEY=' in content and 'sk-' in content
    has_google = 'GOOGLE_AI_API_KEY=' in content and len(content.split('GOOGLE_AI_API_KEY=')[1].split('\n')[0]) > 10
    
    print("🔍 Checking API keys in .env file:")
    print(f"   OpenAI: {'✅' if has_openai else '❌'}")
    print(f"   Google AI: {'✅' if has_google else '❌'}")
    
    return has_openai or has_google

def create_env_file():
    """Create a new .env file with template"""
    template = """# AI API Keys - Add your keys here
# Get keys from: https://platform.openai.com/api-keys (OpenAI)
# Get keys from: https://makersuite.google.com/app/apikey (Google AI)

# OpenAI (Recommended - easiest to set up)
OPENAI_API_KEY=sk-your_openai_key_here

# Google AI (Gemini)
GOOGLE_AI_API_KEY=your_google_ai_key_here

# Optional: Google Calendar & Maps
GOOGLE_CLIENT_ID=your_google_client_id_here
GOOGLE_CLIENT_SECRET=your_google_client_secret_here
GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here
"""
    
    with open('.env', 'w') as f:
        f.write(template)
    
    print("✅ Created .env file with template")
    print("📝 Please edit .env file and add your API keys")

def test_backend_connection():
    """Test if backend is running"""
    try:
        response = requests.get('http://localhost:5000/api/team-bonding/team-members', timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running on http://localhost:5000")
            return True
        else:
            print("❌ Backend responded with error")
            return False
    except requests.exceptions.RequestException:
        print("❌ Backend is not running. Please start it with: python3 app.py")
        return False

def test_ai_integration():
    """Test AI integration with a simple request"""
    test_data = {
        "monthly_theme": "fun",
        "optional_contribution": 100000,
        "available_members": ["Ben", "Cody"],
        "preferred_date": "2024-01-15",
        "preferred_location_zone": "District 1"
    }
    
    try:
        print("🧪 Testing AI integration...")
        response = requests.post(
            'http://localhost:5000/api/team-bonding/plans',
            json=test_data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if 'plans' in result and len(result['plans']) > 0:
                print("✅ AI integration working!")
                print(f"   Generated {len(result['plans'])} plans")
                return True
            else:
                print("❌ No plans generated")
                return False
        else:
            print(f"❌ Backend error: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False

def show_next_steps():
    """Show next steps for setup"""
    print("\n" + "="*50)
    print("🎯 NEXT STEPS")
    print("="*50)
    print("1. Get an API key from one of these providers:")
    print("   • OpenAI (recommended): https://platform.openai.com/api-keys")
    print("   • Google AI: https://makersuite.google.com/app/apikey")
    print()
    print("2. Edit the .env file and add your API key:")
    print("   nano .env")
    print()
    print("3. Restart the backend:")
    print("   python3 app.py")
    print()
    print("4. Test the integration:")
    print("   python3 setup_ai.py")
    print()
    print("5. Open the frontend:")
    print("   http://localhost:3000")
    print("="*50)

def main():
    """Main setup function"""
    print("🤖 AI Integration Setup for Team Bonding Event Planner")
    print("="*60)
    
    # Check if we're in the right directory
    if not Path('app.py').exists():
        print("❌ Please run this script from the backend directory")
        print("   cd backend && python3 setup_ai.py")
        sys.exit(1)
    
    # Check .env file
    has_keys = check_env_file()
    
    if not has_keys:
        print("\n📝 Please add your API keys to the .env file")
        show_next_steps()
        return
    
    # Test backend connection
    if not test_backend_connection():
        show_next_steps()
        return
    
    # Test AI integration
    if test_ai_integration():
        print("\n🎉 SUCCESS! Your AI integration is working!")
        print("   You can now use the frontend to generate AI-powered event plans.")
    else:
        print("\n❌ AI integration test failed")
        print("   Check your API keys and try again")
        show_next_steps()

if __name__ == "__main__":
    main() 