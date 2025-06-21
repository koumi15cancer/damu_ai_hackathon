# AI Integration Guide

This document describes the enhanced AI integration system that supports multiple AI providers with advanced features like performance tracking, A/B testing, and intelligent provider selection.

## Features

### 🔄 Multi-Provider Support

- **OpenAI GPT** (GPT-4, GPT-4 Turbo, GPT-3.5 Turbo, GPT-4o)
- **Google Gemini** (Gemini 1.5 Pro, Gemini 1.5 Flash, Gemini 1.0 Pro)

### 📊 Performance Monitoring

- Real-time response time tracking
- Success/failure rate monitoring
- Automatic performance-based provider selection
- Historical performance analytics

### 🧪 A/B Testing

- Multi-provider A/B testing
- Configurable traffic splitting
- Performance comparison
- Result tracking and analysis

### 🎯 Smart Provider Selection

- Performance-based auto-selection
- Use case-specific recommendations
- Cost optimization
- Fallback mechanisms

## Setup

### 1. Environment Variables

Add the following to your `.env` file:

```bash
# OpenAI
OPENAI_API_KEY=your_openai_api_key

# Google AI
GOOGLE_AI_API_KEY=your_google_ai_api_key

# AI Configuration (optional)
DEFAULT_AI_PROVIDER=openai
FALLBACK_AI_PROVIDER=google
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

## API Endpoints

### Provider Management

#### Get Available Providers

```http
GET /api/ai/providers
```

Response:

```json
{
  "available_providers": ["openai", "google"],
  "current_provider": "openai",
  "providers_info": {
    "openai": {
      "name": "OpenAI GPT",
      "models": ["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo", "gpt-4o"],
      "description": "Advanced language model with strong reasoning capabilities"
    }
  }
}
```

#### Switch Provider

```http
POST /api/ai/switch-provider
Content-Type: application/json

{
  "provider": "google"
}
```

### Performance Monitoring

#### Get Performance Statistics

```http
GET /api/ai/performance?time_window=24
```

Response:

```json
{
  "performance_stats": {
    "openai": {
      "total_requests": 150,
      "successful_requests": 145,
      "success_rate": 0.967,
      "avg_response_time": 2.3,
      "total_response_time": 345.0,
      "errors": ["Rate limit exceeded", "Invalid API key"]
    }
  },
  "time_window_hours": 24,
  "current_provider": "openai"
}
```

#### Get Model Recommendations

```http
GET /api/ai/recommendations?use_case=creative
```

Response:

```json
{
  "recommendations": {
    "fastest": "google",
    "most_reliable": "openai",
    "cost_effective": "google",
    "best_for_use_case": "openai"
  },
  "use_case": "creative",
  "current_provider": "openai"
}
```

### A/B Testing

#### Setup A/B Test

```http
POST /api/ai/ab-test/setup
Content-Type: application/json

{
  "test_name": "suggestion_quality_test",
  "providers": ["openai", "google"],
  "traffic_split": {
    "openai": 0.6,
    "google": 0.4
  }
}
```

#### Get A/B Test Results

```http
GET /api/ai/ab-test/results/suggestion_quality_test
```

Response:

```json
{
  "test_name": "suggestion_quality_test",
  "start_time": "2024-01-15T10:30:00",
  "traffic_split": {
    "openai": 0.6,
    "google": 0.4
  },
  "results": {
    "openai": {
      "requests": 60,
      "successes": 58,
      "success_rate": 0.967
    },
    "google": {
      "requests": 40,
      "successes": 37,
      "success_rate": 0.925
    }
  }
}
```

#### Get A/B Test Provider

```http
GET /api/ai/ab-test/provider/suggestion_quality_test
```

### Testing

#### Test AI Provider

```http
POST /api/ai/test
Content-Type: application/json

{
  "prompt": "Hello, can you provide a brief response to test the AI service?"
}
```

Response:

```json
{
  "success": true,
  "response": "Hello! I'm here to help. The AI service is working correctly.",
  "provider": "openai",
  "response_time": 1.23
}
```

### Enhanced Suggestions with A/B Testing

#### Get Suggestions with A/B Test

```http
POST /api/suggestions
Content-Type: application/json

{
  "team_members": [...],
  "interests": ["hiking", "games"],
  "budget": 50,
  "ab_test_name": "suggestion_quality_test"
}
```

## Configuration

### AI Configuration (config.py)

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

## Usage Examples

### Python Usage

```python
from services.ai_service import AIService

# Initialize with auto-selection
ai_service = AIService(provider='auto')

# Get available providers
providers = ai_service.get_available_providers()
print(f"Available providers: {providers}")

# Switch to specific provider
ai_service.switch_provider('google')

# Get performance stats
stats = ai_service.get_performance_stats(time_window_hours=24)
print(f"Performance stats: {stats}")

# Setup A/B test
ai_service.setup_ab_test(
    test_name="quality_test",
    providers=["openai", "google"],
    traffic_split={"openai": 0.5, "google": 0.5}
)

# Get A/B test provider
provider = ai_service.get_ab_test_provider("quality_test")
print(f"Selected provider: {provider}")
```

### Frontend Integration

```javascript
// Get available providers
const response = await fetch('/api/ai/providers');
const { available_providers, current_provider } = await response.json();

// Switch provider
await fetch('/api/ai/switch-provider', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ provider: 'google' })
});

// Get suggestions with A/B testing
const suggestions = await fetch('/api/suggestions', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    team_members: [...],
    interests: ['hiking', 'games'],
    budget: 50,
    ab_test_name: 'quality_test'
  })
});
```

## Advanced Features

### Performance-Based Selection

The system automatically selects the best performing provider based on:

- Response time
- Success rate
- Recent performance (configurable time window)

### Cost Optimization

The system can recommend cost-effective models based on:

- Per-request cost estimates
- Performance requirements
- Use case requirements

### Use Case Recommendations

Different providers are recommended for different use cases:

- **Creative tasks**: OpenAI GPT
- **Analytical tasks**: OpenAI GPT
- **Multimodal tasks**: Google Gemini

## Monitoring and Analytics

### Performance Tracking

The system tracks:

- Response times
- Success/failure rates
- Error messages
- Provider usage patterns

### Data Export

```python
# Export performance data
filename = ai_service.model_manager.export_performance_data()
print(f"Data exported to: {filename}")
```

## Best Practices

1. **Provider Selection**: Use auto-selection for production, manual selection for testing
2. **A/B Testing**: Run tests for at least 24 hours to get meaningful results
3. **Monitoring**: Regularly check performance stats to identify issues
4. **Fallbacks**: Always configure fallback providers for reliability
5. **Cost Management**: Monitor usage and costs across providers

## Troubleshooting

### Common Issues

1. **No providers available**: Check API keys in environment variables
2. **High response times**: Check network connectivity and API rate limits
3. **A/B test not working**: Ensure test is properly configured with valid providers
4. **Performance data missing**: Check file permissions for model_preferences.json

### Debug Mode

Enable debug logging by setting the environment variable:

```bash
export FLASK_DEBUG=1
```

## Security Considerations

1. **API Keys**: Never commit API keys to version control
2. **Rate Limiting**: Implement rate limiting for API endpoints
3. **Data Privacy**: Be mindful of data sent to AI providers
4. **Access Control**: Implement proper authentication for admin endpoints

## Future Enhancements

- [ ] Real-time performance dashboards
- [ ] Advanced cost tracking and optimization
- [ ] Custom model fine-tuning support
- [ ] Multi-region provider support
- [ ] Advanced A/B testing with statistical significance
- [ ] Integration with monitoring tools (Prometheus, Grafana)
