#!/usr/bin/env python3
"""
Test script for the enhanced AI integration system.
This script demonstrates the multi-provider AI features.
"""

import os
import sys
import time
import json
from dotenv import load_dotenv

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.ai_service import AIService
from config import AI_CONFIG

def test_basic_functionality():
    """Test basic AI service functionality."""
    print("🧪 Testing Basic AI Service Functionality")
    print("=" * 50)
    
    # Initialize AI service
    ai_service = AIService(provider='auto')
    
    # Get available providers
    providers = ai_service.get_available_providers()
    print(f"Available providers: {providers}")
    print(f"Current provider: {ai_service.provider_name}")
    
    # Test provider switching
    if len(providers) > 1:
        other_provider = [p for p in providers if p != ai_service.provider_name][0]
        print(f"\nSwitching to {other_provider}...")
        success = ai_service.switch_provider(other_provider)
        print(f"Switch successful: {success}")
        print(f"Current provider: {ai_service.provider_name}")
    
    print("\n✅ Basic functionality test completed\n")

def test_performance_tracking():
    """Test performance tracking features."""
    print("📊 Testing Performance Tracking")
    print("=" * 50)
    
    ai_service = AIService(provider='auto')
    
    # Generate some test data by making requests
    test_prompts = [
        "Hello, this is a test prompt.",
        "Can you provide a brief response?",
        "Testing the AI service functionality."
    ]
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"Making test request {i}/3...")
        try:
            start_time = time.time()
            response = ai_service.current_provider.generate_response(
                prompt=prompt,
                system_prompt="You are a helpful AI assistant. Provide brief responses.",
                temperature=0.7,
                max_tokens=50
            )
            response_time = time.time() - start_time
            
            # Record performance manually for testing
            ai_service.model_manager.record_performance(
                provider=ai_service.provider_name,
                model=AI_CONFIG['models'][ai_service.provider_name]['default'],
                response_time=response_time,
                success=True
            )
            
            print(f"  Response: {response[:50]}...")
            print(f"  Response time: {response_time:.2f}s")
            
        except Exception as e:
            print(f"  Error: {str(e)}")
            ai_service.model_manager.record_performance(
                provider=ai_service.provider_name,
                model=AI_CONFIG['models'][ai_service.provider_name]['default'],
                response_time=0,
                success=False,
                error_message=str(e)
            )
    
    # Get performance stats
    stats = ai_service.get_performance_stats(time_window_hours=1)
    print(f"\nPerformance stats: {json.dumps(stats, indent=2)}")
    
    print("\n✅ Performance tracking test completed\n")

def test_ab_testing():
    """Test A/B testing features."""
    print("🧪 Testing A/B Testing Features")
    print("=" * 50)
    
    ai_service = AIService(provider='auto')
    available_providers = ai_service.get_available_providers()
    
    if len(available_providers) < 2:
        print("⚠️  Need at least 2 providers for A/B testing")
        return
    
    # Setup A/B test
    test_name = "demo_test"
    providers = available_providers[:2]  # Use first 2 providers
    traffic_split = {providers[0]: 0.6, providers[1]: 0.4}
    
    print(f"Setting up A/B test: {test_name}")
    print(f"Providers: {providers}")
    print(f"Traffic split: {traffic_split}")
    
    ai_service.setup_ab_test(test_name, providers, traffic_split)
    
    # Simulate some requests
    for i in range(10):
        provider = ai_service.get_ab_test_provider(test_name)
        print(f"Request {i+1}: Selected provider {provider}")
        
        # Record result (simulate success)
        ai_service.model_manager.record_ab_test_result(test_name, provider, True)
    
    # Get A/B test results
    results = ai_service.get_ab_test_results(test_name)
    print(f"\nA/B test results: {json.dumps(results, indent=2)}")
    
    print("\n✅ A/B testing test completed\n")

def test_model_recommendations():
    """Test model recommendation features."""
    print("🎯 Testing Model Recommendations")
    print("=" * 50)
    
    ai_service = AIService(provider='auto')
    
    # Test different use cases
    use_cases = ['general', 'creative', 'analytical', 'multimodal']
    
    for use_case in use_cases:
        recommendations = ai_service.get_model_recommendations(use_case)
        print(f"\nUse case: {use_case}")
        print(f"Recommendations: {json.dumps(recommendations, indent=2)}")
    
    print("\n✅ Model recommendations test completed\n")

def test_activity_suggestions():
    """Test activity suggestions with different providers."""
    print("🎉 Testing Activity Suggestions")
    print("=" * 50)
    
    ai_service = AIService(provider='auto')
    
    # Test data
    team_data = {
        'interests': ['hiking', 'games', 'dining'],
        'budget': 50,
        'group_size': 5
    }
    
    free_slots = [
        {
            'start': time.time() + 86400,  # Tomorrow
            'end': time.time() + 86400 + 14400  # 4 hours later
        }
    ]
    
    central_location = {
        'formatted_address': 'San Francisco, CA'
    }
    
    # Test with current provider
    print(f"Testing with provider: {ai_service.provider_name}")
    try:
        suggestions = ai_service.generate_activity_suggestions(
            team_data, free_slots, central_location
        )
        print(f"Generated {len(suggestions)} suggestions")
        for i, suggestion in enumerate(suggestions[:2], 1):  # Show first 2
            print(f"  {i}. {suggestion.get('name', 'Unknown')}")
    except Exception as e:
        print(f"Error generating suggestions: {str(e)}")
    
    print("\n✅ Activity suggestions test completed\n")

def test_data_export():
    """Test data export functionality."""
    print("📤 Testing Data Export")
    print("=" * 50)
    
    ai_service = AIService(provider='auto')
    
    try:
        filename = ai_service.model_manager.export_performance_data()
        print(f"Performance data exported to: {filename}")
        
        # Check if file exists and has content
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                data = json.load(f)
            print(f"Exported data contains {len(data.get('performance_history', []))} performance records")
        else:
            print("⚠️  Export file not found")
            
    except Exception as e:
        print(f"Error exporting data: {str(e)}")
    
    print("\n✅ Data export test completed\n")

def main():
    """Run all tests."""
    print("🚀 AI Integration Test Suite")
    print("=" * 60)
    
    # Load environment variables
    load_dotenv()
    
    # Check if any AI providers are configured
    required_keys = ['OPENAI_API_KEY', 'ANTHROPIC_API_KEY', 'GOOGLE_AI_API_KEY']
    configured_providers = [key for key in required_keys if os.getenv(key)]
    
    if not configured_providers:
        print("⚠️  No AI provider API keys found in environment variables")
        print("Please set at least one of: OPENAI_API_KEY, ANTHROPIC_API_KEY, GOOGLE_AI_API_KEY")
        return
    
    print(f"Configured providers: {configured_providers}")
    print()
    
    # Run tests
    try:
        test_basic_functionality()
        test_performance_tracking()
        test_ab_testing()
        test_model_recommendations()
        test_activity_suggestions()
        test_data_export()
        
        print("🎉 All tests completed successfully!")
        
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 