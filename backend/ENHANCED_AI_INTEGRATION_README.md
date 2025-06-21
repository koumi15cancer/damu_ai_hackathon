Required Backend APIs for Team Bonding Event Planner
The backend development team must create the following APIs to meet the application's requirements for generating team bonding event plans and managing team member profiles.

1. POST /generate-plans

Description:Generates 3–5 team bonding event plans based on user inputs, team member profiles, and constraints such as budget, distance, and preferences. Integrates with an AI service for plan generation and Google Maps for location validation.

Request Body (JSON):  
{
"theme": "string", // e.g., "fun 🎉", "chill 🧘"
"budget_contribution": "string", // e.g., "Yes, up to 150,000 VND"
"available_members": ["string"], // List of team member names (optional)
"date_time": "string", // e.g., "2023-12-15 18:00" (optional)
"location_zone": "string" // e.g., "District 1" (optional)
}

Response (JSON):  
[
{
"phases": [
{
"activity": "string", // e.g., "Dinner"
"location": "string", // e.g., "123 Le Lai, District 1"
"map_link": "string", // Google Maps URL
"cost": number, // Per-person cost in VND
"indicators": ["string"] // e.g., ["indoor", "vegetarian-friendly"]
}
],
"total_cost": number, // Total per-person cost
"contribution_needed": number, // Additional contribution required (if > 300k)
"fit_analysis": "string", // e.g., "Suits team members in District 1"
"rating": number // 1–5 stars
}
]

Functionality:

Constructs an AI prompt using user inputs and team member preferences.
Calls an AI service (e.g., OpenAI GPT) to generate event plans.
Parses AI response to extract phases, locations, and costs.
Geocodes locations using Google Maps API to get coordinates.
Calculates distances and travel times between phases (≤ 2 km, ≤ 15 mins).
Validates budgets: Phase 1 ≤ 300k VND, 2 phases ≤ 450k VND, 3 phases ≤ 500k VND.
Generates Google Maps links for each phase.
Returns only valid plans, indicating contribution if total exceeds 300k VND.

2. GET /team-members

Description:Retrieves the list of all team member profiles.

Response (JSON):  
[
{
"id": "string",
"name": "string",
"location": "string",
"preferences": ["string"],
"vibe": "string"
}
]

Functionality:

Fetches and returns all team member data from the database.

3. POST /team-members

Description:Creates a new team member profile.

Request Body (JSON):  
{
"name": "string",
"location": "string",
"preferences": ["string"],
"vibe": "string"
}

Response (JSON):  
{
"id": "string",
"name": "string",
"location": "string",
"preferences": ["string"],
"vibe": "string"
}

Functionality:

Validates input data and adds a new team member to the database.

4. PUT /team-members/{id}

Description:Updates an existing team member profile.

Request Body (JSON):  
{
"name": "string",
"location": "string",
"preferences": ["string"],
"vibe": "string"
}

Response (JSON):  
{
"id": "string",
"name": "string",
"location": "string",
"preferences": ["string"],
"vibe": "string"
}

Functionality:

Updates the specified team member’s data in the database.

5. DELETE /team-members/{id}

Description:Deletes a team member profile.

Response (JSON):  
{
"message": "Team member deleted successfully"
}

Functionality:

Removes the specified team member from the database.

Additional Backend Requirements

External Integrations:

Google Maps API: For geocoding, distance calculations, and map links.
AI Service: For generating event plans (e.g., OpenAI GPT).

Validation & Constraints:

Ensure distances between phases ≤ 2 km and travel times ≤ 15 mins.
Enforce budget limits per phase configuration.
Validate all inputs for security and correctness.

Performance:

Ensure /generate-plans responds within 10 seconds.

Storage:

Use a database to store team member profiles and optionally historical event data for rotation strategies.

These APIs enable the core functionality of generating event plans and managing team data as per the requirements.
