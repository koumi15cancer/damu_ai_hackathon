import openai
import google.generativeai as genai
import anthropic
import requests
import json
import time
import re
import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from config import AI_CONFIG, OPENAI_API_KEY, GOOGLE_AI_API_KEY, ANTHROPIC_API_KEY
from .ai_model_manager import AIModelManager

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

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
        logger.debug("🔧 Initializing OpenAI provider")
        self.api_key = api_key or OPENAI_API_KEY or ""
        self.client = None
        
        if self.api_key and self.api_key != 'your_openai_api_key_here':
            try:
                import openai
                # Try to create client with minimal parameters
                self.client = openai.OpenAI(api_key=self.api_key)
                logger.info("✅ OpenAI v1.x client initialized successfully")
            except TypeError as e:
                if "proxies" in str(e):
                    logger.warning("⚠️ Proxies error detected, trying alternative initialization...")
                    try:
                        # Try without any additional parameters
                        import openai
                        self.client = openai.OpenAI()
                        # Set API key after initialization
                        self.client.api_key = self.api_key
                        logger.info("✅ OpenAI client initialized with alternative method")
                    except Exception as e2:
                        logger.error(f"❌ Alternative initialization failed: {e2}")
                        self.api_key = ""
                else:
                    logger.error(f"❌ Failed to initialize OpenAI client: {e}")
                    self.api_key = ""
            except Exception as e:
                logger.error(f"❌ Failed to initialize OpenAI client: {e}")
                self.api_key = ""
        else:
            logger.warning("⚠️ OpenAI API key not configured")
    
    def is_available(self) -> bool:
        available = bool(self.api_key and self.api_key != 'your_openai_api_key_here' and self.client)
        logger.debug(f"🔍 OpenAI provider available: {available}")
        return available
    
    def generate_response(self, prompt: str, system_prompt: str = None, **kwargs) -> str:
        if not self.is_available():
            logger.error("❌ OpenAI API key not configured")
            raise Exception("OpenAI API key not configured")
        
        model = kwargs.get('model', AI_CONFIG['models']['openai']['default'])
        temperature = kwargs.get('temperature', AI_CONFIG['settings']['temperature'])
        max_tokens = kwargs.get('max_tokens', AI_CONFIG['settings']['max_tokens'])
        
        logger.debug(f"🤖 OpenAI request: model={model}, temperature={temperature}, max_tokens={max_tokens}")
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        try:
            logger.debug("🔄 Sending request to OpenAI API...")
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            result = response.choices[0].message.content or ""
            logger.debug(f"✅ OpenAI response received (length: {len(result)} characters)")
            return result
        except Exception as e:
            logger.error(f"❌ OpenAI API error: {str(e)}")
            raise Exception(f"OpenAI API error: {str(e)}")

class GoogleAIProvider(AIProvider):
    """Google AI (Gemini) provider implementation."""
    
    def __init__(self, api_key: str = None):
        logger.debug("🔧 Initializing Google AI provider")
        self.api_key = api_key or GOOGLE_AI_API_KEY or ""
        if self.api_key and self.api_key != 'your_google_ai_api_key_here':
            try:
                genai.configure(api_key=self.api_key)
                logger.info("✅ Google AI provider initialized successfully")
            except Exception as e:
                logger.error(f"❌ Failed to initialize Google AI client: {e}")
                self.api_key = ""
        else:
            logger.warning("⚠️ Google AI API key not configured")
    
    def is_available(self) -> bool:
        available = bool(self.api_key and self.api_key != 'your_google_ai_api_key_here')
        logger.debug(f"🔍 Google AI provider available: {available}")
        return available
    
    def generate_response(self, prompt: str, system_prompt: str = None, **kwargs) -> str:
        if not self.is_available():
            logger.error("❌ Google AI API key not configured")
            raise Exception("Google AI API key not configured")
        
        model_name = kwargs.get('model', AI_CONFIG['models']['google']['default'])
        temperature = kwargs.get('temperature', AI_CONFIG['settings']['temperature'])
        
        logger.debug(f"🤖 Google AI request: model={model_name}, temperature={temperature}")
        
        try:
            model = genai.GenerativeModel(model_name)
            
            # Combine system prompt and user prompt
            full_prompt = prompt
            if system_prompt:
                full_prompt = f"{system_prompt}\n\n{prompt}"
            
            logger.debug("🔄 Sending request to Google AI API...")
            response = model.generate_content(
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=temperature,
                    max_output_tokens=kwargs.get('max_tokens', AI_CONFIG['settings']['max_tokens'])
                )
            )
            result = response.text or ""
            logger.debug(f"✅ Google AI response received (length: {len(result)} characters)")
            return result
        except Exception as e:
            logger.error(f"❌ Google AI API error: {str(e)}")
            raise Exception(f"Google AI API error: {str(e)}")

