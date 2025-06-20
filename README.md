# 🎉 Team Bonding Event Planner

A comprehensive AI-powered application for organizing thoughtful, fun, and inclusive monthly team bonding events that align with individual preferences, energy levels, and logistics.

## 🚀 Features

### Core Functionality

- **AI-Powered Event Planning**: Generate 3-5 team bonding plans using advanced AI models
- **Multi-Phase Events**: Support for 1-phase (dinner) or multi-phase (dinner → karaoke → bar) activities
- **Smart Location Planning**: Each phase within 2km of others, max 15 minutes travel time
- **Budget Management**: 300,000 VND base budget with optional contributions up to 150,000 VND
- **Theme Rotation**: Rotate between "fun 🎉", "chill 🧘", and "outdoor 🌤" themes

### Team Member Management

- **Preference-Based Matching**: Consider individual preferences, locations, and vibes
- **Location Balance**: Account for member home locations to avoid unfair travel distances
- **Availability Tracking**: Select which team members are available for events
- **Vibe Analysis**: Match events to team member energy levels (Chill, Energetic, Mixed)

### Event Planning Features

- **Phase Flexibility**: Optional phases 2 & 3 based on team vibe
- **Cost Estimation**: Detailed per-person cost breakdown for each phase
- **Location Details**: Addresses with Google Maps links
- **Venue Information**: Indoor/outdoor, vegetarian-friendly, alcohol-friendly indicators
- **Travel Planning**: Distance and travel time between phases

### Long-term Strategy

- **Vibe Alternation**: Rotate event themes monthly
- **Location Fairness**: Distribute events across city zones
- **Preference Rotation**: Mix activity types across months
- **Host Rotation**: Let different team members suggest ideas

## 🏗️ Architecture

### Backend (Python/Flask)

- **AI Integration**: Multi-provider AI service (OpenAI, Google Gemini)
- **Team Profiles**: JSON-based team member data management
- **Event Generation**: AI-powered plan creation with structured prompts
- **API Endpoints**: RESTful API for frontend communication

### Frontend (React/TypeScript)

- **Modern UI**: Material-UI components with beautiful, responsive design
- **Interactive Forms**: User preference selection and team member management
- **Plan Visualization**: Card-based plan display with detailed dialogs
- **Real-time Updates**: Dynamic plan generation and display

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

```bash
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Set up environment variables (create .env file)
cp .env.example .env
# Edit .env with your API keys:
# OPENAI_API_KEY=your_openai_key
# GOOGLE_AI_API_KEY=your_google_key

# Run the backend server
python app.py
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start the development server
npm start
```

## 📋 Team Member Profiles

The application includes 10 team members with diverse preferences:

| Name      | Location                | Preferences                             | Vibe      |
| --------- | ----------------------- | --------------------------------------- | --------- |
| Ben       | Mizuki Park, Binh Chanh | Vegetarian, Chill places, Cafe-hopping  | Chill     |
| Cody      | Huynh Tan Phat, D7      | Meat-lover, BBQ, Bar/beer club, Karaoke | Energetic |
| Lil Thanh | Le Duc Tho, Go Vap      | Hotpot, Outdoor walks, Chill cafes      | Chill     |
| Big Thanh | D1                      | Hotpot, Karaoke, Bar                    | Energetic |
| Mason     | D3                      | Games, Movie night, Office snacks       | Mixed     |
| Hoa       | D10                     | Vegetarian, Asian food, Dinner & chat   | Chill     |
| Khang     | Tan Phu                 | BBQ, Karaoke, Bar                       | Energetic |
| Huy       | Binh Thanh              | Games, Cafe-hopping, Movie night        | Mixed     |
| Seven     | Phu Nhuan               | BBQ, Rooftop bar, Dinner & chat         | Energetic |
| Roy       | D5                      | Hotpot, Karaoke, Bar, Games             | Energetic |

## 🎯 Usage

### 1. Set Event Preferences

- Choose monthly theme (Fun, Chill, or Outdoor)
- Set optional budget contribution (0-150,000 VND)
- Select preferred date and location zone
- Choose available team members

### 2. Generate Plans

- Click "Generate Event Plans" to create AI-powered suggestions
- Review 3-5 different event options
- Each plan includes detailed phase breakdown

### 3. Review Plan Details

- Click on any plan to see full details
- View cost breakdown, team fit analysis, and long-term strategy
- Check venue details, travel times, and special requirements

### 4. Save and Execute

- Save preferred plans for future reference
- Export to calendar (future feature)
- Share with team members

## 🔧 Configuration

### AI Provider Selection

The backend supports multiple AI providers:

- **OpenAI GPT**: Advanced reasoning capabilities
- **Google Gemini**: Multimodal creative capabilities

### Budget Constraints

- **Base Budget**: 300,000 VND per person
- **Phase 1**: Must fit within base budget
- **Phase 2**: Optional, total max 450,000 VND
- **Phase 3**: Optional if hyped, total max 500,000 VND

### Location Rules

- **Distance**: Each phase within 2km of others
- **Travel Time**: Maximum 15 minutes between phases
- **Zone Balance**: Rotate across city zones for fairness

## 🚀 Future Enhancements

### Planned Features

- **Calendar Integration**: Google Calendar event creation
- **Payment Integration**: Team contribution tracking
- **Photo Sharing**: Event photo galleries
- **Feedback System**: Post-event ratings and comments
- **Mobile App**: Native mobile application
- **Advanced Analytics**: Event success metrics and trends

### AI Improvements

- **Personalized Learning**: AI learns from team preferences over time
- **Weather Integration**: Outdoor event weather considerations
- **Traffic Analysis**: Real-time travel time optimization
- **Venue Recommendations**: AI-suggested new venues based on preferences

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **AI Providers**: OpenAI and Google for their AI services
- **Material-UI**: Beautiful React components
- **Flask**: Lightweight Python web framework
- **Team Members**: For providing real-world use cases and feedback

---

**Built with ❤️ for better team bonding experiences**
