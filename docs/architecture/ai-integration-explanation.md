# How AI Works When Calling the API in This Project

## Overview

This project uses a sophisticated AI integration system that supports multiple AI providers (OpenAI, Google Gemini) to generate personalized team bonding event plans. Here's how it works when you call the API:

## 🏗️ Architecture Overview

```
Frontend → Backend API → AI Service → AI Providers → Response Processing → Frontend
```

## 🔄 Complete AI Workflow

### 1. **Frontend Request**

When you click "Generate Team Bonding Plans" in the frontend:

```typescript
// Frontend sends this to backend
const request = {
  theme: "fun 🎉",
  budget_contribution: "Yes, up to 150,000 VND",
  available_members: ["Ben", "Cody", "Big Thanh"],
  date_time: "2023-12-15 18:00",
  location_zone: "District 1",
};

await axios.post("http://localhost:5000/generate-plans", request);
```

### 2. **Backend API Processing**

The backend receives the request and processes it:

```python
# Backend extracts and validates data
theme = data.get('theme', 'fun 🎉')
budget_contribution = data.get('budget_contribution', 'No')
available_members = data.get('available_members', [])
date_time = data.get('date_time')
location_zone = data.get('location_zone')

# Load team member profiles
team_members = load_team_members()

# Extract budget contribution amount
contribution_amount = extract_budget_amount(budget_contribution)
```

### 3. **AI Service Initialization**

The AI service automatically selects the best available AI provider:

```python
# AI Service automatically chooses provider
ai_service = AIService(provider='auto')

# Provider selection logic:
# 1. Check performance-based selection
# 2. Try default provider (OpenAI)
# 3. Try fallback provider (Google)
# 4. Try any available provider
```

### 4. **AI Prompt Construction**

The system builds a comprehensive prompt for the AI:

```python
def _construct_team_bonding_prompt(self, team_profiles, monthly_theme,
                                 optional_contribution, preferred_date,
                                 preferred_location_zone):
    # Build team member information
    team_members_text = format_team_members(team_profiles)

    # Create detailed prompt with constraints
    prompt = f"""
    Generate 3-5 team bonding event plans for a team in Ho Chi Minh City, Vietnam.

    🎯 EVENT REQUIREMENTS:
    • Theme: {monthly_theme}
    • Budget: 300,000 VND/person base + optional {optional_contribution:,} VND contribution
    • Preferred location: {preferred_location_zone}
    • Preferred date: {preferred_date}

    💰 BUDGET CONSTRAINTS:
    • Phase 1: ≤ 300,000 VND/person
    • Phase 2 (optional): Total ≤ 450,000 VND/person
    • Phase 3 (optional): Total ≤ 500,000 VND/person

    🚶‍♀️ LOGISTICS CONSTRAINTS:
    • Each phase within 2 km of others
    • Max 15 minutes travel time between phases

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
    """
    return prompt
```

### 5. **AI Provider Selection & Call**

The system calls the selected AI provider:

```python
# System prompt for consistent formatting
system_prompt = """You are an expert team bonding event planner specializing in creating thoughtful, inclusive, and engaging activities for teams in Ho Chi Minh City, Vietnam.

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
      "fitAnalysis": "Analysis of who this plan suits best"
    }
  ]
}
"""

# Call AI provider
response = self.current_provider.generate_response(
    prompt=prompt,
    system_prompt=system_prompt,
    temperature=0.7,
    max_tokens=2000
)
```

### 6. **AI Provider Implementation**

Each AI provider has its own implementation:

#### **OpenAI Provider**

```python
def generate_response(self, prompt: str, system_prompt: str = None, **kwargs) -> str:
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    response = openai.chat.completions.create(
        model='gpt-4',
        messages=messages,
        temperature=0.7,
        max_tokens=2000
    )
    return response.choices[0].message.content
```

#### **Google Gemini Provider**

```python
def generate_response(self, prompt: str, system_prompt: str = None, **kwargs) -> str:
    model = genai.GenerativeModel('gemini-1.5-pro')

    full_prompt = prompt
    if system_prompt:
        full_prompt = f"{system_prompt}\n\n{prompt}"

    response = model.generate_content(
        full_prompt,
        generation_config=genai.types.GenerationConfig(
            temperature=0.7,
            max_output_tokens=2000
        )
    )
    return response.text
```

### 7. **Response Processing**

The AI response is parsed and validated:

