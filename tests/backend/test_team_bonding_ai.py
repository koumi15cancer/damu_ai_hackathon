#!/usr/bin/env python3
"""
Test script for the enhanced Team Bonding AI integration.
This script tests the new AI-powered team bonding event planning features.
"""

import os
import sys
import json
import time
from pathlib import Path

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.ai_service import AIService
from config import AI_CONFIG

def test_team_bonding_plan_generation():
    """Test the enhanced team bonding plan generation."""
    print("🎉 Testing Enhanced Team Bonding Plan Generation")
    print("=" * 60)
    
    # Initialize AI service
    ai_service = AIService(provider='auto')
    
    # Check available providers
    providers = ai_service.get_available_providers()
    print(f"Available AI providers: {providers}")
    print(f"Current provider: {ai_service.provider_name}")
    
    if not providers:
        print("❌ No AI providers available. Please configure API keys in .env file")
        return False
    
    # Load team profiles
    try:
        with open('team_profiles.json', 'r', encoding='utf-8') as f:
            team_profiles = json.load(f)
        print(f"✅ Loaded {len(team_profiles)} team profiles")
    except Exception as e:
        print(f"❌ Failed to load team profiles: {e}")
        return False
    
    # Test different themes and scenarios
    test_scenarios = [
        {
            'name': 'Fun Theme with Budget',
            'monthly_theme': 'fun',
            'optional_contribution': 100000,
            'preferred_location_zone': 'District 1',
            'available_members': ['Ben', 'Cody', 'Big Thanh']
        },
        {
            'name': 'Chill Theme No Budget',
            'monthly_theme': 'chill',
            'optional_contribution': 0,
            'preferred_location_zone': None,
            'available_members': ['Lil Thanh', 'Hoa', 'Mason']
        },
        {
            'name': 'Outdoor Theme with High Budget',
            'monthly_theme': 'outdoor',
            'optional_contribution': 150000,
            'preferred_location_zone': 'District 7',
            'available_members': ['Khang', 'Seven', 'Roy']
        }
    ]
    
    success_count = 0
    
    for scenario in test_scenarios:
        print(f"\n🧪 Testing: {scenario['name']}")
        print("-" * 40)
        
        try:
            # Filter team members for this scenario
            filtered_profiles = [member for member in team_profiles 
                               if member['name'] in scenario['available_members']]
            
            start_time = time.time()
            
            # Generate plans using the enhanced AI service
            plans = ai_service.generate_team_bonding_plans(
                team_profiles=filtered_profiles,
                monthly_theme=scenario['monthly_theme'],
                optional_contribution=scenario['optional_contribution'],
                preferred_date="2024-01-15",
                preferred_location_zone=scenario['preferred_location_zone']
            )
            
            generation_time = time.time() - start_time
            
            if plans and len(plans) > 0:
                print(f"✅ Generated {len(plans)} plans in {generation_time:.2f}s")
                
                # Validate the first plan
                first_plan = plans[0]
                print(f"   Plan: {first_plan.get('title', 'Untitled')}")
                print(f"   Theme: {first_plan.get('theme', 'Unknown')}")
                print(f"   Phases: {len(first_plan.get('phases', []))}")
                print(f"   Total Cost: {first_plan.get('totalCost', 0):,} VND")
                
                # Check constraint validation
                validation = first_plan.get('constraintValidation', {})
                print(f"   Budget Compliant: {validation.get('budgetCompliant', False)}")
                print(f"   Distance Compliant: {validation.get('distanceCompliant', False)}")
                print(f"   Travel Time Compliant: {validation.get('travelTimeCompliant', False)}")
                
                success_count += 1
            else:
                print("❌ No plans generated")
                
        except Exception as e:
            print(f"❌ Error generating plans: {e}")
    
    print(f"\n📊 Results: {success_count}/{len(test_scenarios)} scenarios successful")
    return success_count == len(test_scenarios)

def test_constraint_validation():
    """Test the constraint validation logic."""
    print("\n🔍 Testing Constraint Validation")
    print("=" * 40)
    
    ai_service = AIService(provider='auto')
    
    # Test data with known constraints
    test_plans = [
        {
            'id': 'test_1',
            'title': 'Valid Plan',
            'totalCost': 250000,
            'phases': [
                {'distance': 1.5, 'travelTime': 10},
                {'distance': 0.8, 'travelTime': 5}
            ]
        },
        {
            'id': 'test_2',
            'title': 'Invalid Budget Plan',
            'totalCost': 600000,
            'phases': [
                {'distance': 1.0, 'travelTime': 8},
                {'distance': 1.2, 'travelTime': 12}
            ]
        },
        {
            'id': 'test_3',
            'title': 'Invalid Distance Plan',
            'totalCost': 200000,
            'phases': [
                {'distance': 3.0, 'travelTime': 20},
                {'distance': 2.5, 'travelTime': 18}
            ]
        }
    ]
    
    for plan in test_plans:
        validated_plans = ai_service._validate_plans_against_constraints([plan], 0)
        validation = validated_plans[0].get('constraintValidation', {})
        
        print(f"\nPlan: {plan['title']}")
        print(f"  Budget: {plan['totalCost']:,} VND (Compliant: {validation.get('budgetCompliant', False)})")
        print(f"  Distance: {validation.get('distanceCompliant', False)}")
        print(f"  Travel Time: {validation.get('travelTimeCompliant', False)}")

