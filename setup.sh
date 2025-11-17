#!/bin/bash

# Setup script for Data Engineering Interview Prep Platform
set -e

echo "🚀 Setting up Data Engineering Interview Prep Platform..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Check for Anthropic API key
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "⚠️  ANTHROPIC_API_KEY environment variable is not set."
    echo "Please enter your Anthropic API key:"
    read -r ANTHROPIC_API_KEY
    export ANTHROPIC_API_KEY
fi

# Create .env file if it doesn't exist
if [ ! -f backend/.env ]; then
    echo "📝 Creating backend/.env file..."
    cp backend/.env.example backend/.env
    sed -i.bak "s/your_claude_api_key_here/$ANTHROPIC_API_KEY/" backend/.env
    rm backend/.env.bak 2>/dev/null || true
fi

# Create frontend .env.local if it doesn't exist
if [ ! -f frontend/.env.local ]; then
    echo "📝 Creating frontend/.env.local file..."
    cat > frontend/.env.local <<EOF
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
EOF
fi

echo "🐳 Starting Docker containers..."
docker-compose up -d

echo "⏳ Waiting for services to be ready..."
sleep 10

# Check if PostgreSQL is ready
until docker-compose exec -T postgres pg_isready -U deprep > /dev/null 2>&1; do
    echo "⏳ Waiting for PostgreSQL..."
    sleep 2
done

echo "✅ PostgreSQL is ready!"

# Seed the database
echo "🌱 Seeding database with interview questions..."
docker-compose exec -T backend python app/seed_questions.py

echo ""
echo "✅ Setup complete!"
echo ""
echo "🎉 Your Data Engineering Interview Prep Platform is ready!"
echo ""
echo "📍 Access the application:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "📚 To stop the application, run: docker-compose down"
echo "📚 To view logs, run: docker-compose logs -f"
echo ""
