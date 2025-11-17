@echo off
REM Setup script for Data Engineering Interview Prep Platform (Windows)

echo Setting up Data Engineering Interview Prep Platform...

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo Docker is not installed. Please install Docker first.
    exit /b 1
)

docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo Docker Compose is not installed. Please install Docker Compose first.
    exit /b 1
)

REM Check for Anthropic API key
if "%ANTHROPIC_API_KEY%"=="" (
    echo ANTHROPIC_API_KEY environment variable is not set.
    set /p ANTHROPIC_API_KEY="Please enter your Anthropic API key: "
)

REM Create .env file if it doesn't exist
if not exist backend\.env (
    echo Creating backend\.env file...
    copy backend\.env.example backend\.env
    powershell -Command "(gc backend\.env) -replace 'your_claude_api_key_here', '%ANTHROPIC_API_KEY%' | Out-File -encoding ASCII backend\.env"
)

REM Create frontend .env.local if it doesn't exist
if not exist frontend\.env.local (
    echo Creating frontend\.env.local file...
    (
        echo NEXT_PUBLIC_API_URL=http://localhost:8000
        echo NEXT_PUBLIC_WS_URL=ws://localhost:8000
    ) > frontend\.env.local
)

echo Starting Docker containers...
docker-compose up -d

echo Waiting for services to be ready...
timeout /t 10 /nobreak >nul

echo Seeding database with interview questions...
docker-compose exec -T backend python app/seed_questions.py

echo.
echo Setup complete!
echo.
echo Your Data Engineering Interview Prep Platform is ready!
echo.
echo Access the application:
echo    Frontend: http://localhost:3000
echo    Backend API: http://localhost:8000
echo    API Docs: http://localhost:8000/docs
echo.
echo To stop the application, run: docker-compose down
echo To view logs, run: docker-compose logs -f
echo.