class AnthropicProvider(AIProvider):
    """Anthropic (Claude) provider implementation."""
    
    def __init__(self, api_key: str = None):
        logger.debug("🔧 Initializing Anthropic provider")
        self.api_key = api_key or ANTHROPIC_API_KEY or ""
        self.client = None
        
        if self.api_key and self.api_key != 'your_anthropic_api_key_here':
            try:
                self.client = anthropic.Client(api_key=self.api_key)
                logger.info("✅ Anthropic provider initialized successfully")
            except Exception as e:
                logger.error(f"❌ Failed to initialize Anthropic client: {e}")
                self.api_key = ""
        else:
            logger.warning("⚠️ Anthropic API key not configured")
    
    def is_available(self) -> bool:
        available = bool(self.api_key and self.api_key != 'your_anthropic_api_key_here' and self.client)
        logger.debug(f"🔍 Anthropic provider available: {available}")
        return available
    
    def generate_response(self, prompt: str, system_prompt: str = None, **kwargs) -> str:
        if not self.is_available():
            logger.error("❌ Anthropic API key not configured")
            raise Exception("Anthropic API key not configured")
        
        model = kwargs.get('model', AI_CONFIG['models']['anthropic']['default'])
        temperature = kwargs.get('temperature', AI_CONFIG['settings']['temperature'])
        max_tokens = kwargs.get('max_tokens', AI_CONFIG['settings']['max_tokens'])
        
        logger.debug(f"🤖 Anthropic request: model={model}, temperature={temperature}, max_tokens={max_tokens}")
        
        try:
            # Prepare messages for Claude
            messages = []
            if system_prompt:
                messages.append({"role": "user", "content": f"System: {system_prompt}\n\nUser: {prompt}"})
            else:
                messages.append({"role": "user", "content": prompt})
            
            logger.debug("🔄 Sending request to Anthropic API...")
            response = self.client.messages.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            result = response.content[0].text or ""
            logger.debug(f"✅ Anthropic response received (length: {len(result)} characters)")
            return result
        except Exception as e:
            logger.error(f"❌ Anthropic API error: {str(e)}")
            raise Exception(f"Anthropic API error: {str(e)}")

