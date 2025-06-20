# Team Bonding Event Planner - Flow Summary

## 🚀 Complete Flow: Frontend → Backend → AI → Response

### 1. User Interaction (Frontend)

- User selects theme, budget, members, date, location
- Clicks "Generate Team Bonding Plans" button
- Frontend sends POST request to `/generate-plans`

### 2. Backend Processing

- Extracts parameters from request
- Loads team members from `team_profiles.json`
- Filters by selected members
- Parses budget contribution amount
- Calls AI service with team data

### 3. AI Service Integration

- **Providers**: OpenAI, Anthropic, Google AI
- **Auto-selection**: Chooses best available provider
- **Prompt Construction**: Builds comprehensive prompt with team data
- **AI Generation**: Sends prompt to selected AI provider
- **Response Parsing**: Parses JSON response from AI
- **Fallback**: Uses sample plans if AI fails

### 4. Response Processing

- Validates plans against constraints
- Processes phases and costs
- Generates Google Maps links
- Calculates contribution needed
- Formats for frontend display

### 5. Frontend Display

- Shows generated plans as cards
- Displays cost, rating, fit analysis
- Allows plan selection for details
- Shows phase-by-phase breakdown

## 🔧 Key Components

### Frontend (`frontend/src/App.tsx`)

```typescript
const handleGeneratePlans = async () => {
  const response = await axios.post(
    "http://localhost:5000/generate-plans",
    userPreferences
  );
  setPlans(response.data);
};
```

### Backend (`backend/app.py`)

```python
@app.route('/generate-plans', methods=['POST'])
def generate_plans():
    # Extract parameters
    # Load team members
    # Call AI service
    plans = ai_service.generate_team_bonding_plans(...)
    # Process and return plans
```

### AI Service (`backend/services/ai_service.py`)

```python
def generate_team_bonding_plans(self, team_profiles, monthly_theme, ...):
    # Construct prompt
    # Send to AI provider
    # Parse response
    # Validate constraints
    return validated_plans
```

## 🎯 Current Status

✅ **Working**: Complete flow from frontend to AI service
✅ **Working**: Fallback to sample plans when AI unavailable
✅ **Working**: Multiple AI provider support
✅ **Working**: Real-time plan generation and display

## 🚀 Test the Flow

```bash
# Start backend
cd backend && python app.py

# Start frontend
cd frontend && npm start

# Test complete flow
python3 test_complete_flow.py
```

The complete flow is working correctly! Users can generate personalized team bonding plans using AI.
