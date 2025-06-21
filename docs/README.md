# Team Bonding Event Planner

A comprehensive team bonding event planning application with AI-powered recommendations, location services, and team management features.

## 🚀 Quick Start

### Prerequisites
- Node.js (v16 or higher)
- Python 3.9+
- Google Maps API Key (optional, for real location data)

### Installation & Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd damu_ai_hackathon
   ```

2. **Start the application**
   ```bash
   # Using shell script (macOS/Linux)
   ./start.sh
   
   # Using batch file (Windows)
   start.bat
   ```

3. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000

# 📚 Documentation

Welcome to the Team Bonding Event Planner documentation! This directory contains all project documentation organized by category for easy navigation.

## 📁 Directory Structure

```
docs/
├── README.md                    # This file - documentation overview
├── index.md                     # Comprehensive documentation index
├── architecture/                # System architecture and design docs
│   ├── flow-documentation.md    # Complete system flow
│   ├── flow-summary.md          # High-level overview
│   └── ai-integration-explanation.md # AI integration details
├── backend/                     # Backend-specific documentation
│   ├── requirements.md          # Backend requirements
│   ├── ai-integration.md        # AI service integration
│   ├── enhanced-ai-integration.md # Advanced AI features
│   └── logging.md               # Logging configuration
├── frontend/                    # Frontend-specific documentation
│   ├── README.md                # Frontend setup and development
│   └── integration.md           # Frontend-backend integration
├── api/                         # API documentation
│   └── backend-api.md           # Complete API reference
└── setup/                       # Setup and configuration guides
    └── ai-integration-setup.md  # AI provider setup