class AIService:
    """Main AI service that manages multiple providers with enhanced team bonding capabilities."""
    
    def __init__(self, provider: str = 'auto'):
        logger.info(f"🔧 Initializing AIService with provider: {provider}")
        self.provider_name = provider
        self.providers = {
            'openai': OpenAIProvider(),
            'google': GoogleAIProvider(),
            'anthropic': AnthropicProvider()
        }
        self.current_provider = None
        self.model_manager = AIModelManager()
        self._initialize_provider()
        logger.info(f"✅ AIService initialized with provider: {self.provider_name}")
    
    def _initialize_provider(self):
        """Initialize the AI provider based on configuration."""
        logger.debug("🔧 Initializing AI provider...")
        
        if self.provider_name == 'auto':
            logger.debug("🔄 Auto-selecting best provider...")
            
            # Check if performance-based selection is enabled
            if self.model_manager.model_preferences.get('performance_based', True):
                logger.debug("📊 Using performance-based provider selection")
                best_provider = self.model_manager.get_best_performing_model()
                logger.debug(f"📊 Best performing provider: {best_provider}")
                
                if best_provider and self.providers[best_provider].is_available():
                    self.current_provider = self.providers[best_provider]
                    self.provider_name = best_provider
                    logger.info(f"✅ Selected best performing provider: {best_provider}")
                    return
            
            # Try default provider first, then fallback
            default_provider = AI_CONFIG['default_provider']
            fallback_provider = AI_CONFIG['fallback_provider']
            
            logger.debug(f"🔄 Trying default provider: {default_provider}")
            if self.providers[default_provider].is_available():
                self.current_provider = self.providers[default_provider]
                self.provider_name = default_provider
                logger.info(f"✅ Selected default provider: {default_provider}")
            else:
                logger.debug(f"❌ Default provider {default_provider} not available, trying fallback: {fallback_provider}")
                if self.providers[fallback_provider].is_available():
                    self.current_provider = self.providers[fallback_provider]
                    self.provider_name = fallback_provider
                    logger.info(f"✅ Selected fallback provider: {fallback_provider}")
                else:
                    logger.debug("❌ Both default and fallback providers unavailable, trying any available provider")
                    # Try any available provider
                    for name, provider in self.providers.items():
                        if provider.is_available():
                            self.current_provider = provider
                            self.provider_name = name
                            logger.info(f"✅ Selected available provider: {name}")
                            break
        else:
            logger.debug(f"🔄 Using specified provider: {self.provider_name}")
            if self.provider_name in self.providers:
                self.current_provider = self.providers[self.provider_name]
                logger.info(f"✅ Selected specified provider: {self.provider_name}")
            else:
                logger.error(f"❌ Specified provider {self.provider_name} not found")
        
        if not self.current_provider:
            logger.error("❌ No AI providers available")
        else:
            logger.info(f"✅ Provider initialization complete: {self.provider_name}")
    
    def get_available_providers(self) -> List[str]:
        """Get list of available AI providers."""
        available = [name for name, provider in self.providers.items() if provider.is_available()]
        logger.debug(f"🔍 Available providers: {available}")
        return available
    
    def switch_provider(self, provider_name: str) -> bool:
        """Switch to a different AI provider."""
        logger.info(f"🔄 Attempting to switch to provider: {provider_name}")
        
        if provider_name in self.providers and self.providers[provider_name].is_available():
            self.current_provider = self.providers[provider_name]
            self.provider_name = provider_name
            logger.info(f"✅ Successfully switched to provider: {provider_name}")
            return True
        else:
            logger.warning(f"⚠️ Failed to switch to provider {provider_name}: not available")
            return False
    
    def generate_team_bonding_plans(self, team_profiles: List[Dict], monthly_theme: str, 
                                  optional_contribution: int = 0, preferred_date: str = None, 
                                  preferred_location_zone: str = None) -> List[Dict]:
        """Generate team bonding event plans using AI with enhanced constraints and validation."""
        logger.info("🚀 Starting generate_team_bonding_plans")
        logger.info(f"📊 Input parameters: theme={monthly_theme}, optional_contribution={optional_contribution}, "
                   f"preferred_date={preferred_date}, preferred_location_zone={preferred_location_zone}")
        logger.info(f"👥 Team profiles count: {len(team_profiles)}")
        
        try:
            # Log team profiles for debugging
            for i, profile in enumerate(team_profiles):
                logger.info(f"👤 Team member {i+1}: {profile.get('name', 'Unknown')} - {profile.get('vibe', 'Unknown vibe')} - {profile.get('location', 'Unknown location')}")
            
            # Construct the enhanced prompt
            logger.info("📝 Constructing team bonding prompt...")
            prompt = self._construct_team_bonding_prompt(
                team_profiles=team_profiles,
                monthly_theme=monthly_theme,
                optional_contribution=optional_contribution,
                preferred_date=preferred_date,
                preferred_location_zone=preferred_location_zone
            )
            logger.info(f"📝 Prompt constructed successfully (length: {len(prompt)} characters)")
            
            # Generate response from AI
            if not self.current_provider:
                logger.error("❌ No AI providers available")
                raise Exception("No AI providers available")
            
            logger.info(f"🤖 Using AI provider: {self.provider_name}")
            logger.info(f"🤖 Current provider available: {self.current_provider.is_available()}")
            
            start_time = time.time()
            logger.info("🔄 Generating AI response...")
            response = self.current_provider.generate_response(
                prompt=prompt,
                system_prompt=self._get_team_bonding_system_prompt(),
                temperature=0.7,
                max_tokens=2000
            )
            response_time = time.time() - start_time
            
            logger.info(f"✅ AI response generated successfully in {response_time:.2f} seconds")
            logger.info(f"📄 Response length: {len(response)} characters")
            logger.info(f"📄 Response preview: {response[:200]}...")
            
            # Record performance
            logger.info("📊 Recording performance metrics...")
            self.model_manager.record_performance(
                provider=self.provider_name,
                model=AI_CONFIG['models'][self.provider_name]['default'],
                response_time=response_time,
                success=True
            )
            
            # Parse and validate the response
            logger.info("🔍 Parsing AI response...")
            plans = self._parse_team_bonding_response(response)
            logger.info(f"📋 Parsed {len(plans)} plans from AI response")
            
            # Validate plans against constraints
            logger.info("✅ Validating plans against constraints...")
            validated_plans = self._validate_plans_against_constraints(plans, optional_contribution)
            logger.info(f"✅ Validation complete. Returning {len(validated_plans)} validated plans")
            
            # Log final results summary
            for i, plan in enumerate(validated_plans):
                plan_id = plan.get('id', f'plan_{i+1}')
                title = plan.get('title', 'Unknown')
                total_cost = plan.get('totalCost', 0)
                phases_count = len(plan.get('phases', []))
                validation = plan.get('constraintValidation', {})
                
                logger.info(f"📋 Plan {i+1} ({plan_id}): '{title}' - Cost: {total_cost:,} VND - Phases: {phases_count} - "
                           f"Budget compliant: {validation.get('budgetCompliant', False)}")
            
            return validated_plans
            
        except Exception as e:
            logger.error(f"❌ Error in generate_team_bonding_plans: {str(e)}")
            logger.error(f"❌ Exception type: {type(e).__name__}")
            
            # Record failure
            if self.provider_name:
                logger.info("📊 Recording failure metrics...")
                self.model_manager.record_performance(
                    provider=self.provider_name,
                    model=AI_CONFIG['models'][self.provider_name]['default'],
                    response_time=0,
                    success=False,
                    error_message=str(e)
                )
            raise e
    
    def _get_team_bonding_system_prompt(self) -> str:
        """Get the system prompt for team bonding event planning."""
        logger.debug("📝 Getting team bonding system prompt")
        return """You are an expert team bonding event planner specializing in creating thoughtful, inclusive, and engaging activities for teams in Ho Chi Minh City, Vietnam. You understand local culture, cuisine, and entertainment options.

Your responses must be in valid JSON format with the following structure:
{
  "plans": [
    {
      "id": "plan_1",
      "title": "Event Title",
      "theme": "fun|chill|outdoor",
      "phases": [
        {
          "name": "Activity Name",
          "description": "Detailed description",
          "address": "Full address in Ho Chi Minh City",
          "googleMapsLink": "https://maps.google.com/?q=...",
          "cost": 250000,
          "isIndoor": true,
          "isOutdoor": false,
          "isVegetarianFriendly": true,
          "isAlcoholFriendly": false,
          "travelTime": 10,
          "distance": 1.2
        }
      ],
      "totalCost": 500000,
      "bestFor": ["Member1", "Member2"],
      "rating": 4,
      "fitAnalysis": "Analysis of who this plan suits best",
      "constraintValidation": {
        "budgetCompliant": true,
        "distanceCompliant": true,
        "travelTimeCompliant": true,
        "locationBalanced": true
      }
    }
  ]
}

Always ensure:
1. All costs are in VND (Vietnamese Dong)
2. Addresses are real locations in Ho Chi Minh City
3. Budget constraints are strictly followed
4. Distance and travel time constraints are respected
5. Plans are inclusive and consider dietary preferences
6. JSON is properly formatted and valid"""
    
    def _construct_team_bonding_prompt(self, team_profiles: List[Dict], monthly_theme: str, 
                                     optional_contribution: int, preferred_date: str, 
                                     preferred_location_zone: str) -> str:
        """Construct a comprehensive prompt for team bonding event planning."""
        logger.debug("📝 Constructing team bonding prompt with parameters")
        logger.debug(f"📝 Theme: {monthly_theme}, Optional contribution: {optional_contribution}")
        logger.debug(f"📝 Preferred date: {preferred_date}, Preferred location: {preferred_location_zone}")
        
        # Convert team profiles to readable format
        team_members_info = []
        for member in team_profiles:
            member_info = f"• {member['name']} ({member['vibe']}): {member['location']}"
            if member.get('preferences'):
                member_info += f" - Prefers: {', '.join(member['preferences'])}"
            team_members_info.append(member_info)
        
        team_members_text = "\n".join(team_members_info)
        logger.debug(f"📝 Team members formatted: {len(team_members_info)} members")
        
        # Build location preference text
        location_text = f"Preferred location zone: {preferred_location_zone}" if preferred_location_zone else "No specific location preference"
        
        # Build date preference text
        date_text = f"Preferred date: {preferred_date}" if preferred_date else "No specific date preference"
        
        prompt = f"""
Generate 3-5 team bonding event plans for a team in Ho Chi Minh City, Vietnam.

🎯 EVENT REQUIREMENTS:
• Theme: {monthly_theme} ({'🎉' if monthly_theme == 'fun' else '🧘' if monthly_theme == 'chill' else '🌤'})
• Budget: 300,000 VND/person base + optional {optional_contribution:,} VND contribution
• {location_text}
• {date_text}

💰 BUDGET CONSTRAINTS:
• Phase 1: ≤ 300,000 VND/person
• Phase 2 (optional): Total ≤ 450,000 VND/person
• Phase 3 (optional): Total ≤ 500,000 VND/person

🚶‍♀️ LOGISTICS CONSTRAINTS:
• Each phase within 2 km of others
• Max 15 minutes travel time between phases
• Consider team member home locations for fairness

👥 TEAM MEMBERS:
{team_members_text}

📋 PLAN REQUIREMENTS:
Each plan must include:
1. 1-3 phases (dinner → karaoke → bar style)
2. Real Ho Chi Minh City locations with addresses
3. Cost breakdown per phase
4. Dietary and accessibility notes
5. Travel time and distance between phases
6. Best fit analysis for team members
7. Constraint validation

🎨 THEME GUIDELINES:
• Fun 🎉: Energetic activities, karaoke, bars, games
• Chill 🧘: Cafes, restaurants, movie nights, board games
• Outdoor 🌤: Parks, outdoor dining, walking tours, sports

Please provide the response in the exact JSON format specified in the system prompt.
"""
        
        logger.debug(f"📝 Prompt constructed successfully (length: {len(prompt)} characters)")
        return prompt
    
    def _parse_team_bonding_response(self, ai_response: str) -> List[Dict]:
        """Parse AI response into structured team bonding plans."""
        logger.info("🔍 Starting to parse AI response")
        logger.debug(f"🔍 Response length: {len(ai_response)} characters")
        
        try:
            # Try to extract JSON from the response
            logger.debug("🔍 Attempting to extract JSON from markdown code blocks...")
            json_match = re.search(r'```json\s*(.*?)\s*```', ai_response, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
                logger.info("✅ Found JSON in markdown code blocks")
                logger.debug(f"🔍 Extracted JSON length: {len(json_str)} characters")
                parsed_data = json.loads(json_str)
            else:
                # Try to find JSON in the response
                logger.debug("🔍 No markdown code blocks found, searching for JSON in response...")
                json_start = ai_response.find('{')
                json_end = ai_response.rfind('}') + 1
                if json_start != -1 and json_end != 0:
                    json_str = ai_response[json_start:json_end]
                    logger.info("✅ Found JSON in response body")
                    logger.debug(f"🔍 Extracted JSON length: {len(json_str)} characters")
                    parsed_data = json.loads(json_str)
                else:
                    # If no JSON found, try to parse the entire response
                    logger.debug("🔍 No JSON markers found, attempting to parse entire response...")
                    parsed_data = json.loads(ai_response)
                    logger.info("✅ Parsed entire response as JSON")
            
            # Extract plans from the parsed data
            logger.debug(f"🔍 Parsed data type: {type(parsed_data)}")
            if isinstance(parsed_data, dict) and 'plans' in parsed_data:
                plans = parsed_data['plans']
                logger.info(f"✅ Extracted {len(plans)} plans from 'plans' key")
            elif isinstance(parsed_data, list):
                plans = parsed_data
                logger.info(f"✅ Extracted {len(plans)} plans from list response")
            else:
                logger.error(f"❌ Invalid response format. Expected dict with 'plans' key or list, got {type(parsed_data)}")
                raise ValueError("Invalid response format")
            
            # Log plan details
            for i, plan in enumerate(plans):
                plan_id = plan.get('id', f'unknown_{i}')
                title = plan.get('title', 'Unknown')
                phases_count = len(plan.get('phases', []))
                logger.debug(f"📋 Plan {i+1}: {plan_id} - '{title}' - {phases_count} phases")
            
            return plans
                
        except (json.JSONDecodeError, ValueError) as e:
            logger.error(f"❌ Failed to parse AI response: {e}")
            logger.error(f"❌ Raw response preview: {ai_response[:500]}...")
            logger.info("🔄 Falling back to default plans")
            # Return fallback plans
            return self._generate_fallback_plans()
    
    def _validate_plans_against_constraints(self, plans: List[Dict], optional_contribution: int) -> List[Dict]:
        """Validate plans against budget, distance, and other constraints."""
        logger.info(f"✅ Starting validation of {len(plans)} plans")
        logger.debug(f"✅ Optional contribution: {optional_contribution} VND")
        
        validated_plans = []
        
        for i, plan in enumerate(plans):
            plan_id = plan.get('id', f'plan_{i+1}')
            title = plan.get('title', 'Unknown')
            logger.debug(f"✅ Validating plan {i+1}: {plan_id} - '{title}'")
            
            try:
                # Validate budget constraints
                total_cost = plan.get('totalCost', 0)
                max_budget = 300000 + optional_contribution
                
                budget_compliant = total_cost <= max_budget
                logger.debug(f"💰 Plan {i+1} budget: {total_cost:,} VND (max: {max_budget:,} VND) - Compliant: {budget_compliant}")
                
                # Validate distance and travel time constraints
                phases = plan.get('phases', [])
                distance_compliant = True
                travel_time_compliant = True
                
                logger.debug(f"🚶‍♀️ Plan {i+1} has {len(phases)} phases")
                for j in range(len(phases) - 1):
                    current_phase = phases[j]
                    next_phase = phases[j + 1]
                    
                    distance = current_phase.get('distance', 0)
                    travel_time = current_phase.get('travelTime', 0)
                    
                    logger.debug(f"🚶‍♀️ Phase {j+1} to {j+2}: distance={distance}km, travel_time={travel_time}min")
                    
                    if distance > 2.0:
                        distance_compliant = False
                        logger.debug(f"❌ Distance constraint violated: {distance}km > 2.0km")
                    if travel_time > 15:
                        travel_time_compliant = False
                        logger.debug(f"❌ Travel time constraint violated: {travel_time}min > 15min")
                
                # Add validation results to plan
                validation_result = {
                    'budgetCompliant': budget_compliant,
                    'distanceCompliant': distance_compliant,
                    'travelTimeCompliant': travel_time_compliant,
                    'locationBalanced': True  # Would need more complex logic for full validation
                }
                
                plan['constraintValidation'] = validation_result
                validated_plans.append(plan)
                
                logger.info(f"✅ Plan {i+1} validation complete: Budget={budget_compliant}, Distance={distance_compliant}, TravelTime={travel_time_compliant}")
                
            except Exception as e:
                logger.error(f"❌ Error validating plan {i+1}: {e}")
                # Add plan with validation errors
                plan['constraintValidation'] = {
                    'budgetCompliant': False,
                    'distanceCompliant': False,
                    'travelTimeCompliant': False,
                    'locationBalanced': False,
                    'validationError': str(e)
                }
                validated_plans.append(plan)
        
        logger.info(f"✅ Validation complete for {len(validated_plans)} plans")
        return validated_plans
    
    def _generate_fallback_plans(self) -> List[Dict]:
        """Generate fallback plans when AI parsing fails."""
        logger.info("🔄 Generating fallback plans due to parsing failure")
        return [
            {
                "id": "fallback_1",
                "title": "District 1 Food & Entertainment",
                "theme": "fun",
                "phases": [
                    {
                        "name": "Hotpot Dinner at Pho 24",
                        "description": "Authentic Vietnamese hotpot experience",
                        "address": "123 Nguyen Hue, District 1, Ho Chi Minh City",
                        "googleMapsLink": "https://maps.google.com/?q=123+Nguyen+Hue+District+1",
                        "cost": 250000,
                        "isIndoor": True,
                        "isOutdoor": False,
                        "isVegetarianFriendly": True,
                        "isAlcoholFriendly": False,
                        "travelTime": None,
                        "distance": None
                    }
                ],
                "totalCost": 250000,
                "bestFor": ["All team members"],
                "rating": 3,
                "fitAnalysis": "Basic fallback plan for team bonding",
                "constraintValidation": {
                    "budgetCompliant": True,
                    "distanceCompliant": True,
                    "travelTimeCompliant": True,
                    "locationBalanced": True
                }
            }
        ]

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

    def _create_prompt(self, team_data: Dict, free_slots: List, central_location: Dict) -> str:
        """Create a prompt for activity suggestions."""
        interests = team_data.get('interests', [])
        budget = team_data.get('budget', 50)
        group_size = team_data.get('group_size', 5)
        
        time_slots = self._format_time_slots(free_slots)
        location = central_location.get('formatted_address', 'San Francisco')
        
        prompt = f"""
        I need activity suggestions for a team bonding event with the following details:
        
        Team Interests: {', '.join(interests)}
        Budget per person: ${budget}
        Group size: {group_size} people
        Available time: {time_slots}
        Location: {location}
        
        Please suggest 3-5 activities that would be suitable for this team. For each activity, include:
        - Activity name
        - Brief description
        - Estimated cost per person
        - Why it would be good for this team
        - Any special considerations
        
        Make sure the suggestions are realistic, within budget, and suitable for the group size and interests.
        """
        
        return prompt

    def _format_time_slots(self, free_slots: List) -> str:
        """Format time slots for the prompt."""
        if not free_slots:
            return "No specific time constraints"
        
        formatted_slots = []
        for slot in free_slots:
            start_time = time.strftime('%Y-%m-%d %H:%M', time.localtime(slot['start']))
            end_time = time.strftime('%Y-%m-%d %H:%M', time.localtime(slot['end']))
            formatted_slots.append(f"{start_time} to {end_time}")
        
        return "; ".join(formatted_slots)

    def _parse_suggestions(self, ai_response: str) -> List[Dict]:
        """Parse AI response into structured suggestions."""
        try:
            # Try to extract structured data from the response
            suggestions = []
            
            # Simple parsing - look for numbered items
            lines = ai_response.split('\n')
            current_suggestion = {}
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # Check if this is a new suggestion (numbered item)
                if re.match(r'^\d+\.', line):
                    if current_suggestion:
                        suggestions.append(current_suggestion)
                    current_suggestion = {'name': line.split('.', 1)[1].strip()}
                elif current_suggestion and ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip().lower().replace(' ', '_')
                    current_suggestion[key] = value.strip()
            
            # Add the last suggestion
            if current_suggestion:
                suggestions.append(current_suggestion)
            
            return suggestions if suggestions else self._alternative_parse_suggestions(ai_response)
            
        except Exception as e:
            print(f"Error parsing suggestions: {e}")
            return self._alternative_parse_suggestions(ai_response)

    def _alternative_parse_suggestions(self, ai_response: str) -> List[Dict]:
        """Alternative parsing method for AI response."""
        try:
            # Try to find activity names in the response
            suggestions = []
            
            # Look for common activity patterns
            activity_patterns = [
                r'([A-Z][a-z\s]+(?:dinner|lunch|breakfast|cafe|restaurant|bar|park|museum|theater|bowling|escape room|karaoke|game|movie|hiking|walking|tour))',
                r'([A-Z][a-z\s]+(?:night|day|evening|morning|afternoon))',
                r'([A-Z][a-z\s]+(?:class|workshop|session|meeting))'
            ]
            
            for pattern in activity_patterns:
                matches = re.findall(pattern, ai_response, re.IGNORECASE)
                for match in matches:
                    if len(match.strip()) > 3:  # Filter out very short matches
                        suggestions.append({
                            'name': match.strip(),
                            'description': f"Activity found in AI response: {match.strip()}",
                            'estimated_cost': 'Varies',
                            'suitability': 'Based on team interests and budget'
                        })
            
            return suggestions[:5]  # Limit to 5 suggestions
            
        except Exception as e:
            print(f"Alternative parsing failed: {e}")
            return self._generate_fallback_suggestions({})

    def _generate_fallback_suggestions(self, team_data: Dict) -> List[Dict]:
        """Generate fallback suggestions when AI fails."""
        return [
            {
                'name': 'Team Dinner',
                'description': 'A casual dinner at a local restaurant',
                'estimated_cost': '$20-30 per person',
                'suitability': 'Good for team bonding and conversation'
            },
            {
                'name': 'Escape Room',
                'description': 'Solve puzzles together in an escape room',
                'estimated_cost': '$25-35 per person',
                'suitability': 'Great for problem-solving and teamwork'
            },
            {
                'name': 'Board Game Night',
                'description': 'Play board games at a cafe or office',
                'estimated_cost': '$10-15 per person',
                'suitability': 'Fun and interactive for all team members'
            }
        ] 