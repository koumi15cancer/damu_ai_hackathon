# Frontend-Backend Integration Guide

This document describes how the frontend React application integrates with the new backend API.

## Overview

The frontend has been updated to work with the new backend API endpoints that follow the specifications in `ENHANCED_AI_INTEGRATION_README.md`. The integration provides:

- **Event Plan Generation**: Generate team bonding plans using AI
- **Team Member Management**: Full CRUD operations for team members
- **Real-time Data**: Live updates from the backend
- **Error Handling**: Graceful error handling and user feedback

## API Integration

### Base Configuration

The frontend connects to the backend at `http://localhost:5000` using axios for HTTP requests.

### Key Endpoints Used

1. **GET /team-members** - Load team member profiles
2. **POST /team-members** - Create new team member
3. **PUT /team-members/{id}** - Update team member
4. **DELETE /team-members/{id}** - Delete team member
5. **POST /generate-plans** - Generate team bonding plans
6. **GET /health** - Health check

## Component Structure

### Main App Component (`App.tsx`)

The main application component with three tabs:

1. **🎉 Event Planner** - Generate team bonding plans
2. **👥 Team Members** - Manage team member profiles
3. **🤖 AI Management** - AI provider management

### Team Member Management (`TeamMemberManagement.tsx`)

Dedicated component for managing team member profiles with:

- Add new team members
- Edit existing members
- Delete members
- View all member details

## Data Flow

### 1. Team Member Loading

```typescript
// Load team members on component mount
useEffect(() => {
  loadTeamMembers();
}, []);

const loadTeamMembers = async () => {
  try {
    const response = await axios.get("http://localhost:5000/team-members");
    setTeamMembers(response.data);
  } catch (error) {
    setError("Failed to load team members");
  }
};
```

### 2. Plan Generation

```typescript
const handleGeneratePlans = async () => {
  try {
    const response = await axios.post(
      "http://localhost:5000/generate-plans",
      userPreferences
    );
    setPlans(response.data);
  } catch (error) {
    setError("Failed to generate plans");
  }
};
```

### 3. Team Member CRUD Operations

```typescript
// Create
const response = await axios.post(
  "http://localhost:5000/team-members",
  newMember
);

// Update
const response = await axios.put(
  `http://localhost:5000/team-members/${id}`,
  updatedMember
);

// Delete
await axios.delete(`http://localhost:5000/team-members/${id}`);
```

## Data Structures

### Team Member Interface

```typescript
interface TeamMember {
  id: string;
  name: string;
  location: string;
  preferences: string[];
  vibe: string;
}
```

### Event Plan Interface

```typescript
interface EventPlan {
  phases: EventPhase[];
  total_cost: number;
  contribution_needed: number;
  fit_analysis: string;
  rating: number;
}

interface EventPhase {
  activity: string;
  location: string;
  map_link: string;
  cost: number;
  indicators: string[];
}
```

### User Preferences Interface

```typescript
interface UserPreferences {
  theme: string;
  budget_contribution: string;
  available_members: string[];
  date_time?: string;
  location_zone?: string;
}
```

## Features

### 1. Event Plan Generation

- **Theme Selection**: Choose from "fun 🎉", "chill 🧘", "outdoor 🌤"
- **Budget Management**: Set contribution limits
- **Member Selection**: Choose available team members
- **Date & Location**: Specify preferred date/time and location zone
- **Real-time Generation**: Instant plan generation with AI

### 2. Team Member Management

- **Add Members**: Create new team member profiles
- **Edit Members**: Update existing member information
- **Delete Members**: Remove team members
- **Preference Management**: Set member preferences and vibe
- **Visual Indicators**: Color-coded vibe indicators

### 3. Plan Display

- **Card Layout**: Clean card-based plan display
- **Cost Breakdown**: Per-person cost and contribution requirements
- **Rating System**: 1-5 star ratings for each plan
- **Phase Details**: Expandable phase information
- **Map Integration**: Google Maps links for each location

## Error Handling

The frontend includes comprehensive error handling:

```typescript
try {
  const response = await axios.get("http://localhost:5000/team-members");
  setTeamMembers(response.data);
} catch (error) {
  console.error("Failed to load team members:", error);
  setError(
    "Failed to load team members. Please check if the backend server is running."
  );
}
```

## Testing

### Manual Testing

1. Start the backend server: `cd backend && python app.py`
2. Start the frontend: `cd frontend && npm start`
3. Test each feature:
   - Load team members
   - Generate plans
   - Add/edit/delete team members

### Automated Testing

Run the integration test script:

```bash
# In browser console
node frontend/test-integration.js
```

## Development Setup

### Prerequisites

- Node.js 14+
- Python 3.7+
- Backend server running on port 5000

### Installation

1. Install frontend dependencies:

```bash
cd frontend
npm install
```

2. Start the development server:

```bash
npm start
```

3. Ensure backend is running:

```bash
cd backend
python app.py
```

## Troubleshooting

### Common Issues

1. **CORS Errors**: Ensure backend has CORS enabled
2. **Connection Refused**: Check if backend server is running on port 5000
3. **Data Not Loading**: Verify API endpoints are correct
4. **Plan Generation Fails**: Check AI service configuration

### Debug Mode

Enable debug logging in the browser console:

```javascript
// In browser console
localStorage.setItem("debug", "true");
```

## Future Enhancements

1. **Real-time Updates**: WebSocket integration for live updates
2. **Offline Support**: Service worker for offline functionality
3. **Advanced Filtering**: Filter plans by cost, location, preferences
4. **Export Features**: Export plans to calendar or PDF
5. **Mobile Optimization**: Responsive design improvements

## API Documentation

For detailed API documentation, see `backend/API_README.md`.

## Contributing

When making changes to the frontend:

1. Update TypeScript interfaces if API changes
2. Test all CRUD operations
3. Verify error handling
4. Update this documentation
