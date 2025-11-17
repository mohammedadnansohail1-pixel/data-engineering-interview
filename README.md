# Data Engineering Interview Preparation Platform

An AI-powered full-stack web application that helps data engineers prepare for technical interviews using real-time feedback, adaptive learning paths, and intelligent coaching powered by Claude AI.

## Features

### MVP Features
- **User Authentication**: Secure JWT-based authentication with registration and login
- **Question Bank**: 15+ curated interview questions covering:
  - SQL queries and optimization
  - Python/PySpark data processing
  - System design scenarios
  - Behavioral interview questions
- **Interactive Code Editor**: Monaco Editor with syntax highlighting for Python and SQL
- **AI-Powered Feedback**: Real-time code evaluation and feedback using Claude Sonnet 4.5
- **Progressive Hints System**: Get up to 3 contextual hints per question
- **Progress Dashboard**: Track completed questions, average scores, and recent activity
- **Question Filtering**: Browse by category, difficulty, and search keywords

## Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **PostgreSQL**: Relational database
- **SQLAlchemy**: ORM for database operations
- **Redis**: Caching and session management
- **Anthropic Claude API**: AI-powered code evaluation
- **JWT**: Secure authentication

### Frontend
- **Next.js 14**: React framework with App Router
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first styling
- **Monaco Editor**: VS Code-based code editor
- **Zustand**: Lightweight state management
- **Axios**: HTTP client

### DevOps
- **Docker & Docker Compose**: Containerization
- **PostgreSQL 15**: Database
- **Redis 7**: Cache

## Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── endpoints/
│   │   │   │   ├── auth.py          # Authentication endpoints
│   │   │   │   ├── questions.py     # Question management
│   │   │   │   ├── practice.py      # Code submission & evaluation
│   │   │   │   └── progress.py      # User progress tracking
│   │   │   └── deps.py              # Dependencies
│   │   ├── core/
│   │   │   ├── config.py            # Configuration
│   │   │   ├── database.py          # Database setup
│   │   │   └── security.py          # JWT & password hashing
│   │   ├── models/                  # SQLAlchemy models
│   │   ├── schemas/                 # Pydantic schemas
│   │   ├── services/
│   │   │   ├── ai_service.py        # Claude AI integration
│   │   │   └── code_executor.py     # Code execution engine
│   │   ├── main.py                  # FastAPI app
│   │   └── seed_questions.py        # Database seeding
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── app/
│   │   ├── auth/
│   │   │   ├── login/               # Login page
│   │   │   └── register/            # Registration page
│   │   ├── dashboard/               # User dashboard
│   │   ├── questions/               # Questions browser
│   │   ├── interview/[id]/          # Interview interface
│   │   ├── layout.tsx
│   │   └── page.tsx
│   ├── components/
│   │   └── Navbar.tsx               # Navigation component
│   ├── hooks/
│   │   └── useAuth.ts               # Authentication hook
│   ├── lib/
│   │   ├── api.ts                   # API client
│   │   └── utils.ts                 # Utility functions
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

## Getting Started

