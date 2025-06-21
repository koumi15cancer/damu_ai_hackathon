# AI Service Logging Guide

This guide explains how to use the comprehensive logging system added to the `generate_team_bonding_plans` flow to understand what's happening at each step.

## Overview

The logging system provides detailed insights into:

- AI provider initialization and selection
- Team bonding plan generation process
- AI response parsing and validation
- Constraint checking and validation results
- Error handling and fallback mechanisms

## Logging Levels

### INFO Level (Default)

Shows the main flow steps and important information:

- Service initialization
- Provider selection
- Plan generation start/completion
- Validation results
- Error messages

### DEBUG Level

Shows detailed information for debugging:

- All INFO level messages
- Prompt construction details
- AI response parsing steps
- Individual plan validation details
- Provider availability checks

### WARNING Level

Shows only warnings and errors:

- Provider unavailability
- Validation failures
- API errors

## Quick Start

### 1. Run the Test Script

```bash
# Basic test with INFO logging
python test_logging.py

# Maximum verbosity for debugging
python test_logging.py DEBUG

# Minimal output (warnings only)
python test_logging.py WARNING
```

### 2. Use in Your Code

```python
from logging_config import setup_logging
from services.ai_service import AIService

# Setup logging
setup_logging(level="DEBUG", log_to_file=True)

# Use the service
ai_service = AIService(provider='auto')
plans = ai_service.generate_team_bonding_plans(
    team_profiles=team_profiles,
    monthly_theme="fun",
    optional_contribution=50000
)
```

## Log Output Examples

### Service Initialization

```
2024-01-15 10:30:00 - services.ai_service - INFO - 🔧 Initializing AIService with provider: auto
2024-01-15 10:30:00 - services.ai_service - DEBUG - 🔧 Initializing AI provider...
2024-01-15 10:30:00 - services.ai_service - DEBUG - 🔄 Auto-selecting best provider...
2024-01-15 10:30:00 - services.ai_service - INFO - ✅ Selected default provider: openai
2024-01-15 10:30:00 - services.ai_service - INFO - ✅ AIService initialized with provider: openai
```

### Plan Generation Flow

```
2024-01-15 10:30:01 - services.ai_service - INFO - 🚀 Starting generate_team_bonding_plans
2024-01-15 10:30:01 - services.ai_service - INFO - 📊 Input parameters: theme=fun, optional_contribution=50000
2024-01-15 10:30:01 - services.ai_service - INFO - 👥 Team profiles count: 3
2024-01-15 10:30:01 - services.ai_service - INFO - 👤 Team member 1: Alice - energetic - District 1
2024-01-15 10:30:01 - services.ai_service - INFO - 📝 Constructing team bonding prompt...
2024-01-15 10:30:01 - services.ai_service - INFO - 📝 Prompt constructed successfully (length: 1234 characters)
2024-01-15 10:30:01 - services.ai_service - INFO - 🤖 Using AI provider: openai
2024-01-15 10:30:01 - services.ai_service - INFO - 🔄 Generating AI response...
2024-01-15 10:30:05 - services.ai_service - INFO - ✅ AI response generated successfully in 4.23 seconds
2024-01-15 10:30:05 - services.ai_service - INFO - 🔍 Parsing AI response...
2024-01-15 10:30:05 - services.ai_service - INFO - ✅ Found JSON in markdown code blocks
2024-01-15 10:30:05 - services.ai_service - INFO - 📋 Parsed 3 plans from AI response
2024-01-15 10:30:05 - services.ai_service - INFO - ✅ Validating plans against constraints...
2024-01-15 10:30:05 - services.ai_service - INFO - ✅ Plan 1 validation complete: Budget=True, Distance=True, TravelTime=True
```

## Understanding the Flow

### 1. Service Initialization

- Logs show which AI providers are available
- Shows the provider selection process
- Indicates if performance-based selection is used

### 2. Input Processing

- Logs team member details and preferences
- Shows input parameters (theme, budget, location)
- Tracks prompt construction

### 3. AI Generation

- Shows which provider is being used
- Tracks API request parameters
- Measures response time
- Shows response length and preview

### 4. Response Parsing

- Shows parsing strategy (markdown blocks, JSON extraction)
- Indicates if parsing succeeded or failed
- Shows number of plans extracted

### 5. Validation

- Shows budget compliance for each plan
- Tracks distance and travel time constraints
- Indicates validation success/failure

### 6. Error Handling

- Shows detailed error messages
- Indicates fallback plan generation
- Tracks performance recording

## Common Issues and Debugging

### No AI Providers Available

```
❌ No AI providers available
🔍 Available providers: []
```

**Solution**: Check API keys in `config.py`

### JSON Parsing Failures

```
❌ Failed to parse AI response: Expecting property name enclosed in double quotes
❌ Raw response preview: { plans: [ { id: "plan_1"...
```

**Solution**: AI response format issue - check system prompt

### Budget Constraint Violations

```
💰 Plan 1 budget: 600,000 VND (max: 350,000 VND) - Compliant: False
❌ Distance constraint violated: 3.5km > 2.0km
```

**Solution**: AI not following constraints - adjust prompt or validation

### Provider Selection Issues

```
❌ Default provider openai not available, trying fallback: anthropic
⚠️ Failed to switch to provider anthropic: not available
```

**Solution**: Check API keys and provider availability

## Log Files

When `log_to_file=True` is set, logs are saved to:

- `ai_service.log` (default)
- `ai_service_debug.log` (debug mode)
- `ai_service_development.log` (development mode)
- `ai_service_production.log` (production mode)

## Performance Monitoring

The logging system also tracks:

- Response times for each AI provider
- Success/failure rates
- Error types and frequencies
- Provider performance comparisons

## Customization

You can customize logging by modifying `logging_config.py`:

- Change log format
- Add custom handlers
- Set different levels for different components
- Add log rotation

## Best Practices

1. **Use DEBUG level** when investigating issues
2. **Use INFO level** for normal operation monitoring
3. **Use WARNING level** in production
4. **Enable file logging** for persistent records
5. **Check log files** for detailed error information
6. **Monitor response times** to identify performance issues
