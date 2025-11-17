# Quick Start Guide

Get up and running with the Data Engineering Interview Prep Platform in 5 minutes!

## Prerequisites

- Docker and Docker Compose installed
- Anthropic API key ([get one here](https://console.anthropic.com/))

## Option 1: Automatic Setup (Recommended)

### Linux/macOS
```bash
# Set your API key
export ANTHROPIC_API_KEY=your_key_here

# Run setup script
./setup.sh
```

### Windows
```cmd
# Set your API key
set ANTHROPIC_API_KEY=your_key_here

# Run setup script
setup.bat
```

## Option 2: Using Makefile

```bash
# Set your API key
export ANTHROPIC_API_KEY=your_key_here

# Run setup
make setup

# View all available commands
make help
```

## Option 3: Manual Setup

```bash
# 1. Set your API key
export ANTHROPIC_API_KEY=your_key_here

# 2. Create backend .env file
cp backend/.env.example backend/.env
# Edit backend/.env and add your ANTHROPIC_API_KEY

# 3. Start services
docker-compose up -d

# 4. Wait for services to be ready (about 10 seconds)
sleep 10

# 5. Seed the database
docker-compose exec backend python app/seed_questions.py
```

## Access the Application

Once setup is complete, access the application at:

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## First Steps

1. **Register an Account**
   - Go to http://localhost:3000
   - Click "Sign up" and create your account
   - Fill in your experience level and target role

2. **Browse Questions**
   - After login, click "Browse Questions"
   - Filter by category (SQL, Python, System Design, etc.)
   - Click any question to start practicing

3. **Practice**
   - Write your solution in the code editor
   - Click "Submit Code" for AI feedback
   - Use "Get Hint" if you're stuck (up to 3 hints)

4. **Track Progress**
   - View your dashboard to see completed questions
   - Check your average score and skill proficiency
   - Review recent activity

## Useful Commands

```bash
# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Restart services
docker-compose restart

# Access backend shell
docker-compose exec backend /bin/bash

# Access database
docker-compose exec postgres psql -U deprep -d interview_prep

# Run tests
docker-compose exec backend pytest tests/

# Reseed database (will skip if already seeded)
docker-compose exec backend python app/seed_questions.py
```

## Troubleshooting

### Port Already in Use
If ports 3000, 5432, or 8000 are already in use, edit `docker-compose.yml` to change the port mappings.

### Database Connection Failed
Wait a few more seconds for PostgreSQL to fully start, then try again.

### API Key Issues
Make sure your `ANTHROPIC_API_KEY` is set correctly in `backend/.env`.

### Frontend Not Loading
Check that all services are running:
```bash
docker-compose ps
```

All services should show "Up" status.

## Next Steps

- Check out the full README for advanced features
- Explore the API documentation at http://localhost:8000/docs
- Review the codebase to understand the architecture
- Add your own custom questions to `backend/app/seed_questions.py`

## Need Help?

- Check the main README.md for detailed documentation
- Review API docs at http://localhost:8000/docs
- Open an issue on GitHub

---

**Happy practicing! Good luck with your interviews!** 🚀
