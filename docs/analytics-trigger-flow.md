# 📊 Analytics Trigger Flow Documentation

## Overview

The Event Analytics & Suggestions system provides AI-powered insights based on team bonding event history. This document describes the complete trigger flow implementation.

## 🎯 Trigger Strategy

### Primary Triggers (High Priority)

1. **After Plan Save** - Analytics refresh when user saves a new plan
2. **Analytics Tab Switch** - Fresh data when user visits Analytics tab
3. **Manual Refresh** - User-initiated refresh via refresh button

### Secondary Triggers (Medium Priority)

4. **Filter Changes** - Re-analysis when user changes limit or theme filters
5. **Periodic Updates** - Background refresh every 30 minutes when tab is visible

### Tertiary Triggers (Low Priority)

6. **Event Rating Updates** - Minor impact analysis
7. **Background Monitoring** - System health checks

## 🔄 Implementation Flow

### 1. Frontend Triggers

#### AnalyticsSuggestions Component (`frontend/src/AnalyticsSuggestions.tsx`)

```typescript
// Smart trigger detection
const shouldTriggerAnalytics = useCallback(() => {
  const lastAnalysis = localStorage.getItem("lastAnalyticsUpdate");
  const lastEventUpdate = localStorage.getItem("lastEventUpdate");
  const currentCacheKey = localStorage.getItem("analyticsCacheKey");

  // Always refresh if cache key changed (filters changed)
  if (currentCacheKey !== cacheKey) return true;

  // Refresh if events were updated after last analysis
  if (!lastAnalysis || (lastEventUpdate && lastEventUpdate > lastAnalysis))
    return true;

  // Refresh if last analysis was more than 30 minutes ago
  const lastAnalysisTime = new Date(lastAnalysis);
  const thirtyMinutesAgo = new Date(Date.now() - 30 * 60 * 1000);
  return lastAnalysisTime < thirtyMinutesAgo;
}, [cacheKey]);
```

#### App Component Integration (`frontend/src/App.tsx`)

```typescript
// Trigger analytics after plan save
const handleSavePlan = async () => {
  // ... save plan logic ...

  // Update event history timestamp for analytics triggers
  localStorage.setItem("lastEventUpdate", new Date().toISOString());
};

// Trigger analytics on tab switch
const handleTabChange = (newValue: number) => {
  setActiveTab(newValue);

  if (newValue === 3) {
    // Analytics tab
    setTimeout(() => {
      window.dispatchEvent(new CustomEvent("refreshAnalytics"));
    }, 100);
  }
};
```

### 2. Backend API Endpoints

#### Analytics Suggestions Endpoint

```python
@app.route("/analytics/suggestions", methods=["GET"])
def get_activity_suggestions():
    """
    Query Parameters:
    - limit: Number of events to analyze (default: 10)
    - theme: Filter by theme (optional)
    - force_refresh: Force refresh (default: false)
    """
    limit = request.args.get("limit", 10, type=int)
    theme_filter = request.args.get("theme", None)
    force_refresh = request.args.get("force_refresh", "false").lower() == "true"

    # Check cache first
    if not force_refresh:
        cached_data = get_cached_analytics(limit, theme_filter)
        if cached_data:
            return jsonify(cached_data)

    # Generate fresh analytics
    # ... analytics generation logic ...

    # Cache result
    cache_analytics_result(limit, result, theme_filter)
    return jsonify(result)
```

#### Analytics Trigger Endpoint

```python
@app.route("/analytics/trigger", methods=["POST"])
def trigger_analytics_update():
    """
    Request Body:
    {
        "limit": 10,
        "theme": "fun",
        "reason": "plan_saved|tab_switch|manual"
    }
    """
    data = request.get_json() or {}
    limit = data.get("limit", 10)
    theme = data.get("theme", "")
    reason = data.get("reason", "manual")

    # Clear cache for these parameters
    clear_analytics_cache(limit, theme)

    return jsonify({
        "message": "Analytics update triggered successfully",
        "cache_cleared": True,
        "reason": reason
    })
```

### 3. Caching System

#### Cache Management

