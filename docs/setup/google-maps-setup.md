# 🗺️ Google Maps API Setup Guide

This guide will help you set up Google Maps API to enable location services in the Team Bonding Event Planner.

## 🚀 Quick Setup

### 1. Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click the project dropdown (top left) and select **New Project**
3. Give your project a name (e.g., "Team Bonding Event Planner")
4. Click **Create**

### 2. Enable Required APIs

With your project selected, go to [APIs & Services Dashboard](https://console.cloud.google.com/apis/dashboard) and enable these APIs:

#### Required APIs:
- **Geocoding API** - For converting addresses to coordinates
- **Places API** - For finding nearby places
- **Routes API** - For calculating travel times and distances
- **Maps JavaScript API** - For map display (optional, for future features)

#### How to Enable:
1. Click **+ ENABLE APIS AND SERVICES**
2. Search for each API name
3. Click on the API and press **Enable**
4. Repeat for all required APIs

### 3. Create API Key

1. Go to **APIs & Services > Credentials**
2. Click **+ CREATE CREDENTIALS** and select **API key**
3. Copy the generated API key

### 4. Restrict Your API Key (Recommended)

For security, restrict your API key:

1. Click on your API key in the Credentials page
2. Under **API restrictions**:
   - Select **Restrict key**
   - Choose the APIs you enabled above
3. Under **Application restrictions**:
   - Choose **HTTP referrers** for web apps
   - Add your domain (e.g., `localhost:5000/*` for development)
4. Click **Save**

### 5. Add API Key to Your Project

#### Option A: Environment Variable (Recommended)
```bash
# Add to your .env file
GOOGLE_MAPS_API_KEY=your_actual_api_key_here
```

#### Option B: Direct in config.py (Not recommended for production)
```python
# In backend/config.py
GOOGLE_MAPS_API_KEY = 'your_actual_api_key_here'
```

## 🔧 Troubleshooting

### Common Errors and Solutions

#### 1. "REQUEST_DENIED (This API project is not authorized to use this API)"

**Cause**: API not enabled for your project

**Solution**:
1. Go to [APIs & Services Dashboard](https://console.cloud.google.com/apis/dashboard)
2. Check if all required APIs are enabled
3. If not, enable them following step 2 above

#### 2. "REQUEST_DENIED (You're calling a legacy API)"

**Cause**: Using deprecated APIs

**Solution**: 
- The code has been updated to use newer APIs
- Make sure you have **Routes API** enabled (not just Distance Matrix API)

#### 3. "API key not valid"

**Cause**: Invalid or restricted API key

**Solution**:
1. Check your API key is correct
2. Verify API restrictions allow your usage
3. Check billing is enabled (if required)

#### 4. "Quota exceeded"

**Cause**: API usage limits reached

**Solution**:
1. Check your quota in Google Cloud Console
2. Consider upgrading your plan
3. Implement caching to reduce API calls

## 💰 Billing Setup

### Free Tier Limits
- **Geocoding API**: 2,500 requests/day
- **Places API**: 1,000 requests/day  
- **Routes API**: 2,500 requests/day

### Enable Billing (if needed)
1. Go to [Billing](https://console.cloud.google.com/billing)
2. Link a billing account to your project
3. This enables higher quotas and removes some restrictions

## 🧪 Testing Your Setup

### 1. Test API Key
```bash
# Run the test script
cd backend
python3 test_location_service.py
```

### 2. Check Logs
Look for these success messages:
```
✅ Google Maps API initialized successfully
✅ Geocoded '123 Nguyen Hue' to [formatted address] at [coordinates]
✅ Travel time: [origin] → [destination] = [time] ([distance])
```

### 3. Manual Test
```python
import googlemaps

# Test your API key
gmaps = googlemaps.Client(key='your_api_key')
result = gmaps.geocode('Ho Chi Minh City, Vietnam')
print(result)
```

## 🔒 Security Best Practices

### 1. API Key Restrictions
- **Always restrict your API key** to specific APIs
- **Use HTTP referrers** for web applications
- **Set up IP restrictions** for server applications

### 2. Environment Variables
- **Never commit API keys** to version control
- **Use .env files** for local development
- **Use secure environment variables** in production

### 3. Monitoring
- **Monitor API usage** in Google Cloud Console
- **Set up alerts** for quota limits
- **Review billing** regularly

## 📊 API Usage Optimization

### 1. Caching
The application includes fallback to dummy data when APIs fail, but for production:

```python
# Example caching implementation
import redis
import json

def cached_geocode(address):
    cache_key = f"geocode:{address}"
    cached = redis_client.get(cache_key)
    if cached:
        return json.loads(cached)
    
    result = gmaps.geocode(address)
    redis_client.setex(cache_key, 3600, json.dumps(result))  # Cache for 1 hour
    return result
```

### 2. Batch Requests
For multiple addresses, consider batching:

```python
# Batch geocoding
addresses = ["Address 1", "Address 2", "Address 3"]
results = gmaps.geocode(addresses)
```

### 3. Error Handling
The updated code includes graceful fallbacks:
- Falls back to dummy data when APIs fail
- Logs specific error messages for debugging
- Continues operation even with API issues

## 🚀 Production Deployment

### 1. Environment Variables
```bash
# Production environment
export GOOGLE_MAPS_API_KEY="your_production_api_key"
```

### 2. API Key Rotation
- **Rotate API keys** regularly
- **Monitor for unauthorized usage**
- **Have backup API keys** ready

### 3. Monitoring
- **Set up Google Cloud Monitoring**
- **Monitor API quotas and usage**
- **Set up alerts for errors**

## 📞 Support

### Google Maps Platform Support
- [Google Maps Platform Documentation](https://developers.google.com/maps/documentation)
- [API Status Dashboard](https://status.cloud.google.com/)
- [Google Cloud Support](https://cloud.google.com/support)

### Application Support
- Check the [Troubleshooting Guide](../troubleshooting/backend.md)
- Review [Backend Logging](../backend/logging.md)
- Open an issue on GitHub

---

**Need help?** If you're still having issues after following this guide, check the logs for specific error messages and refer to the troubleshooting section above. 