### Prerequisites
- Docker and Docker Compose installed
- Anthropic API key (get one at https://console.anthropic.com/)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd data-engineering-interview
   ```

2. **Set up environment variables**

   Create a `.env` file in the project root (or use `backend/.env`):
   ```bash
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   ```

3. **Start the application**
   ```bash
   docker-compose up --build
   ```

   This will start:
   - PostgreSQL on port 5432
   - Redis on port 6379
   - Backend API on http://localhost:8000
   - Frontend on http://localhost:3000

4. **Seed the database**

   In a new terminal, run:
   ```bash
   docker-compose exec backend python app/seed_questions.py
   ```

5. **Access the application**

   Open your browser and go to http://localhost:3000

### Alternative: Local Development (Without Docker)

#### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set environment variables
export DATABASE_URL=postgresql://deprep:devpassword@localhost:5432/interview_prep
export REDIS_URL=redis://localhost:6379
export ANTHROPIC_API_KEY=your_key_here

# Run database migrations (ensure PostgreSQL is running)
python app/seed_questions.py

# Start the server
uvicorn app.main:app --reload --port 8000
```

#### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## Usage

### 1. Register an Account
- Navigate to http://localhost:3000
- Click "Sign up" and create an account
- Fill in your details (experience level, target role, etc.)

### 2. Browse Questions
- After login, you'll see the dashboard
- Click "Browse Questions" to see all available questions
- Filter by category (SQL, Python, etc.) or difficulty (Easy, Medium, Hard)

### 3. Practice Questions
- Click on any question to start practicing
- Write your solution in the code editor
- Click "Submit Code" to get AI feedback
- Use "Get Hint" if you're stuck (up to 3 hints per question)

### 4. Track Progress
- View your dashboard to see:
  - Total questions completed
  - Average score
  - Recent activity
  - Skill proficiency

## API Documentation

Once the backend is running, visit http://localhost:8000/docs for interactive API documentation (Swagger UI).

### Key Endpoints

#### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login (returns JWT token)
- `GET /api/auth/me` - Get current user info

#### Questions
- `GET /api/questions/` - List questions (with filters)
- `GET /api/questions/{id}` - Get specific question

#### Practice
- `POST /api/practice/start` - Start question attempt
- `POST /api/practice/submit` - Submit code for evaluation
- `POST /api/practice/hint` - Get hint

#### Progress
- `GET /api/progress/dashboard` - Get dashboard stats
- `GET /api/progress/skills` - Get skill breakdown

## Database Schema

### Tables
- **users**: User accounts and profiles
- **questions**: Interview questions
- **attempts**: User question attempts and submissions
- **user_progress**: Skill proficiency tracking
- **practice_sessions**: Practice session metadata

See `backend/app/models/` for detailed schema definitions.

## AI Integration

The platform uses Claude Sonnet 4.5 for:

1. **Code Evaluation**: Analyzes submissions for correctness, quality, efficiency
2. **Feedback Generation**: Provides actionable improvement suggestions
3. **Hint System**: Generates progressive hints without giving away solutions
4. **Behavioral Assessment**: Evaluates STAR-format behavioral responses

### AI Prompts
See `backend/app/services/ai_service.py` for prompt templates.

## Configuration

### Backend Configuration
Edit `backend/app/core/config.py` or use environment variables:

```python
DATABASE_URL=postgresql://user:pass@host:port/dbname
REDIS_URL=redis://host:port
ANTHROPIC_API_KEY=sk-ant-...
JWT_SECRET=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Frontend Configuration
Edit `frontend/.env.local`:

```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
```

## Development

### Adding New Questions

1. Edit `backend/app/seed_questions.py`
2. Add question objects to the `questions` list
3. Run the seed script:
   ```bash
   docker-compose exec backend python app/seed_questions.py
   ```

### Running Tests

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## Troubleshooting

### Database Connection Issues
- Ensure PostgreSQL is running
- Check `DATABASE_URL` in environment variables
- Verify port 5432 is not in use by another service

### Frontend Build Issues
- Delete `node_modules` and `.next` folders
- Run `npm install` again
- Clear browser cache

### AI API Issues
- Verify your Anthropic API key is valid
- Check API rate limits and quotas
- Review API error messages in backend logs

## Roadmap

### Planned Features
- System design whiteboard tool
- Mock interview scheduling with AI interviewer
- Peer practice matching
- Company-specific question packs
- Video recording and analysis
- Resume review and optimization
- Mobile app (React Native)

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For issues and questions:
- Open an issue on GitHub
- Check existing documentation
- Review API docs at /docs endpoint

## Acknowledgments

- Built with FastAPI, Next.js, and Claude AI
- Interview questions inspired by real data engineering interviews
- UI components styled with Tailwind CSS
- Code editor powered by Monaco Editor

---

**Happy Practicing! Good luck with your interviews!** 🚀