```python
def get_cached_analytics(limit: int, theme_filter: Optional[str] = None) -> Optional[dict]:
    """Get cached analytics if available and fresh (< 30 minutes)"""
    cache_key = f"analytics_{limit}_{theme_filter or 'all'}"
    cache_file = f"cache_{cache_key}.json"

    if os.path.exists(cache_file):
        cache_age = time.time() - os.path.getmtime(cache_file)
        if cache_age < 30 * 60:  # 30 minutes
            with open(cache_file, 'r', encoding='utf-8') as f:
                return json.load(f)
    return None

def cache_analytics_result(limit: int, result: dict, theme_filter: Optional[str] = None):
    """Cache analytics result for future use"""
    cache_key = f"analytics_{limit}_{theme_filter or 'all'}"
    cache_file = f"cache_{cache_key}.json"

    with open(cache_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
```

## 🚀 Performance Optimizations

### 1. Debounced Filter Changes

```typescript
// Debounce filter changes to avoid excessive API calls
useEffect(() => {
  const timer = setTimeout(() => {
    setDebouncedLimit(limit);
    setDebouncedThemeFilter(themeFilter);
  }, 300);

  return () => clearTimeout(timer);
}, [limit, themeFilter]);
```

### 2. Visibility-Based Updates

```typescript
// Only refresh when tab is visible
useEffect(() => {
  const handleVisibilityChange = () => {
    setIsTabVisible(!document.hidden);
  };

  document.addEventListener("visibilitychange", handleVisibilityChange);
  return () =>
    document.removeEventListener("visibilitychange", handleVisibilityChange);
}, []);
```

### 3. Smart Caching

- **Cache Duration**: 30 minutes
- **Cache Keys**: Based on limit and theme filters
- **Cache Invalidation**: On event updates or manual triggers

## 📊 Analytics Data Flow

```
Event History Data → Analytics Processing → AI Analysis → Suggestions → Cache → UI Display
     ↓                    ↓                    ↓            ↓         ↓         ↓
  JSON File         Data Extraction      OpenAI/Gemini   JSON     File     React
  (event_history)   (themes, costs,     (AI prompts)   Response  Cache    Component
                     ratings, etc.)
```

## 🧪 Testing

### Test Script

Run the comprehensive test suite:

```bash
python test_analytics_triggers.py
```

### Test Coverage

1. **Basic Analytics Request** - Verify endpoint functionality
2. **Caching Performance** - Measure speed improvements
3. **Force Refresh** - Test cache bypass
4. **Trigger Endpoint** - Test manual triggers
5. **Theme Filtering** - Test different themes
6. **Cache Files** - Verify cache persistence
7. **Event History Integration** - Test data source
8. **Performance** - Measure response times

## 🔧 Configuration

### Cache Settings

```python
CACHE_DURATION = 30 * 60  # 30 minutes in seconds
CACHE_PREFIX = "cache_analytics_"
```

### Trigger Thresholds

```typescript
const TRIGGER_THRESHOLDS = {
  PERIODIC_REFRESH: 30 * 60 * 1000, // 30 minutes
  DEBOUNCE_DELAY: 300, // 300ms
  TAB_SWITCH_DELAY: 100, // 100ms
};
```

## 📈 Monitoring

### Key Metrics

- **Response Time**: Average analytics generation time
- **Cache Hit Rate**: Percentage of cached vs fresh requests
- **Trigger Frequency**: How often analytics are refreshed
- **Error Rate**: Failed analytics requests

### Logging

```python
logger.info(f"Analytics result cached: {cache_file}")
logger.info(f"Triggering analytics update: limit={limit}, theme={theme}, reason={reason}")
logger.info("Returning cached analytics data")
```

## 🎯 Best Practices

### Performance

1. **Use caching** for expensive AI operations
2. **Debounce user inputs** to reduce API calls
3. **Background processing** for non-critical updates
4. **Lazy loading** of analytics data

### User Experience

1. **Loading states** for all operations
2. **Progress indicators** for long operations
3. **Error handling** with retry options
4. **Success feedback** for manual actions

### Data Freshness

1. **Real-time** for critical actions (plan save)
2. **Near real-time** for user interactions (tab switch)
3. **Periodic** for background maintenance

## 🔄 Future Enhancements

### Planned Features

1. **Real-time WebSocket updates** for live analytics
2. **Advanced caching** with Redis
3. **Analytics scheduling** for off-peak hours
4. **Custom trigger rules** for different user types
5. **Analytics export** functionality

### Performance Improvements

1. **Incremental updates** instead of full refresh
2. **Parallel processing** for multiple analytics
3. **Predictive caching** based on user patterns
4. **CDN integration** for global performance

---

This implementation provides a robust, performant, and user-friendly analytics system that automatically stays up-to-date while minimizing unnecessary API calls and providing excellent user experience.
