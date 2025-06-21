#!/usr/bin/env python3
"""
Simple test script to verify AI providers are working
"""

import os
import sys
from dotenv import load_dotenv
from services.ai_service import AIService, OpenAIProvider, GoogleAIProvider

def test_openai_provider():
    """Test OpenAI provider directly"""
    print("🧪 Testing OpenAI Provider...")
    
    provider = OpenAIProvider()
    print(f"   Available: {provider.is_available()}")
    
    if provider.is_available():
        try:
            response = provider.generate_response(
                prompt="Hello! Please respond with 'OpenAI is working!'",
                system_prompt="You are a helpful assistant. Keep responses short.",
                max_tokens=50
            )
            print(f"   ✅ Response: {response}")
            return True
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return False
    else:
        print("   ⚠️ OpenAI not available")
        return False

def test_google_ai_provider():
    """Test Google AI provider directly"""
    print("🧪 Testing Google AI Provider...")
    
    provider = GoogleAIProvider()
    print(f"   Available: {provider.is_available()}")
    
    if provider.is_available():
        try:
            response = provider.generate_response(
                prompt="Hello! Please respond with 'Google AI is working!'",
                system_prompt="You are a helpful assistant. Keep responses short.",
                max_tokens=50
            )
            print(f"   ✅ Response: {response}")
            return True
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return False
    else:
        print("   ⚠️ Google AI not available")
        return False

def test_ai_service():
    """Test the main AI service"""
    print("🧪 Testing AI Service...")
    
    ai_service = AIService(provider='auto')
    print(f"   Current provider: {ai_service.provider_name}")
    print(f"   Available providers: {ai_service.get_available_providers()}")
    
    if ai_service.current_provider:
        try:
            response = ai_service.current_provider.generate_response(
                prompt="Hello! Please respond with 'AI Service is working!'",
                system_prompt="You are a helpful assistant. Keep responses short.",
                max_tokens=50
            )
            print(f"   ✅ Response: {response}")
            return True
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return False
    else:
        print("   ❌ No AI providers available")
        return False

def main():
    """Run all tests"""
    print("🚀 AI API Test Suite")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Check environment variables
    openai_key = os.getenv('OPENAI_API_KEY', '')
    google_key = os.getenv('GOOGLE_AI_API_KEY', '')
    
    print(f"🔑 OpenAI API Key: {'✅ Set' if openai_key and openai_key != 'your_openai_api_key_here' else '❌ Not set'}")
    print(f"🔑 Google AI API Key: {'✅ Set' if google_key and google_key != 'your_google_ai_api_key_here' else '❌ Not set'}")
    print()
    
    # Run tests
    openai_works = test_openai_provider()
    print()
    
    google_works = test_google_ai_provider()
    print()
    
    service_works = test_ai_service()
    print()
    
    # Summary
    print("📊 Test Results:")
    print(f"   OpenAI: {'✅ Working' if openai_works else '❌ Failed'}")
    print(f"   Google AI: {'✅ Working' if google_works else '❌ Failed'}")
    print(f"   AI Service: {'✅ Working' if service_works else '❌ Failed'}")
    
    if openai_works or google_works:
        print("\n🎉 At least one AI provider is working!")
    else:
        print("\n❌ No AI providers are working. Please check your API keys.")

if __name__ == "__main__":
    main() 