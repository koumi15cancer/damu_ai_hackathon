#!/usr/bin/env python3
"""
Test script to demonstrate logging in the generate_team_bonding_plans flow.
This script will help you understand what's happening at each step of the process.
"""

import sys
import os

# Add the backend directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import logging configuration first
from logging_config import setup_logging, setup_debug_logging, setup_development_logging
from services.ai_service import AIService

def test_team_bonding_plans_with_logging():
    """Test the generate_team_bonding_plans method with comprehensive logging."""
    
    print("🧪 Testing generate_team_bonding_plans with logging...")
    print("=" * 60)
    
    # Sample team profiles
    team_profiles = [
        {
            "name": "Alice",
            "vibe": "energetic",
            "location": "District 1",
            "preferences": ["food", "music"]
        },
        {
            "name": "Bob",
            "vibe": "chill",
            "location": "District 2",
            "preferences": ["cafe", "quiet"]
        },
        {
            "name": "Charlie",
            "vibe": "adventurous",
            "location": "District 3",
            "preferences": ["outdoor", "sports"]
        }
    ]
    
    # Initialize AI service
    print("\n🔧 Initializing AI Service...")
    ai_service = AIService(provider='auto')
    
    # Test parameters
    monthly_theme = "fun"
    optional_contribution = 50000  # 50,000 VND
    preferred_date = "2024-01-15"
    preferred_location_zone = "District 1"
    
    print(f"\n📊 Test Parameters:")
    print(f"   Theme: {monthly_theme}")
    print(f"   Optional contribution: {optional_contribution:,} VND")
    print(f"   Preferred date: {preferred_date}")
    print(f"   Preferred location: {preferred_location_zone}")
    print(f"   Team members: {len(team_profiles)}")
    
    try:
        # Generate team bonding plans
        print(f"\n🚀 Calling generate_team_bonding_plans...")
        plans = ai_service.generate_team_bonding_plans(
            team_profiles=team_profiles,
            monthly_theme=monthly_theme,
            optional_contribution=optional_contribution,
            preferred_date=preferred_date,
            preferred_location_zone=preferred_location_zone
        )
        
        print(f"\n✅ Successfully generated {len(plans)} plans!")
        
        # Display results
        for i, plan in enumerate(plans, 1):
            print(f"\n📋 Plan {i}:")
            print(f"   ID: {plan.get('id', 'N/A')}")
            print(f"   Title: {plan.get('title', 'N/A')}")
            print(f"   Theme: {plan.get('theme', 'N/A')}")
            print(f"   Total Cost: {plan.get('totalCost', 0):,} VND")
            print(f"   Phases: {len(plan.get('phases', []))}")
            
            validation = plan.get('constraintValidation', {})
            print(f"   Validation:")
            print(f"     - Budget compliant: {validation.get('budgetCompliant', False)}")
            print(f"     - Distance compliant: {validation.get('distanceCompliant', False)}")
            print(f"     - Travel time compliant: {validation.get('travelTimeCompliant', False)}")
            
            # Show phases
            for j, phase in enumerate(plan.get('phases', []), 1):
                print(f"     Phase {j}: {phase.get('name', 'N/A')} - {phase.get('cost', 0):,} VND")
        
    except Exception as e:
        print(f"\n❌ Error occurred: {e}")
        print(f"   Exception type: {type(e).__name__}")
        import traceback
        traceback.print_exc()

def test_provider_availability():
    """Test which AI providers are available."""
    print("\n🔍 Testing AI Provider Availability...")
    print("=" * 40)
    
    ai_service = AIService(provider='auto')
    available_providers = ai_service.get_available_providers()
    
    print(f"Available providers: {available_providers}")
    print(f"Current provider: {ai_service.provider_name}")
    
    if ai_service.current_provider:
        print(f"Provider available: {ai_service.current_provider.is_available()}")
    else:
        print("No provider available")

def test_different_logging_levels():
    """Test different logging levels to see the difference in output."""
    print("\n🔧 Testing Different Logging Levels...")
    print("=" * 50)
    
    # Test with INFO level
    print("\n📝 Testing with INFO level:")
    setup_logging(level="INFO")
    ai_service = AIService(provider='auto')
    
    # Test with DEBUG level
    print("\n📝 Testing with DEBUG level:")
    setup_logging(level="DEBUG")
    ai_service = AIService(provider='auto')

if __name__ == "__main__":
    print("🧪 AI Service Logging Test")
    print("=" * 60)
    
    # Choose logging level based on command line argument
    if len(sys.argv) > 1:
        log_level = sys.argv[1].upper()
        if log_level == "DEBUG":
            setup_debug_logging()
        elif log_level == "DEVELOPMENT":
            setup_development_logging()
        else:
            setup_logging(level=log_level)
    else:
        # Default to INFO level
        setup_logging(level="INFO")
    
    # Test provider availability first
    test_provider_availability()
    
    # Test the main flow
    test_team_bonding_plans_with_logging()
    
    print("\n✅ Test completed!")
    print("\n💡 Usage tips:")
    print("   - Run with 'python test_logging.py DEBUG' for maximum verbosity")
    print("   - Run with 'python test_logging.py WARNING' for minimal output")
    print("   - Check the generated log files for detailed information") 