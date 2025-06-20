# Team Bonding Event Planner - Complete Flow Documentation

## 🚀 Overview

This document explains the complete flow of the Team Bonding Event Planner application, from user interaction in the frontend to AI-powered plan generation in the backend.

## 📋 Flow Architecture

```
Frontend (React) → Backend API (Flask) → AI Service → Response
```

## 🔄 Complete Flow Breakdown

### 1. Frontend User Interaction

**Location**: `frontend/src/App.tsx`

**User Actions**:

1. User selects event theme (fun 🎉, chill 🧘, outdoor 🌤)
2. User sets budget contribution preferences
3. User selects available team members
4. User sets date/time and location preferences
5. User clicks "Generate Team Bonding Plans" button

**Code Flow**:

```typescript
const handleGeneratePlans = async () => {
  setLoading(true);
  setError("");

  try {
    const response = await axios.post(
      "http://localhost:5000/generate-plans",
      userPreferences
    );

    if (response.data.error) {
      setError(response.data.error);
      return;
    }

    setPlans(response.data);
  } catch (error) {
    console.error("Failed to generate plans:", error);
    setError("Failed to generate team bonding plans. Please try again.");
  } finally {
    setLoading(false);
  }
};
```

### 2. Backend API Processing

**Location**: `backend/app.py`

**API Endpoint**: `POST /generate-plans`

**Request Processing**:

1. **Extract Parameters**: Theme, budget, members, date, location
2. **Load Team Members**: From `team_profiles.json`
3. **Filter Members**: Based on available_members selection
4. **Parse Budget**: Extract contribution amount from string
5. **Call AI Service**: Generate plans using AI

**Code Flow**:

```python
@app.route('/generate-plans', methods=['POST'])
def generate_plans():
    try:
        data = request.json

        # Extract request parameters
        theme = data.get('theme', 'fun 🎉')
        budget_contribution = data.get('budget_contribution', 'No')
        available_members = data.get('available_members', [])
        date_time = data.get('date_time')
        location_zone = data.get('location_zone')

        # Load and filter team members
        all_team_members = load_team_members()
        if available_members:
            team_members = [member for member in all_team_members
                          if member['name'] in available_members]
        else:
            team_members = all_team_members

        # Extract budget contribution amount
        contribution_amount = 0
        if 'Yes' in budget_contribution:
            match = re.search(r'(\d+(?:,\d+)*)', budget_contribution)
            if match:
                contribution_amount = int(match.group(1).replace(',', ''))

        # Generate plans using AI service
        try:
            plans = ai_service.generate_team_bonding_plans(
                team_profiles=team_members,
                monthly_theme=theme,
                optional_contribution=contribution_amount,
                preferred_date=date_time,
                preferred_location_zone=location_zone
            )
        except Exception as e:
            # Fallback to sample plans if AI fails
            plans = generate_sample_plans(team_members, theme,
                                        contribution_amount, location_zone)

        # Process and validate plans
        processed_plans = []
        for plan in plans:
            processed_plan = process_plan(plan, team_members, contribution_amount)
            if processed_plan:
                processed_plans.append(processed_plan)

        return jsonify(processed_plans)

    except Exception as e:
        return jsonify({'error': str(e)}), 500
```

### 3. AI Service Integration

**Location**: `backend/services/ai_service.py`

**AI Providers Supported**:

- OpenAI (GPT-4, GPT-3.5)
- Google AI (Gemini)

**AI Service Flow**:

1. **Provider Selection**: Auto-select best available provider
2. **Prompt Construction**: Build comprehensive prompt with team data
3. **AI Generation**: Send prompt to selected AI provider
4. **Response Parsing**: Parse JSON response from AI
5. **Validation**: Validate plans against constraints
6. **Fallback**: Use sample plans if AI fails

**Code Flow**:

```python
def generate_team_bonding_plans(self, team_profiles, monthly_theme,
                               optional_contribution=0, preferred_date=None,
                               preferred_location_zone=None):
    try:
        # Construct the enhanced prompt
        prompt = self._construct_team_bonding_prompt(
            team_profiles=team_profiles,
            monthly_theme=monthly_theme,
            optional_contribution=optional_contribution,
            preferred_date=preferred_date,
            preferred_location_zone=preferred_location_zone
        )

        # Generate response from AI
        if not self.current_provider:
            raise Exception("No AI providers available")

        start_time = time.time()
        response = self.current_provider.generate_response(
            prompt=prompt,
            system_prompt=self._get_team_bonding_system_prompt(),
            temperature=0.7,
            max_tokens=2000
        )
        response_time = time.time() - start_time

        # Parse and validate the response
        plans = self._parse_team_bonding_response(response)
        validated_plans = self._validate_plans_against_constraints(
            plans, optional_contribution)

        return validated_plans

    except Exception as e:
        # Record failure and raise
        raise e
```

