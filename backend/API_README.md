# Team Bonding Event Planner API

This is the backend API for the Team Bonding Event Planner application. It provides endpoints for generating team bonding event plans and managing team member profiles.

## Getting Started

### Prerequisites

- Python 3.7+
- Flask
- Required dependencies (see `requirements.txt`)

### Installation

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Set up environment variables (optional):

```bash
export GOOGLE_MAPS_API_KEY="your_google_maps_api_key"
export OPENAI_API_KEY="your_openai_api_key"
```

3. Run the server:

```bash
python app.py
```

The server will start on `http://localhost:5000`

## API Endpoints

### 1. POST /generate-plans

Generates 3-5 team bonding event plans based on user inputs, team member profiles, and constraints.

**Request Body:**

```json
{
  "theme": "fun 🎉",
  "budget_contribution": "Yes, up to 150,000 VND",
  "available_members": ["Ben", "Cody", "Big Thanh"],
  "date_time": "2023-12-15 18:00",
  "location_zone": "District 1"
}
```

**Response:**

```json
[
  {
    "phases": [
      {
        "activity": "Hotpot Dinner",
        "location": "123 Le Lai, District 1, Ho Chi Minh City",
        "map_link": "https://maps.google.com/?q=123+Le+Lai+District+1",
        "cost": 250000,
        "indicators": ["indoor", "vegetarian-friendly"]
      }
    ],
    "total_cost": 250000,
    "contribution_needed": 0,
    "fit_analysis": "Suits team members in District 1",
    "rating": 4
  }
]
```

### 2. GET /team-members

Retrieves the list of all team member profiles.

**Response:**

```json
[
  {
    "id": "1",
    "name": "Ben",
    "location": "Mizuki Park, Binh Chanh",
    "preferences": ["Vegetarian", "Chill places", "Cafe-hopping"],
    "vibe": "Chill"
  }
]
```

### 3. POST /team-members

Creates a new team member profile.

**Request Body:**

```json
{
  "name": "New Member",
  "location": "District 1, Ho Chi Minh City",
  "preferences": ["Cafe", "Games", "Outdoor activities"],
  "vibe": "Mixed"
}
```

**Response:**

```json
{
  "id": "uuid-string",
  "name": "New Member",
  "location": "District 1, Ho Chi Minh City",
  "preferences": ["Cafe", "Games", "Outdoor activities"],
  "vibe": "Mixed"
}
```

### 4. PUT /team-members/{id}

Updates an existing team member profile.

**Request Body:**

```json
{
  "name": "Updated Name",
  "location": "District 2, Ho Chi Minh City",
  "preferences": ["Cafe", "Games", "Indoor activities"],
  "vibe": "Chill"
}
```

### 5. DELETE /team-members/{id}

Deletes a team member profile.

**Response:**

```json
{
  "message": "Team member deleted successfully"
}
```

### 6. GET /health

Health check endpoint.

**Response:**

```json
{
  "status": "healthy",
  "timestamp": "2023-12-15T10:30:00",
  "ai_provider": "openai"
}
```

## Features

- **AI-Powered Plan Generation**: Uses AI services to generate personalized team bonding plans
- **Budget Management**: Enforces budget constraints and calculates contribution requirements
- **Location Validation**: Integrates with Google Maps for location validation and map links
- **Team Member Management**: Full CRUD operations for team member profiles
- **Fallback Support**: Provides sample plans when AI services are unavailable

## Constraints & Validation

- **Budget Limits**:
  - Phase 1: ≤ 300k VND
  - 2 phases: ≤ 450k VND
  - 3 phases: ≤ 500k VND
- **Distance Rule**: Each phase within 2km of others
- **Travel Time**: Max 15 minutes between phases
- **Theme Rotation**: Alternates between "fun 🎉", "chill 🧘", and "outdoor 🌤"

## Testing

Run the test script to verify all endpoints:

```bash
python test_api.py
```

Make sure the server is running before executing tests.

## Data Storage

Team member data is stored in `team_profiles.json`. In production, consider using a proper database.

## Error Handling

All endpoints return appropriate HTTP status codes and error messages in JSON format:

- `200`: Success
- `201`: Created
- `400`: Bad Request
- `404`: Not Found
- `500`: Internal Server Error