````python
def _parse_team_bonding_response(self, ai_response: str) -> List[Dict]:
    try:
        # Extract JSON from response
        json_match = re.search(r'```json\s*(.*?)\s*```', ai_response, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
            parsed_data = json.loads(json_str)
        else:
            # Try to find JSON in the response
            json_start = ai_response.find('{')
            json_end = ai_response.rfind('}') + 1
            json_str = ai_response[json_start:json_end]
            parsed_data = json.loads(json_str)

        # Extract plans from parsed data
        if isinstance(parsed_data, dict) and 'plans' in parsed_data:
            return parsed_data['plans']
        elif isinstance(parsed_data, list):
            return parsed_data
        else:
            raise ValueError("Invalid response format")

    except (json.JSONDecodeError, ValueError) as e:
        # Return fallback plans if parsing fails
        return self._generate_fallback_plans()
````

### 8. **Plan Validation**

Plans are validated against constraints:

```python
def _validate_plans_against_constraints(self, plans: List[Dict], optional_contribution: int) -> List[Dict]:
    validated_plans = []

    for plan in plans:
        # Check budget constraints
        total_cost = plan.get('totalCost', 0)
        max_budget = 300000 + optional_contribution

        if total_cost <= max_budget:
            # Check distance constraints
            phases = plan.get('phases', [])
            distance_valid = True

            for i in range(len(phases) - 1):
                distance = phases[i].get('distance', 0)
                if distance > 2.0:  # 2km limit
                    distance_valid = False
                    break

            if distance_valid:
                validated_plans.append(plan)

    return validated_plans
```

### 9. **Response Formatting**

The backend formats the response for the frontend:

```python
def process_plan(plan, team_members, contribution_amount):
    # Extract phases and convert to frontend format
    phases = []
    for phase_data in plan['phases']:
        phase = {
            'activity': phase_data.get('name', 'Unknown Activity'),
            'location': phase_data.get('address', 'Unknown Location'),
            'map_link': generate_map_link(phase_data.get('address')),
            'cost': phase_data.get('cost', 0),
            'indicators': extract_indicators(phase_data)
        }
        phases.append(phase)

    return {
        'phases': phases,
        'total_cost': plan.get('totalCost', 0),
        'contribution_needed': max(0, plan.get('totalCost', 0) - 300000),
        'fit_analysis': plan.get('fitAnalysis', ''),
        'rating': plan.get('rating', 3)
    }
```

### 10. **Frontend Display**

The frontend receives and displays the plans:

```typescript
// Frontend receives processed plans
const plans = response.data;

// Display plans in UI
plans.map((plan, index) => (
  <Card key={index}>
    <CardContent>
      <Typography variant='h6'>Plan {index + 1}</Typography>
      <Typography>
        Total Cost: {plan.total_cost.toLocaleString()} VND
      </Typography>
      <Typography>Rating: {plan.rating}/5</Typography>
      {plan.phases.map((phase, phaseIndex) => (
        <Box key={phaseIndex}>
          <Typography>{phase.activity}</Typography>
          <Typography>{phase.location}</Typography>
          <Typography>{phase.cost.toLocaleString()} VND</Typography>
        </Box>
      ))}
    </CardContent>
  </Card>
));
```

## 🤖 AI Provider Features

### **Multi-Provider Support**

- **OpenAI GPT-4**: Advanced reasoning, creative responses
- **Google Gemini**: Multimodal, strong creative capabilities

### **Automatic Provider Selection**

```python
# Performance-based selection
best_provider = self.model_manager.get_best_performing_model()

# Fallback chain
if self.providers['openai'].is_available():
    self.current_provider = self.providers['openai']
elif self.providers['google'].is_available():
    self.current_provider = self.providers['google']
```

### **Performance Tracking**

```python
# Record performance metrics
self.model_manager.record_performance(
    provider=self.provider_name,
    model=AI_CONFIG['models'][self.provider_name]['default'],
    response_time=response_time,
    success=True
)
```

## 🔧 Configuration

### **Environment Variables**

```bash
# AI Provider API Keys
OPENAI_API_KEY=your_openai_key_here
GOOGLE_AI_API_KEY=your_google_ai_key_here

# Provider Selection
DEFAULT_AI_PROVIDER=openai
FALLBACK_AI_PROVIDER=google
```

### **AI Configuration**

```python
AI_CONFIG = {
    'default_provider': 'openai',
    'fallback_provider': 'google',
    'models': {
        'openai': {
            'default': 'gpt-4',
            'available': ['gpt-4', 'gpt-4-turbo', 'gpt-3.5-turbo']
        },
        'google': {
            'default': 'gemini-1.5-pro',
            'available': ['gemini-1.5-pro', 'gemini-1.5-flash']
        }
    },
    'settings': {
        'temperature': 0.7,
        'max_tokens': 2000,
        'timeout': 30
    }
}
```

## 🛡️ Error Handling & Fallbacks

### **AI Provider Failures**

```python
try:
    plans = ai_service.generate_team_bonding_plans(...)
except Exception as e:
    print(f"AI generation failed: {e}")
    # Fallback to sample plans
    plans = generate_sample_plans(...)
```

### **Response Parsing Failures**

```python
try:
    parsed_plans = self._parse_team_bonding_response(ai_response)
except (json.JSONDecodeError, ValueError) as e:
    # Return fallback plans
    return self._generate_fallback_plans()
```

### **Provider Unavailability**

```python
if not self.current_provider:
    # Try to initialize any available provider
    for name, provider in self.providers.items():
        if provider.is_available():
            self.current_provider = provider
            self.provider_name = name
            break
```

## 📊 Performance Monitoring

### **Response Time Tracking**

```python
start_time = time.time()
response = self.current_provider.generate_response(...)
response_time = time.time() - start_time

# Record for performance analysis
self.model_manager.record_performance(
    provider=self.provider_name,
    response_time=response_time,
    success=True
)
```

### **Success Rate Monitoring**

```python
# Track success/failure rates
self.model_manager.record_performance(
    provider=self.provider_name,
    success=False,
    error_message=str(e)
)
```

## 🎯 Key Benefits

1. **Multi-Provider Redundancy**: If one AI provider fails, others are available
2. **Performance Optimization**: Automatically selects the best performing provider
3. **Consistent Output**: Structured prompts ensure consistent JSON responses
4. **Constraint Validation**: Plans are validated against budget and distance limits
5. **Fallback Support**: Sample plans when AI is unavailable
6. **Real-time Monitoring**: Performance tracking and error handling
7. **Local Context**: Specialized for Ho Chi Minh City locations and culture

This AI integration provides a robust, scalable solution for generating personalized team bonding plans with multiple fallback mechanisms and comprehensive error handling.
