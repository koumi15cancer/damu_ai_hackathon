# Team Bonding Activity Suggester

An AI-powered application that suggests team bonding activities based on team members' availability, locations, and interests. The application integrates with Google Calendar to find common free time slots, Google Maps to determine central meeting locations, and OpenAI to generate personalized activity suggestions.

## Features

- **Google Calendar Integration**: Automatically finds common free time slots for team members
- **Location-based Suggestions**: Uses Google Maps to find central meeting locations and nearby places
- **AI-powered Recommendations**: Generates personalized activity suggestions using OpenAI
- **Team Member Management**: Add multiple team members with their locations and calendar IDs
- **Interactive UI**: Modern and user-friendly interface built with React and Material-UI

## Tech Stack

- **Frontend**: React with TypeScript and Material-UI
- **Backend**: Python with Flask
- **APIs**:
  - Google Calendar API for availability checking
  - Google Maps API for location services
  - OpenAI API for activity suggestions
- **Data Storage**: JSON file for sample data

## Prerequisites

- Node.js (v14 or higher)
- Python (v3.8 or higher)
- npm or yarn
- Google Cloud Platform account with the following APIs enabled:
  - Google Calendar API
  - Google Maps API
- OpenAI API key

## Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd team-bonding-suggester
   ```

2. Set up the backend:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Set up API keys:
   ```bash
   python setup_env.py
   ```
   Follow the prompts to enter your API keys:
   - Google Client ID and Secret (from Google Cloud Console)
   - OpenAI API key
   - Google Maps API key

4. Set up the frontend:
   ```bash
   cd ../frontend
   npm install
   ```

## Running the Application

1. Start the backend server:
   ```bash
   cd backend
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   python app.py
   ```

2. Start the frontend development server:
   ```bash
   cd frontend
   npm start
   ```

3. Open your browser and navigate to http://localhost:3000

## Usage

1. Add team members:
   - Click "Add Team Member" to add a new team member
   - Enter their name, email, and address
   - Click "Connect Google Calendar" to authorize calendar access

2. Set preferences:
   - Enter team interests (comma-separated)
   - Set budget per person
   - Click "Get Suggestions"

3. View results:
   - The application will show:
     - Central meeting location
     - Available time slots
     - Suggested activities with nearby places
     - Cost and duration for each activity

## Project Structure

```
team-bonding-suggester/
├── backend/
│   ├── app.py
│   ├── config.py
│   ├── requirements.txt
│   ├── setup_env.py
│   └── services/
│       ├── calendar_service.py
│       ├── maps_service.py
│       └── ai_service.py
└── frontend/
    ├── package.json
    ├── tsconfig.json
    └── src/
        ├── App.tsx
        └── index.tsx
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 