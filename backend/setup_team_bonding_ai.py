#!/usr/bin/env python3
"""
Team Bonding AI Integration Setup Script
Helps you configure and test the enhanced AI integration for team bonding event planning
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
    template = """# Team Bonding AI Integration - API Keys
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

# AI Configuration (optional)
DEFAULT_AI_PROVIDER=openai
FALLBACK_AI_PROVIDER=google
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

def test_ai_providers():
    """Test AI provider availability"""
    try:
        response = requests.get('http://localhost:5000/api/ai/providers', timeout=5)
        if response.status_code == 200:
            data = response.json()
            providers = data.get('available_providers', [])
            current = data.get('current_provider', 'None')
            
            print(f"✅ AI Providers API working")
            print(f"   Available providers: {providers}")
            print(f"   Current provider: {current}")
            
            return len(providers) > 0
        else:
            print("❌ AI Providers API error")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ AI Providers API failed: {e}")
        return False

def test_team_bonding_generation():
    """Test team bonding plan generation"""
    test_data = {
        "monthly_theme": "fun",
        "optional_contribution": 100000,
        "available_members": ["Ben", "Cody", "Big Thanh"],
        "preferred_date": "2024-01-15",
        "preferred_location_zone": "District 1"
    }
    
    try:
        print("🧪 Testing team bonding plan generation...")
        response = requests.post(
            'http://localhost:5000/api/team-bonding/plans',
            json=test_data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            plans = result.get('plans', [])
            ai_provider = result.get('ai_provider', 'None')
            
            if len(plans) > 0:
                print("✅ Team bonding generation working!")
                print(f"   Generated {len(plans)} plans")
                print(f"   AI Provider: {ai_provider}")
                
                # Show first plan details
                first_plan = plans[0]
                print(f"   First plan: {first_plan.get('title', 'Untitled')}")
                print(f"   Theme: {first_plan.get('theme', 'Unknown')}")
                print(f"   Cost: {first_plan.get('totalCost', 0):,} VND")
                
                # Check constraint validation
                validation = first_plan.get('constraintValidation', {})
                print(f"   Budget compliant: {validation.get('budgetCompliant', False)}")
                print(f"   Distance compliant: {validation.get('distanceCompliant', False)}")
                
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

def test_performance_monitoring():
    """Test performance monitoring features"""
    try:
        print("📊 Testing performance monitoring...")
        response = requests.get('http://localhost:5000/api/ai/performance', timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            stats = data.get('performance_stats', {})
            current_provider = data.get('current_provider', 'None')
            
            print("✅ Performance monitoring working!")
            print(f"   Current provider: {current_provider}")
            print(f"   Stats available: {len(stats)} providers")
            
            return True
        else:
            print("❌ Performance monitoring error")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Performance monitoring failed: {e}")
        return False

def test_ab_testing():
    """Test A/B testing features"""
    try:
        print("🧪 Testing A/B testing setup...")
        
        # Setup A/B test
        ab_test_data = {
            "test_name": "team_bonding_test",
            "providers": ["openai", "google"],
            "traffic_split": {"openai": 0.6, "google": 0.4}
        }
        
        response = requests.post(
            'http://localhost:5000/api/ai/ab-test/setup',
            json=ab_test_data,
            timeout=5
        )
        
        if response.status_code == 200:
            print("✅ A/B testing setup working!")
            
            # Test getting provider
            provider_response = requests.get(
                'http://localhost:5000/api/ai/ab-test/provider/team_bonding_test',
                timeout=5
            )
            
            if provider_response.status_code == 200:
                provider_data = provider_response.json()
                selected_provider = provider_data.get('selected_provider', 'None')
                print(f"   Selected provider: {selected_provider}")
                return True
            else:
                print("❌ A/B test provider selection failed")
                return False
        else:
            print("❌ A/B testing setup failed")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ A/B testing failed: {e}")
        return False

def show_enhanced_features():
    """Show the enhanced AI features"""
    print("\n🚀 Enhanced Team Bonding AI Features")
    print("=" * 50)
    print("✅ Multi-Provider AI Support")
    print("   • OpenAI GPT (GPT-4, GPT-4 Turbo, GPT-3.5 Turbo)")
    print("   • Google Gemini (Gemini 1.5 Pro, Flash, 1.0 Pro)")
    print()
    print("✅ Advanced Constraint Validation")
    print("   • Budget compliance (300k VND base + optional contributions)")
    print("   • Distance constraints (≤ 2km between phases)")
    print("   • Travel time validation (≤ 15 minutes)")
    print("   • Location balance consideration")
    print()
    print("✅ Intelligent Prompt Construction")
    print("   • Dynamic prompts based on team profiles")
    print("   • Theme-specific guidelines (fun 🎉, chill 🧘, outdoor 🌤)")
    print("   • Multi-phase event planning (dinner → karaoke → bar)")
    print("   • Ho Chi Minh City specific recommendations")
    print()
    print("✅ Performance Monitoring")
    print("   • Real-time response time tracking")
    print("   • Success/failure rate monitoring")
    print("   • Automatic performance-based provider selection")
    print("   • Historical performance analytics")
    print()
    print("✅ A/B Testing Capabilities")
    print("   • Multi-provider A/B testing")
    print("   • Configurable traffic splitting")
    print("   • Performance comparison")
    print("   • Result tracking and analysis")
    print()
    print("✅ Robust Error Handling")
    print("   • Automatic fallback to sample plans")
    print("   • Provider switching on failure")
    print("   • Graceful degradation")
    print("   • Comprehensive error logging")

def show_next_steps():
    """Show next steps for setup"""
    print("\n" + "="*60)
    print("🎯 NEXT STEPS")
    print("="*60)
    print("1. Get an API key from one of these providers:")
    print("   • OpenAI (recommended): https://platform.openai.com/api-keys")
    print("   • Google AI: https://makersuite.google.com/app/apikey")
    print()
    print("2. Edit the .env file and add your API key:")
    print("   nano .env")
    print()
    print("3. Start the backend:")
    print("   python3 app.py")
    print()
    print("4. Test the enhanced AI integration:")
    print("   python3 test_team_bonding_ai.py")
    print()
    print("5. Open the frontend:")
    print("   http://localhost:3000")
    print()
    print("6. Try the enhanced features:")
    print("   • Generate team bonding plans with AI")
    print("   • Test different themes (fun, chill, outdoor)")
    print("   • Monitor AI performance")
    print("   • Set up A/B testing")
    print("="*60)

def main():
    """Main setup function"""
    print("🤖 Enhanced Team Bonding AI Integration Setup")
    print("="*60)
    
    # Check if we're in the right directory
    if not Path('app.py').exists():
        print("❌ Please run this script from the backend directory")
        print("   cd backend && python3 setup_team_bonding_ai.py")
        sys.exit(1)
    
    # Show enhanced features
    show_enhanced_features()
    
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
    
    # Test AI providers
    if not test_ai_providers():
        print("\n❌ No AI providers available")
        show_next_steps()
        return
    
    # Test team bonding generation
    if not test_team_bonding_generation():
        print("\n❌ Team bonding generation failed")
        show_next_steps()
        return
    
    # Test performance monitoring
    test_performance_monitoring()
    
    # Test A/B testing
    test_ab_testing()
    
    print("\n🎉 SUCCESS! Your enhanced AI integration is working!")
    print("   You can now use all the advanced team bonding features.")
    print("\n💡 Try these advanced features:")
    print("   • Switch between AI providers: POST /api/ai/switch-provider")
    print("   • Monitor performance: GET /api/ai/performance")
    print("   • Set up A/B testing: POST /api/ai/ab-test/setup")
    print("   • Get model recommendations: GET /api/ai/recommendations")

if __name__ == "__main__":
    main() 