### 4. AI Prompt Construction

**System Prompt**: Defines the AI's role and response format

```python
def _get_team_bonding_system_prompt(self) -> str:
    return """You are an expert team bonding event planner specializing in creating thoughtful, inclusive, and engaging activities for teams in Ho Chi Minh City, Vietnam.

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
```

**User Prompt**: Contains specific requirements and team data

```python
def _construct_team_bonding_prompt(self, team_profiles, monthly_theme,
                                 optional_contribution, preferred_date,
                                 preferred_location_zone):
    # Convert team profiles to readable format
    team_members_info = []
    for member in team_profiles:
        member_info = f"• {member['name']} ({member['vibe']}): {member['location']}"
        if member.get('preferences'):
            member_info += f" - Prefers: {', '.join(member['preferences'])}"
        team_members_info.append(member_info)

    prompt = f"""
Generate 3-5 team bonding event plans for a team in Ho Chi Minh City, Vietnam.

🎯 EVENT REQUIREMENTS:
• Theme: {monthly_theme}
• Budget: 300,000 VND/person base + optional {optional_contribution:,} VND contribution
• Preferred location zone: {preferred_location_zone or 'No specific preference'}
• Preferred date: {preferred_date or 'No specific preference'}

💰 BUDGET CONSTRAINTS:
• Phase 1: ≤ 300,000 VND/person
• Phase 2 (optional): Total ≤ 450,000 VND/person
• Phase 3 (optional): Total ≤ 500,000 VND/person

👥 TEAM MEMBERS:
{chr(10).join(team_members_info)}

📋 PLAN REQUIREMENTS:
Each plan must include:
1. 1-3 phases (dinner → karaoke → bar style)
2. Real Ho Chi Minh City locations with addresses
3. Cost breakdown per phase
4. Dietary and accessibility notes
5. Travel time and distance between phases
6. Best fit analysis for team members

Please provide the response in the exact JSON format specified in the system prompt.
"""
    return prompt
```

### 5. Response Processing

**Plan Processing**: Convert AI response to frontend format

```python
def process_plan(plan, team_members, contribution_amount):
    try:
        # Extract phases from the plan
        phases = []
        total_cost = 0

        # Handle different plan formats
        if 'phases' in plan:
            phases_data = plan['phases']
        elif 'activities' in plan:
            phases_data = plan['activities']
        else:
            phases_data = []
            for key, value in plan.items():
                if isinstance(value, dict) and 'activity' in value:
                    phases_data.append(value)

        for phase_data in phases_data:
            # Extract phase information
            activity = phase_data.get('activity', phase_data.get('name', 'Unknown Activity'))
            location = phase_data.get('location', phase_data.get('address', 'Unknown Location'))
            cost = phase_data.get('cost', 0)

            # Generate Google Maps link
            map_link = generate_map_link(location)

            # Determine indicators
            indicators = []
            if phase_data.get('isIndoor', True):
                indicators.append('indoor')
            if phase_data.get('isOutdoor', False):
                indicators.append('outdoor')
            if phase_data.get('isVegetarianFriendly', False):
                indicators.append('vegetarian-friendly')
            if phase_data.get('isAlcoholFriendly', False):
                indicators.append('alcohol-friendly')

            phase = {
                'activity': activity,
                'location': location,
                'map_link': map_link,
                'cost': cost,
                'indicators': indicators
            }

            phases.append(phase)
            total_cost += cost

        # Calculate contribution needed
        contribution_needed = max(0, total_cost - 300000)

        # Generate fit analysis
        fit_analysis = generate_fit_analysis(plan, team_members)

        # Get rating
        rating = plan.get('rating', 3)

        return {
            'phases': phases,
            'total_cost': total_cost,
            'contribution_needed': contribution_needed,
            'fit_analysis': fit_analysis,
            'rating': rating
        }

    except Exception as e:
        print(f"Error processing plan: {e}")
        return None
```

### 6. Frontend Display

**Plan Display**: Show generated plans to user

