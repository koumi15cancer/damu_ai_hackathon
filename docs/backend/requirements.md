# Team Bonding Event Planner: Backend Requirements Document

## 1. Overview
The backend of the Team Bonding Event Planner is responsible for managing data, processing user inputs, generating event plans via AI integration, and ensuring all constraints and guidelines are met. It must handle team member profiles, construct dynamic AI prompts, validate generated plans, and integrate with external services like Google Maps for location-based features.

## 2. Key Components and Functionalities
The backend must support the following key components and functionalities:

### 2.1 Team Member Profiles
- **Storage and Management:**
  - Store team member data including name, location, preferences, and vibe.
  - Allow for creation, updating, and deletion of profiles.
- **Data Structure:**
  - Example: `{ "name": "Ben", "location": "Mizuki Park, Binh Chanh", "preferences": ["Vegetarian", "Chill places", "Cafe-hopping"], "vibe": "Chill" }`

### 2.2 User Inputs Handling
- **Inputs:**
  - Theme preference (fun 🎉, chill 🧘, outdoor 🌤)
  - Optional budget contributions (e.g., up to 150,000 VND)
  - Team member availability (list of available members)
  - Specific date/time (optional)
  - Preferred location zone (e.g., "District 1")
- **Processing:**
  - Validate and sanitize inputs to prevent security vulnerabilities.

### 2.3 Event Plan Generation
- **AI Prompt Construction:**
  - Dynamically build a prompt based on user inputs, team profiles, and constraints.
  - Include budget, distance rules, location balance, and phase flexibility.
- **AI Integration:**
  - Send the prompt to an AI service (e.g., OpenAI GPT) to generate event plans.
  - Parse the AI response to extract structured event plans.
- **Plan Validation:**
  - Ensure plans meet budget, distance, and travel time constraints.
  - Verify location balance and optional phase requirements.

### 2.4 Constraints and Guidelines Enforcement
- **Budget Constraints:**
  - Phase 1: ≤ 300,000 VND/person
  - Phase 2 (optional): Total ≤ 450,000 VND/person
  - Phase 3 (optional): Total ≤ 500,000 VND/person
- **Distance and Travel Time:**
  - Each phase within 2 km and 15 minutes travel time of others.
- **Location Balance:**
  - Consider team members' home locations to avoid excessive travel.
- **Phase Flexibility:**
  - Phases 2 and 3 are optional based on the event vibe.

### 2.5 Long-Term Rotation Strategy
- **Historical Data Tracking:**
  - Store past event themes, locations, and hosts.
- **Rotation Logic:**
  - Implement logic to suggest future themes and locations based on rotation rules (e.g., vibe alternation, location fairness).

### 2.6 Integration with External Services
- **Google Maps API:**
  - Retrieve location coordinates, calculate distances, and generate map links.
- **AI Service:**
  - Integrate with AI for generating event plans (e.g., OpenAI GPT).

### 2.7 Data Storage
- **Database:**
  - Store team member profiles and historical event data.
  - Support JSON data types (e.g., MongoDB, PostgreSQL with JSONB).

### 2.8 Security
- **API Key Management:**
  - Securely store and manage keys for external services.
- **Input Validation:**
  - Sanitize and validate all user inputs to prevent injection attacks.

### 2.9 Performance
- **Response Times:**
  - Plan generation: ≤ 10 seconds.
  - API responses: ≤ 2 seconds for standard requests.
- **Optimization:**
  - Use caching for frequently accessed data (e.g., team profiles).
  - Implement asynchronous processing for AI and Google Maps API calls.

### 2.10 Scalability
- **Concurrent Requests:**
  - Handle multiple simultaneous requests efficiently.
- **Team Size:**
  - Support up to 20 team members with potential for growth.

## 3. API Endpoints
The backend must provide the following API endpoints:

### 3.1 POST /generate-plans
- **Description:**
  - Accepts user inputs and generates event plans via AI.
- **Request Body:**
  - Theme, budget contribution, availability, date/time, location zone.
- **Response:**
  - List of 3–5 event plans with details (phases, costs, locations, etc.).

### 3.2 GET /team-members
- **Description:**
  - Retrieves the list of team member profiles.
- **Response:**
  - Array of team member objects.

### 3.3 POST /team-members
- **Description:**
  - Creates a new team member profile.
- **Request Body:**
  - Team member data (name, location, preferences, vibe).

### 3.4 PUT /team-members/{id}
- **Description:**
  - Updates an existing team member profile.
- **Request Body:**
  - Updated team member data.

### 3.5 DELETE /team-members/{id}
- **Description:**
  - Deletes a team member profile.

## 4. AI Integration Details
- **Prompt Construction:**
  - Build a dynamic prompt including user inputs, team profiles, and constraints.
  - Example: "Generate plans for a 'fun 🎉' event in District 1 with a 150,000 VND optional contribution."
- **API Call:**
  - Send the prompt to the AI service and handle the response.
- **Response Parsing:**
  - Extract structured event plans from the AI's text response.
  - Validate plans against constraints (budget, distance, etc.).

## 5. Google Maps Integration
- **Location Services:**
  - Use Google Maps API to:
    - Get coordinates for event locations.
    - Calculate distances and travel times between phases.
    - Generate map links for each phase.
- **API Usage:**
  - Ensure efficient use to avoid exceeding rate limits.

## 6. Validation and Constraints Logic
- **Budget Validation:**
  - Check per-phase and total costs against budget limits.
- **Distance and Travel Time:**
  - Use Google Maps API to verify distances and travel times.
- **Location Balance:**
  - Calculate average distance from team members' locations to event zones.
  - Prioritize zones closer to the majority of team members.

## 7. Long-Term Rotation Strategy Implementation
- **Data Storage:**
  - Store past event details (theme, location, host).
- **Rotation Logic:**
  - Alternate themes monthly (e.g., fun → chill → outdoor).
  - Rotate locations to ensure fairness.
  - Allow for host rotation by suggesting team members.

## 8. Security Measures
- **API Key Security:**
  - Store keys in environment variables or a secure vault.
- **Input Validation:**
  - Use libraries to sanitize inputs and prevent SQL injection, XSS, etc.

## 9. Performance Optimization Strategies
- **Caching:**
  - Cache team member profiles and frequently accessed data.
- **Asynchronous Processing:**
  - Use async/await for non-blocking API calls.
- **Database Indexing:**
  - Index frequently queried fields for faster access.

## 10. Error Handling and Logging
- **Error Handling:**
  - Implement try-catch blocks for external service calls.
  - Return user-friendly error messages to the frontend.
- **Logging:**
  - Log requests, responses, and errors for debugging.
  - Monitor performance metrics (e.g., response times).

## 11. Additional Considerations
- **Database Choice:**
  - Use MongoDB or PostgreSQL with JSONB for flexible data storage.
- **API Documentation:**
  - Provide Swagger/OpenAPI documentation for all endpoints.
- **Testing:**
  - Write unit tests for critical components (e.g., prompt construction, validation).
  - Conduct integration tests for AI and Google Maps interactions.

---

This requirements document provides a clear and comprehensive guide for the backend team to develop the necessary components and functionalities for the Team Bonding Event Planner. It ensures that all constraints are met, integrations are handled properly, and the system is secure, scalable, and performant.