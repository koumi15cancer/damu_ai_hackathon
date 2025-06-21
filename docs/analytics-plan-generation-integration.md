# Analytics Integration in Plan Generation

This document explains how analytics data from event history is now integrated into the plan generation process for the "similar" and "reuse" options.

## 🎯 **Overview**

Previously, the plan generation options ("reuse", "similar", "new") were only using generic prompt instructions without actual event history data. Now, the system properly integrates analytics data to provide more personalized and data-driven plan generation.

## 🔄 **How It Works**

### **Before (Generic Prompts)**

```python
# Old approach - only text instructions
if plan_generation_mode == "similar":
    generation_mode_text = "Generate plans similar to previous events but with variations..."
```

### **After (Data-Driven Prompts)**

```python
# New approach - includes actual event history
if event_history and plan_generation_mode in ["reuse", "similar"]:
    # Add recent events to prompt
    event_history_text = "\n\n📚 RECENT EVENT HISTORY:\n"
    for event in recent_events:
        event_history_text += f"• {event['date']}: {event['theme']} theme\n"
        event_history_text += f"  Activities: {', '.join(event['activities'])}\n"
        event_history_text += f"  Cost: {event['total_cost']:,} VND, Rating: {event['rating']}/5\n"

    # Add analytics insights
    event_history_text += f"📈 ANALYTICS INSIGHTS:\n"
    event_history_text += f"• Most popular theme: {most_popular_theme}\n"
    event_history_text += f"• Average cost: {avg_cost:,.0f} VND\n"
    event_history_text += f"• Average rating: {avg_rating:.1f}/5\n"
```

## 📊 **Data Flow**

### **1. Frontend Selection**

```typescript
// User selects generation mode
<RadioGroup value={userPreferences.plan_generation_mode}>
  <FormControlLabel value='reuse' label='Reuse previous plan structure' />
  <FormControlLabel value='similar' label='Generate similar plan' />
  <FormControlLabel value='new' label='Create brand new plan' />
</RadioGroup>
```

### **2. Backend API Processing**

```python
# app.py - generate_plans endpoint
if plan_generation_mode in ["reuse", "similar"]:
    event_history = load_event_history()  # Load actual data
    logger.info(f"📊 Loaded {len(event_history)} events from history")

plans = ai_service.generate_team_bonding_plans(
    # ... other parameters ...
    plan_generation_mode=plan_generation_mode,
    event_history=event_history,  # Pass to AI service
)
```

### **3. AI Service Integration**

```python
# ai_service.py - enhanced prompt construction
def _construct_team_bonding_prompt(
    self,
    team_profiles: List[Dict],
    monthly_theme: str,
    # ... other parameters ...
    event_history: Optional[List[Dict]] = None,
) -> str:

    # Add event history context for reuse and similar modes
    if event_history and plan_generation_mode in ["reuse", "similar"]:
        # Include recent events and analytics insights in prompt
        event_history_text = self._build_event_history_context(event_history)
        prompt += event_history_text
```

## 🎯 **Three Generation Modes Explained**

### **1. "new" Mode**

- **Analytics Data**: None
- **Prompt**: Generic instructions only
- **Use Case**: When you want completely fresh ideas
- **Example**: "Create brand new innovative plans"

### **2. "similar" Mode**

- **Analytics Data**: Recent events + insights
- **Prompt**: Includes event history + analytics insights
- **Use Case**: When you want variations of what worked before
- **Example**:

  ```
  📚 RECENT EVENT HISTORY:
  1. 2024-01-15: fun 🎉 theme
     Activities: Hotpot Dinner, Karaoke, Bar Hopping
     Cost: 450,000 VND, Rating: 4/5

  📈 ANALYTICS INSIGHTS:
  • Most popular theme: fun 🎉
  • Average cost: 316,667 VND
  • Average rating: 4.3/5
  ```

### **3. "reuse" Mode**

- **Analytics Data**: Event structure + patterns
- **Prompt**: Includes event structure and flow patterns
- **Use Case**: When you want to follow successful patterns
- **Example**:
  ```
  📋 STRUCTURE PATTERNS:
  • fun 🎉: 3 phases (dinner → karaoke → bar)
  • chill 🧘: 2 phases (cafe → board games)
  • outdoor 🌤: 2 phases (park → dining)
  ```

## 📈 **Analytics Insights Included**

### **Event History Data**

- Recent events (last 5)
- Event dates and themes
- Activity lists
- Costs and ratings
- Locations

### **Statistical Insights**

- Most popular theme
- Average cost per event
- Average rating
- Total events analyzed
- Cost trends
- Rating trends

### **Pattern Recognition**

- Phase structure patterns
- Activity combinations
- Location preferences
- Cost ranges
- Success indicators

## 🔧 **Implementation Details**

### **Backend Changes**

1. **app.py**: Load event history for relevant modes
2. **ai_service.py**: Accept event_history parameter
3. **Prompt Construction**: Include analytics data in prompts

### **Data Processing**

```python
# Extract analytics insights
themes = [e.get('theme') for e in event_history]
costs = [e.get('total_cost', 0) for e in event_history]
ratings = [e.get('rating', 0) for e in event_history if e.get('rating')]

avg_cost = sum(costs) / len(costs) if costs else 0
avg_rating = sum(ratings) / len(ratings) if ratings else 0
most_popular_theme = max(set(themes), key=themes.count) if themes else "Unknown"
```

### **Prompt Enhancement**

```python
# Add to AI prompt
prompt += f"""
{event_history_text}

Based on this historical data, generate plans that:
• Follow successful patterns from previous events
• Use similar activity types that received high ratings
• Stay within the average cost range of {avg_cost:,.0f} VND
• Incorporate the most popular theme: {most_popular_theme}
"""
```

## 🧪 **Testing**

Run the test script to see the integration in action:

```bash
python3 test_analytics_integration.py
```

This will:

1. Create sample event history
2. Test "new" mode (no analytics)
3. Test "similar" mode (with analytics)
4. Test "reuse" mode (with analytics)
5. Show the differences in prompts

## 📊 **Benefits**

### **For Users**

- More personalized plan suggestions
- Better cost predictions
- Higher success rate plans
- Learning from past experiences

### **For AI**

- Context-aware generation
- Data-driven decisions
- Pattern recognition
- Improved accuracy

### **For System**

- Better user satisfaction
- Reduced plan failures
- Continuous improvement
- Data-driven insights

## 🔮 **Future Enhancements**

1. **Machine Learning**: Use ML models to predict plan success
2. **Seasonal Patterns**: Consider time-based trends
3. **Team Preferences**: Learn individual member preferences
4. **Cost Optimization**: Suggest budget-friendly alternatives
5. **Location Intelligence**: Use location-based analytics

## 📝 **Summary**

The analytics integration transforms the plan generation from generic prompts to data-driven, personalized suggestions. The AI now has access to:

- **Historical Events**: Real data about past events
- **Analytics Insights**: Statistical analysis of patterns
- **Success Indicators**: What worked well before
- **Cost Patterns**: Budget optimization insights

This makes the "similar" and "reuse" options truly meaningful and valuable for users who want to build on their successful team bonding experiences.