```typescript
{
  plans.length > 0 && (
    <Box sx={{ mt: 4 }}>
      <Typography variant='h5' gutterBottom>
        Generated Plans ({plans.length})
      </Typography>
      <Grid container spacing={3}>
        {plans.map((plan, index) => (
          <Grid item xs={12} md={6} lg={4} key={index}>
            <Card
              sx={{
                height: "100%",
                cursor: "pointer",
                transition: "transform 0.2s",
                "&:hover": {
                  transform: "translateY(-4px)",
                },
              }}
              onClick={() => handlePlanClick(plan)}>
              <CardContent>
                <Box sx={{ display: "flex", alignItems: "center", mb: 2 }}>
                  <Box
                    sx={{
                      backgroundColor: getThemeColor(userPreferences.theme),
                      borderRadius: "50%",
                      p: 1,
                      mr: 2,
                    }}>
                    {getThemeIcon(userPreferences.theme)}
                  </Box>
                  <Typography variant='h6'>Plan {index + 1}</Typography>
                </Box>

                <Box sx={{ mb: 2 }}>
                  <Typography
                    variant='body2'
                    color='text.secondary'
                    gutterBottom>
                    {plan.fit_analysis}
                  </Typography>
                </Box>

                <Box sx={{ display: "flex", alignItems: "center", mb: 2 }}>
                  <Rating value={plan.rating} readOnly size='small' />
                  <Typography variant='body2' sx={{ ml: 1 }}>
                    {plan.rating}/5
                  </Typography>
                </Box>

                <Box sx={{ display: "flex", alignItems: "center", mb: 2 }}>
                  <AttachMoney sx={{ mr: 1, color: "text.secondary" }} />
                  <Typography variant='body2'>
                    {plan.total_cost.toLocaleString()} VND
                  </Typography>
                </Box>

                {plan.contribution_needed > 0 && (
                  <Alert severity='warning' sx={{ mb: 2 }}>
                    Additional contribution:{" "}
                    {plan.contribution_needed.toLocaleString()} VND
                  </Alert>
                )}

                <Typography variant='body2' color='text.secondary'>
                  {plan.phases.length} phase
                  {plan.phases.length !== 1 ? "s" : ""}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
}
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```env
# AI Provider API Keys
OPENAI_API_KEY=your_openai_api_key_here
GOOGLE_AI_API_KEY=your_google_ai_api_key_here

# AI Provider Configuration
DEFAULT_AI_PROVIDER=openai
FALLBACK_AI_PROVIDER=google

# Google Maps API key
GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here
```

### AI Configuration

**Location**: `backend/config.py`

```python
AI_CONFIG = {
    'default_provider': 'openai',
    'fallback_provider': 'google',
    'models': {
        'openai': {
            'default': 'gpt-4',
            'fallback': 'gpt-3.5-turbo',
            'available': ['gpt-4', 'gpt-4-turbo', 'gpt-3.5-turbo', 'gpt-4o']
        },
        'google': {
            'default': 'gemini-1.5-pro',
            'fallback': 'gemini-1.5-flash',
            'available': ['gemini-1.5-pro', 'gemini-1.5-flash', 'gemini-1.0-pro']
        }
    },
    'settings': {
        'temperature': 0.7,
        'max_tokens': 500,
        'timeout': 30
    }
}
```

## 🚀 Running the Application

### 1. Start Backend

```bash
cd backend
python app.py
```

### 2. Start Frontend

```bash
cd frontend
npm start
```

### 3. Test the Flow

```bash
python3 test_complete_flow.py
```

## 📊 Data Flow Summary

1. **User Input** → Frontend collects preferences
2. **API Request** → Frontend sends POST to `/generate-plans`
3. **Data Processing** → Backend extracts and validates parameters
4. **AI Generation** → AI service creates personalized plans
5. **Response Processing** → Backend formats plans for frontend
6. **Display** → Frontend shows plans to user

## 🎯 Key Features

- **Multi-AI Provider Support**: Automatic fallback between OpenAI and Google AI
- **Intelligent Prompting**: Context-aware prompts based on team preferences
- **Constraint Validation**: Budget, distance, and preference constraints
- **Fallback System**: Sample plans when AI is unavailable
- **Real-time Processing**: Fast response times with loading states
- **Error Handling**: Graceful error handling at all levels

## 🔍 Testing

The application includes comprehensive testing:

- **Backend API Tests**: `backend/test_api.py`
- **AI Integration Tests**: `backend/test_ai_integration.py`
- **Complete Flow Test**: `test_complete_flow.py`

Run tests to verify the complete flow is working correctly.
