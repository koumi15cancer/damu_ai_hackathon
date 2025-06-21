@echo off
echo 🎉 Starting Team Bonding Event Planner...
echo ========================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8+ first.
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is not installed. Please install Node.js 16+ first.
    pause
    exit /b 1
)

REM Check if npm is installed
npm --version >nul 2>&1
if errorlevel 1 (
    echo ❌ npm is not installed. Please install npm first.
    pause
    exit /b 1
)

echo ✅ Prerequisites check passed

REM Install backend dependencies
echo 📦 Installing backend dependencies...
cd backend

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat
pip install -r requirements.txt

REM Check if .env file exists
if not exist ".env" (
    echo ⚠️  No .env file found. Creating template...
    (
        echo # AI API Keys (get these from respective providers
        echo OPENAI_API_KEY=your_openai_api_key_here
        echo GOOGLE_AI_API_KEY=your_google_ai_api_key_here
        echo.
        echo # Google Calendar API (optional
        echo GOOGLE_CLIENT_ID=your_google_client_id_here
        echo GOOGLE_CLIENT_SECRET=your_google_client_secret_here
        echo.
        echo # Google Maps API (optional
        echo GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here
    ) > .env
    echo 📝 Please edit backend\.env with your API keys
    echo    You can get API keys from:
    echo    - OpenAI: https://platform.openai.com/api-keys
    echo    - Google AI: https://makersuite.google.com/app/apikey
)

REM Start backend server in background
echo 🚀 Starting backend server...
start "Backend Server" python app.py
cd ..

REM Wait a moment for backend to start
timeout /t 3 /nobreak >nul

REM Install frontend dependencies
echo 📦 Installing frontend dependencies...
cd frontend
npm install

REM Start frontend server
echo 🚀 Starting frontend server...
start "Frontend Server" npm start
cd ..

echo.
echo 🎯 Application is starting up...
echo    Backend: http://localhost:5000
echo    Frontend: http://localhost:3000
echo.
echo 📋 Next steps:
echo    1. Wait for both servers to fully start
echo    2. Open http://localhost:3000 in your browser
echo    3. Configure API keys in backend\.env if needed
echo    4. Start planning your team bonding events!
echo.
echo 🛑 To stop the servers, close the command windows or press Ctrl+C
pause 