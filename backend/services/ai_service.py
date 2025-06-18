import openai
import anthropic
import google.generativeai as genai
import requests
import json
import time
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from config import AI_CONFIG, OPENAI_API_KEY, ANTHROPIC_API_KEY, GOOGLE_AI_API_KEY
from .ai_model_manager import AIModelManager

class AIProvider(ABC):
    """Abstract base class for AI providers."""
    
    @abstractmethod
    def generate_response(self, prompt: str, system_prompt: str = None, **kwargs) -> str:
        """Generate a response from the AI model."""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if the provider is available."""
        pass

class OpenAIProvider(AIProvider):
    """OpenAI API provider implementation."""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or OPENAI_API_KEY
        if self.api_key:
            openai.api_key = self.api_key
    
    def is_available(self) -> bool:
        return bool(self.api_key)
    
    def generate_response(self, prompt: str, system_prompt: str = None, **kwargs) -> str:
        if not self.is_available():
            raise Exception("OpenAI API key not configured")
        
        model = kwargs.get('model', AI_CONFIG['models']['openai']['default'])
        temperature = kwargs.get('temperature', AI_CONFIG['settings']['temperature'])
        max_tokens = kwargs.get('max_tokens', AI_CONFIG['settings']['max_tokens'])
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        try:
            response = openai.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")

class AnthropicProvider(AIProvider):
    """Anthropic Claude API provider implementation."""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or ANTHROPIC_API_KEY
        self.client = None
        if self.api_key:
            self.client = anthropic.Anthropic(api_key=self.api_key)
    
    def is_available(self) -> bool:
        return bool(self.api_key and self.client)
    
    def generate_response(self, prompt: str, system_prompt: str = None, **kwargs) -> str:
        if not self.is_available():
            raise Exception("Anthropic API key not configured")
        
        model = kwargs.get('model', AI_CONFIG['models']['anthropic']['default'])
        temperature = kwargs.get('temperature', AI_CONFIG['settings']['temperature'])
        max_tokens = kwargs.get('max_tokens', AI_CONFIG['settings']['max_tokens'])
        
        try:
            response = self.client.messages.create(
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system_prompt or "You are a helpful AI assistant.",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        except Exception as e:
            raise Exception(f"Anthropic API error: {str(e)}")

class GoogleAIProvider(AIProvider):
    """Google AI (Gemini) provider implementation."""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or GOOGLE_AI_API_KEY
        if self.api_key:
            genai.configure(api_key=self.api_key)
    
    def is_available(self) -> bool:
        return bool(self.api_key)
    
    def generate_response(self, prompt: str, system_prompt: str = None, **kwargs) -> str:
        if not self.is_available():
            raise Exception("Google AI API key not configured")
        
        model_name = kwargs.get('model', AI_CONFIG['models']['google']['default'])
        temperature = kwargs.get('temperature', AI_CONFIG['settings']['temperature'])
        
        try:
            model = genai.GenerativeModel(model_name)
            
            # Combine system prompt and user prompt
            full_prompt = prompt
            if system_prompt:
                full_prompt = f"{system_prompt}\n\n{prompt}"
            
            response = model.generate_content(
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=temperature,
                    max_output_tokens=kwargs.get('max_tokens', AI_CONFIG['settings']['max_tokens'])
                )
            )
            return response.text
        except Exception as e:
            raise Exception(f"Google AI API error: {str(e)}")

class AIService:
    """Main AI service that manages multiple providers."""
    
    def __init__(self, provider: str = 'auto'):
        self.provider_name = provider
        self.providers = {
            'openai': OpenAIProvider(),
            'anthropic': AnthropicProvider(),
            'google': GoogleAIProvider()
        }
        self.current_provider = None
        self.model_manager = AIModelManager()
        self._initialize_provider()
    
    def _initialize_provider(self):
        """Initialize the AI provider based on configuration."""
        if self.provider_name == 'auto':
            # Check if performance-based selection is enabled
            if self.model_manager.model_preferences.get('performance_based', True):
                best_provider = self.model_manager.get_best_performing_model()
                if best_provider and self.providers[best_provider].is_available():
                    self.current_provider = self.providers[best_provider]
                    self.provider_name = best_provider
                    return
            
            # Try default provider first, then fallback
            default_provider = AI_CONFIG['default_provider']
            fallback_provider = AI_CONFIG['fallback_provider']
            
            if self.providers[default_provider].is_available():
                self.current_provider = self.providers[default_provider]
                self.provider_name = default_provider
            elif self.providers[fallback_provider].is_available():
                self.current_provider = self.providers[fallback_provider]
                self.provider_name = fallback_provider
            else:
                # Try any available provider
                for name, provider in self.providers.items():
                    if provider.is_available():
                        self.current_provider = provider
                        self.provider_name = name
                        break
        else:
            if self.provider_name in self.providers:
                self.current_provider = self.providers[self.provider_name]
    
    def get_available_providers(self) -> List[str]:
        """Get list of available AI providers."""
        return [name for name, provider in self.providers.items() if provider.is_available()]
    
    def switch_provider(self, provider_name: str) -> bool:
        """Switch to a different AI provider."""
        if provider_name in self.providers and self.providers[provider_name].is_available():
            self.current_provider = self.providers[provider_name]
            self.provider_name = provider_name
            return True
        return False
    
    def generate_activity_suggestions(self, team_data: Dict, free_slots: List, central_location: Dict) -> List[Dict]:
        """Generate activity suggestions using the current AI provider."""
        try:
            if not self.current_provider:
                return self._generate_fallback_suggestions(team_data)
            
            prompt = self._create_prompt(team_data, free_slots, central_location)
            system_prompt = "You are a team bonding activity expert. Provide suggestions in a structured format."
            
            # Try with current provider
            try:
                start_time = time.time()
                response = self.current_provider.generate_response(
                    prompt=prompt,
                    system_prompt=system_prompt,
                    temperature=0.7,
                    max_tokens=800
                )
                response_time = time.time() - start_time
                
                # Record successful performance
                self.model_manager.record_performance(
                    provider=self.provider_name,
                    model=AI_CONFIG['models'][self.provider_name]['default'],
                    response_time=response_time,
                    success=True
                )
                
                return self._parse_suggestions(response)
            except Exception as e:
                response_time = time.time() - start_time if 'start_time' in locals() else 0
                
                # Record failed performance
                self.model_manager.record_performance(
                    provider=self.provider_name,
                    model=AI_CONFIG['models'][self.provider_name]['default'],
                    response_time=response_time,
                    success=False,
                    error_message=str(e)
                )
                
                print(f"Error with {self.provider_name}: {str(e)}")
                
                # Try fallback provider
                fallback_provider = AI_CONFIG['fallback_provider']
                if fallback_provider != self.provider_name and self.providers[fallback_provider].is_available():
                    try:
                        self.current_provider = self.providers[fallback_provider]
                        self.provider_name = fallback_provider
                        
                        start_time = time.time()
                        response = self.current_provider.generate_response(
                            prompt=prompt,
                            system_prompt=system_prompt,
                            temperature=0.7,
                            max_tokens=800
                        )
                        response_time = time.time() - start_time
                        
                        # Record successful fallback performance
                        self.model_manager.record_performance(
                            provider=self.provider_name,
                            model=AI_CONFIG['models'][self.provider_name]['default'],
                            response_time=response_time,
                            success=True
                        )
                        
                        return self._parse_suggestions(response)
                    except Exception as fallback_error:
                        response_time = time.time() - start_time if 'start_time' in locals() else 0
                        
                        # Record failed fallback performance
                        self.model_manager.record_performance(
                            provider=self.provider_name,
                            model=AI_CONFIG['models'][self.provider_name]['default'],
                            response_time=response_time,
                            success=False,
                            error_message=str(fallback_error)
                        )
                        
                        print(f"Fallback provider error: {str(fallback_error)}")
                
                return self._generate_fallback_suggestions(team_data)
                
        except Exception as e:
            print(f"AI suggestion error: {str(e)}")
            return self._generate_fallback_suggestions(team_data)
    
    def get_performance_stats(self, time_window_hours: int = 24) -> Dict[str, Any]:
        """Get performance statistics for all providers."""
        return self.model_manager.get_performance_stats(time_window_hours)
    
    def get_model_recommendations(self, use_case: str = 'general') -> Dict[str, Any]:
        """Get model recommendations based on use case and performance."""
        return self.model_manager.get_model_recommendations(use_case)
    
    def setup_ab_test(self, test_name: str, providers: List[str], 
                     traffic_split: Dict[str, float] = None):
        """Setup A/B testing configuration."""
        self.model_manager.setup_ab_test(test_name, providers, traffic_split)
    
    def get_ab_test_provider(self, test_name: str) -> Optional[str]:
        """Get provider for A/B testing."""
        return self.model_manager.get_ab_test_provider(test_name)
    
    def get_ab_test_results(self, test_name: str) -> Optional[Dict[str, Any]]:
        """Get A/B test results."""
        return self.model_manager.get_ab_test_results(test_name)
    
    def _create_prompt(self, team_data: Dict, free_slots: List, central_location: Dict) -> str:
        """Create a prompt for the AI model."""
        prompt = f"""
        Based on the following team information, suggest 3-5 team bonding activities:

        Team Preferences:
        - Interests: {', '.join(team_data['interests'])}
        - Budget per person: ${team_data['budget']}
        - Group size: {team_data['group_size']} people
        - Location: {central_location.get('formatted_address', 'Unknown location')}

        Available Time Slots:
        {self._format_time_slots(free_slots)}

        Please suggest activities that:
        1. Match the team's interests and budget
        2. Are suitable for the group size
        3. Are accessible from the central location
        4. Can be completed within the available time slots

        For each suggestion, provide the information in this exact format:
        - Activity Name: [name]
        - Estimated Cost: [cost per person]
        - Duration: [duration]
        - Description: [why it's a good fit]
        - Category: [indoor/outdoor/hybrid]

        Format each activity as a separate section with clear labels.
        """
        return prompt

    def _format_time_slots(self, free_slots: List) -> str:
        """Format time slots for the prompt."""
        if not free_slots:
            return "No specific time slots available"
        
        formatted_slots = []
        for slot in free_slots:
            start = slot['start'].strftime('%Y-%m-%d %H:%M')
            end = slot['end'].strftime('%Y-%m-%d %H:%M')
            formatted_slots.append(f"- {start} to {end}")
        return '\n'.join(formatted_slots)

    def _parse_suggestions(self, ai_response: str) -> List[Dict]:
        """Parse the AI response into structured suggestions."""
        suggestions = []
        current_suggestion = {}
        
        lines = ai_response.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                if current_suggestion and len(current_suggestion) > 1:
                    suggestions.append(current_suggestion)
                    current_suggestion = {}
                continue
            
            # Look for key-value pairs
            if ':' in line:
                parts = line.split(':', 1)
                if len(parts) == 2:
                    key = parts[0].strip().lower().replace(' ', '_')
                    value = parts[1].strip()
                    
                    # Clean up common variations
                    if 'activity' in key or 'name' in key:
                        key = 'name'
                    elif 'cost' in key:
                        key = 'cost'
                    elif 'duration' in key:
                        key = 'duration'
                    elif 'description' in key:
                        key = 'description'
                    elif 'category' in key:
                        key = 'category'
                    
                    current_suggestion[key] = value
        
        # Add the last suggestion if it exists
        if current_suggestion and len(current_suggestion) > 1:
            suggestions.append(current_suggestion)
        
        # If parsing failed, try alternative parsing
        if not suggestions:
            suggestions = self._alternative_parse_suggestions(ai_response)
        
        return suggestions

    def _alternative_parse_suggestions(self, ai_response: str) -> List[Dict]:
        """Alternative parsing method for different response formats."""
        suggestions = []
        
        # Split by common separators
        sections = ai_response.split('\n\n')
        for section in sections:
            if not section.strip():
                continue
            
            suggestion = {}
            lines = section.split('\n')
            for line in lines:
                line = line.strip()
                if line.startswith('-') or line.startswith('•'):
                    if 'name' not in suggestion:
                        suggestion['name'] = line[1:].strip()
                elif ':' in line:
                    parts = line.split(':', 1)
                    if len(parts) == 2:
                        key = parts[0].strip().lower().replace(' ', '_')
                        value = parts[1].strip()
                        suggestion[key] = value
            
            if suggestion and 'name' in suggestion:
                suggestions.append(suggestion)
        
        return suggestions

    def _generate_fallback_suggestions(self, team_data: Dict) -> List[Dict]:
        """Generate fallback suggestions when AI is unavailable."""
        suggestions = []
        interests = team_data['interests']
        budget = team_data['budget']
        group_size = team_data['group_size']
        
        # Enhanced fallback suggestions based on interests
        interest_activities = {
            'hiking': {
                'name': 'Group Hiking Adventure',
                'cost': 'Free - $20 per person',
                'duration': '2-4 hours',
                'description': 'Explore scenic trails suitable for team bonding',
                'category': 'outdoor'
            },
            'games': {
                'name': 'Board Game & Strategy Night',
                'cost': '$10-30 per person',
                'duration': '3-4 hours',
                'description': 'Fun team games with snacks and drinks',
                'category': 'indoor'
            },
            'dining': {
                'name': 'Team Dinner & Social',
                'cost': f'${budget} per person',
                'duration': '2-3 hours',
                'description': 'Casual dinner at a local restaurant',
                'category': 'indoor'
            },
            'sports': {
                'name': 'Team Sports Activity',
                'cost': '$15-40 per person',
                'duration': '2-3 hours',
                'description': 'Engage in team sports like volleyball or soccer',
                'category': 'outdoor'
            },
            'creative': {
                'name': 'Creative Workshop',
                'cost': '$20-50 per person',
                'duration': '2-3 hours',
                'description': 'Art, cooking, or craft workshop',
                'category': 'indoor'
            }
        }
        
        # Add suggestions based on interests
        for interest in interests:
            if interest.lower() in interest_activities:
                suggestions.append(interest_activities[interest.lower()])
        
        # Add generic suggestions if not enough specific ones
        if len(suggestions) < 3:
            suggestions.extend([
                {
                    'name': 'Team Building Workshop',
                    'cost': '$25-60 per person',
                    'duration': '3-4 hours',
                    'description': 'Professional team building activities',
                    'category': 'indoor'
                },
                {
                    'name': 'Outdoor Adventure',
                    'cost': '$30-80 per person',
                    'duration': '4-6 hours',
                    'description': 'Adventure activities like zip-lining or rock climbing',
                    'category': 'outdoor'
                }
            ])
        
        return suggestions[:5]  # Return max 5 suggestions 