```

## 🚀 Quick Navigation

### For New Users
1. **[Main Project README](../README.md)** - Start here for project overview
2. **[AI Integration Setup](setup/ai-integration-setup.md)** - Set up AI providers
3. **[Backend API](api/backend-api.md)** - Understand available APIs

### For Developers
1. **[Architecture Overview](architecture/flow-summary.md)** - System architecture
2. **[Backend Requirements](backend/requirements.md)** - Backend specifications
3. **[Frontend Integration](frontend/integration.md)** - Frontend development

### For Contributors
1. **[Documentation Index](index.md)** - Complete documentation navigation
2. **[Flow Documentation](architecture/flow-documentation.md)** - Detailed system flow
3. **[Enhanced AI Integration](backend/enhanced-ai-integration.md)** - Advanced features

## 📖 Documentation Categories

### 🏗️ Architecture & Design
- **System Architecture**: Complete system design and data flow
- **AI Integration**: How AI services are integrated and used
- **Component Design**: Individual component architecture

### 🔧 Setup & Configuration
- **Environment Setup**: How to set up development environment
- **API Configuration**: Setting up external services (AI, Maps)
- **Deployment**: Production deployment guides

### 🎯 Development Guides
- **Backend Development**: Python/Flask development
- **Frontend Development**: React/TypeScript development
- **API Development**: Creating and documenting APIs

### 📋 Feature Documentation
- **Core Features**: Event planning, team management, location services
- **AI Features**: AI-powered event generation and recommendations
- **Advanced Features**: Advanced capabilities and optimizations

## 🔍 Finding Information

### By Topic
- **AI Integration**: Check `architecture/ai-integration-explanation.md` and `backend/ai-integration.md`
- **API Reference**: Check `api/backend-api.md`
- **Setup Guides**: Check `setup/` directory
- **Architecture**: Check `architecture/` directory

### By Role
- **End Users**: Start with main README and setup guides
- **Frontend Developers**: Check `frontend/` directory
- **Backend Developers**: Check `backend/` and `api/` directories
- **DevOps**: Check setup and deployment guides

## 📝 Contributing to Documentation

When adding new documentation:

1. **Choose the right directory** based on the content type
2. **Use descriptive filenames** with kebab-case (e.g., `my-feature-guide.md`)
3. **Update the index** in `index.md` to include your new document
4. **Follow the existing format** and style
5. **Include examples** and code snippets where helpful

### Documentation Standards

- **Use Markdown** for all documentation
- **Include headers** for easy navigation
- **Add code examples** where relevant
- **Keep it concise** but comprehensive
- **Update regularly** as features change

## 🔗 External Resources

- **[GitHub Repository](https://github.com/your-repo)** - Source code
- **[Issue Tracker](https://github.com/your-repo/issues)** - Bug reports and feature requests
- **[Wiki](https://github.com/your-repo/wiki)** - Additional community documentation

---

**Need help?** Check the [Documentation Index](index.md) for comprehensive navigation, or open an issue for documentation improvements.

## 🎯 Features

### Core Features
- **AI-Powered Event Planning** - Generate personalized team bonding events
- **Location Services** - Real-time location data and Google Maps integration
- **Team Management** - Comprehensive team member profiles and preferences
- **Budget Management** - Cost tracking and contribution management
- **Travel Optimization** - Distance and travel time calculations

### AI Integration
- **Multiple AI Providers** - Support for OpenAI, Google Gemini, and Anthropic Claude
- **Smart Recommendations** - Context-aware event suggestions
- **Constraint Validation** - Budget, distance, and time constraint checking
- **Fallback Systems** - Graceful degradation when AI services are unavailable

### Location Services
- **Google Maps Integration** - Real-time geocoding and map links
- **Travel Time Calculation** - Accurate travel time between locations
- **Location Validation** - Constraint checking for event phases
- **Zone Management** - Ho Chi Minh City district-based organization

## 🛠️ Technology Stack

### Backend
- **Python Flask** - Web framework
- **Google Maps API** - Location services
- **Multiple AI APIs** - OpenAI, Google Gemini, Anthropic
- **JSON Storage** - Simple data persistence

### Frontend
- **React TypeScript** - Modern UI framework
- **Material-UI** - Component library
- **Axios** - HTTP client
- **Responsive Design** - Mobile-friendly interface

## 🏗️ Project Structure

```
damu_ai_hackathon/
├── docs/                    # 📚 Documentation
│   ├── architecture/        # System architecture docs
│   │   ├── flow-documentation.md
│   │   ├── flow-summary.md
│   │   └── ai-integration-explanation.md
│   ├── backend/            # Backend-specific docs
│   │   ├── requirements.md
│   │   ├── ai-integration.md
│   │   ├── enhanced-ai-integration.md
│   │   └── logging.md
│   ├── frontend/           # Frontend-specific docs
│   │   ├── README.md
│   │   └── integration.md
│   ├── api/                # API documentation
│   └── setup/              # Setup and configuration
├── backend/                # 🐍 Backend application
│   ├── services/           # Core services
│   │   ├── ai_service.py   # AI integration
│   │   ├── maps_service.py # Location services
│   │   ├── location_service.py # Enhanced location handling
│   │   └── calendar_service.py # Calendar integration
│   ├── app.py              # Main Flask application
│   └── config.py           # Configuration
├── frontend/               # ⚛️ Frontend application
│   ├── src/                # React source code
│   ├── public/             # Static assets
│   └── package.json        # Dependencies
└── tests/                  # 🧪 Test files
```

## 🚀 Getting Started

### For Developers

1. **Backend Development**
   ```bash
   cd backend
   pip install -r requirements.txt
   python app.py
   ```

2. **Frontend Development**
   ```bash
   cd frontend
   npm install
   npm start
   ```

3. **Running Tests**
   ```bash
   cd backend
   python -m pytest tests/
   ```

### For Users

1. **Set up AI API keys** (optional)
   - Follow the [AI Integration Setup](setup/ai-integration-setup.md) guide
   - Configure your preferred AI provider

2. **Set up Google Maps API** (optional)
   - Get a Google Maps API key
   - Add it to your environment variables

3. **Start the application**
   - Use the provided start scripts
   - Access via web browser

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For questions or issues:
1. Check the relevant documentation section
2. Review the [Architecture Documentation](architecture/flow-documentation.md)
3. Open an issue on GitHub

---

**Happy Team Bonding! 🎉**
