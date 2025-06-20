# 🤖 AI Integration Setup Guide

This guide will help you replace the demo output with real AI API integration for the Team Bonding Event Planner.

## 🎯 Current Status

✅ **Backend is working** with fallback sample data  
✅ **Frontend is connected** and displaying plans  
✅ **Ready for AI integration** - just need API keys

## 🚀 Step 1: Get AI API Keys

### Option A: OpenAI (Recommended - Easiest)

1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign up/Login
3. Click "Create new secret key"
4. Copy the key (starts with `sk-`)

### Option B: Google AI (Gemini)

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with Google
3. Click "Create API Key"
4. Copy the key

## 🔧 Step 2: Configure API Keys

### Create/Edit Environment File

```bash
cd backend
nano .env
```

### Add Your API Keys

```env
# Choose ONE or more providers:

# OpenAI (Recommended)
OPENAI_API_KEY=sk-your_openai_key_here

# Google AI
GOOGLE_AI_API_KEY=your_google_ai_key_here

# Optional: Google Calendar & Maps
GOOGLE_CLIENT_ID=your_google_client_id_here
GOOGLE_CLIENT_SECRET=your_google_client_secret_here
GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here
```

## 🧪 Step 3: Test AI Integration

### Test with OpenAI

```bash
curl -X POST http://localhost:5000/api/team-bonding/plans \
  -H "Content-Type: application/json" \
  -d '{
    "monthly_theme": "fun",
    "optional_contribution": 100000,
    "available_members": ["Ben", "Cody", "Big Thanh"],
    "preferred_date": "2024-01-15",
    "preferred_location_zone": "District 1"
  }'
```

### Test with Google AI

```bash
# Same command - the system will automatically choose the best available provider
```

## 🔍 Step 4: Verify AI is Working

### Check Backend Logs

Look for these messages in your terminal:

- ✅ `"Using OpenAI for AI generation"`
- ✅ `"AI response generated successfully"`
- ❌ `"No AI providers available, using sample plans"`

### Test in Frontend

1. Open http://localhost:3000
2. Fill out the form
3. Click "Generate Event Plans"
4. You should see AI-generated plans instead of sample data

## 🎨 Step 5: Customize AI Prompts

### Edit the AI Prompt

File: `backend/app.py` - Function: `construct_team_bonding_prompt()`

You can customize:

- **Budget constraints**
- **Location preferences**
- **Team member matching logic**
- **Event type preferences**

### Example Customization

```python
# Add specific venue preferences
prompt += f"\n• Preferred venues: {preferred_venues}"

# Add dietary restrictions
prompt += f"\n• Dietary requirements: {dietary_restrictions}"
```

## 🔧 Step 6: Advanced Configuration

### AI Provider Selection

The system automatically chooses the best available provider:

1. **OpenAI GPT-4** (if available)
2. **Google Gemini** (if available)
3. **Sample data** (fallback)

### Model Configuration

Edit `backend/config.py` to change AI models:

```python
AI_CONFIG = {
    'models': {
        'openai': {
            'default': 'gpt-4',  # Change to gpt-3.5-turbo for cheaper
            'available': ['gpt-4', 'gpt-4-turbo', 'gpt-3.5-turbo']
        }
    }
}
```

## 🚨 Troubleshooting

### Common Issues

**1. "No AI providers available"**

- Check your API keys are correct
- Verify the keys are not placeholder values
- Check internet connection

**2. "API rate limit exceeded"**

- Wait a few minutes and try again
- Consider upgrading your API plan
- Use a different provider

**3. "Invalid API key"**

- Double-check the key format
- Ensure the key is active
- Check for extra spaces or characters

**4. "Timeout error"**

- Increase timeout in config.py
- Check your internet connection
- Try a different AI provider

### Debug Commands

```bash
# Check which providers are available
curl http://localhost:5000/api/ai/providers

# Test specific provider
curl -X POST http://localhost:5000/api/ai/test \
  -H "Content-Type: application/json" \
  -d '{"provider": "openai", "prompt": "Hello"}'
```

## 💰 Cost Estimation

### OpenAI

- **GPT-3.5-turbo**: ~$0.002 per 1K tokens
- **GPT-4**: ~$0.03 per 1K tokens
- **Typical plan generation**: 500-1000 tokens

### Google AI

- **Gemini Pro**: ~$0.0005 per 1K tokens
- **Typical plan generation**: 500-1000 tokens

## 🎯 Next Steps

1. **Get your API key** (recommend OpenAI for easiest setup)
2. **Add it to .env file**
3. **Restart the backend** if needed
4. **Test the integration**
5. **Customize prompts** as needed

## 🆘 Need Help?

If you encounter issues:

1. Check the backend logs for error messages
2. Verify your API key is correct
3. Test with a simple prompt first
4. Try a different AI provider

The system will automatically fall back to sample data if AI providers aren't available, so your application will always work!