def test_prompt_construction():
    """Test the prompt construction logic."""
    print("\n📝 Testing Prompt Construction")
    print("=" * 40)
    
    ai_service = AIService(provider='auto')
    
    # Sample team profiles
    team_profiles = [
        {
            'name': 'Ben',
            'location': 'Mizuki Park, Binh Chanh',
            'preferences': ['Vegetarian', 'Chill places', 'Cafe-hopping'],
            'vibe': 'Chill'
        },
        {
            'name': 'Cody',
            'location': 'Huynh Tan Phat, D7',
            'preferences': ['Meat-lover', 'BBQ', 'Bar/beer club', 'Karaoke'],
            'vibe': 'Energetic'
        }
    ]
    
    # Test prompt construction
    prompt = ai_service._construct_team_bonding_prompt(
        team_profiles=team_profiles,
        monthly_theme='fun',
        optional_contribution=100000,
        preferred_date='2024-01-15',
        preferred_location_zone='District 1'
    )
    
    print("Generated prompt preview:")
    print("-" * 30)
    print(prompt[:500] + "..." if len(prompt) > 500 else prompt)
    print("-" * 30)
    
    # Check if key elements are present
    required_elements = [
        'fun 🎉',
        '100,000',
        'District 1',
        '2024-01-15',
        'Ben',
        'Cody',
        '300,000 VND',
        '2 km'
    ]
    
    missing_elements = []
    for element in required_elements:
        if element not in prompt:
            missing_elements.append(element)
    
    if missing_elements:
        print(f"❌ Missing elements: {missing_elements}")
        return False
    else:
        print("✅ All required elements present in prompt")
        return True

def test_response_parsing():
    """Test the AI response parsing logic."""
    print("\n🔧 Testing Response Parsing")
    print("=" * 40)
    
    ai_service = AIService(provider='auto')
    
    # Test JSON response parsing
    test_responses = [
        # Valid JSON response
        '''```json
{
  "plans": [
    {
      "id": "plan_1",
      "title": "Test Plan",
      "theme": "fun",
      "phases": [
        {
          "name": "Dinner",
          "cost": 250000
        }
      ],
      "totalCost": 250000
    }
  ]
}```''',
        
        # JSON without code blocks
        '''{
  "plans": [
    {
      "id": "plan_2",
      "title": "Another Plan",
      "theme": "chill"
    }
  ]
}''',
        
        # Invalid response
        "This is not a valid JSON response"
    ]
    
    for i, response in enumerate(test_responses, 1):
        print(f"\nTest {i}:")
        try:
            plans = ai_service._parse_team_bonding_response(response)
            if plans:
                print(f"  ✅ Parsed {len(plans)} plans")
                if isinstance(plans, list) and len(plans) > 0:
                    print(f"  First plan: {plans[0].get('title', 'Untitled')}")
            else:
                print("  ❌ No plans parsed")
        except Exception as e:
            print(f"  ❌ Parsing error: {e}")

def test_performance_monitoring():
    """Test performance monitoring features."""
    print("\n📊 Testing Performance Monitoring")
    print("=" * 40)
    
    ai_service = AIService(provider='auto')
    
    # Get performance stats
    stats = ai_service.get_performance_stats(time_window_hours=24)
    print(f"Performance stats: {json.dumps(stats, indent=2)}")
    
    # Get model recommendations
    recommendations = ai_service.get_model_recommendations('team_bonding')
    print(f"Model recommendations: {json.dumps(recommendations, indent=2)}")

def main():
    """Main test function."""
    print("🤖 Enhanced Team Bonding AI Integration Test")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not Path('app.py').exists():
        print("❌ Please run this script from the backend directory")
        print("   cd backend && python3 test_team_bonding_ai.py")
        sys.exit(1)
    
    # Check if .env file exists
    if not Path('.env').exists():
        print("❌ No .env file found. Please run setup_ai.py first")
        print("   python3 setup_ai.py")
        sys.exit(1)
    
    # Run tests
    tests = [
        ("Team Bonding Plan Generation", test_team_bonding_plan_generation),
        ("Constraint Validation", test_constraint_validation),
        ("Prompt Construction", test_prompt_construction),
        ("Response Parsing", test_response_parsing),
        ("Performance Monitoring", test_performance_monitoring)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*60}")
        print(f"Running: {test_name}")
        print(f"{'='*60}")
        
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print(f"\n{'='*60}")
    print("📋 TEST SUMMARY")
    print(f"{'='*60}")
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\n🎉 All tests passed! Your AI integration is working correctly.")
    else:
        print(f"\n⚠️  {len(results) - passed} tests failed. Check your configuration.")
    
    return passed == len(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 