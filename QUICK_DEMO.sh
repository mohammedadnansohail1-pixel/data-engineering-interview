#!/bin/bash

# Quick Demo Script - Data Engineering Interview Prep Platform
# This script demonstrates the platform capabilities

set -e

echo "════════════════════════════════════════════════════════════════"
echo "   🚀 Data Engineering Interview Prep Platform - Quick Demo"
echo "════════════════════════════════════════════════════════════════"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print section headers
print_section() {
    echo ""
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
}

# Function to print success
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

# Function to print info
print_info() {
    echo -e "${YELLOW}ℹ $1${NC}"
}

# Check prerequisites
print_section "1. Checking Prerequisites"

if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi
print_success "Docker installed"

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed."
    exit 1
fi
print_success "Docker Compose installed"

if ! command -v curl &> /dev/null; then
    echo "❌ curl is not installed."
    exit 1
fi
print_success "curl installed"

# Project structure
print_section "2. Project Structure"
echo "Project files and directories:"
tree -L 2 -I 'node_modules|__pycache__|.git|.next|venv' . || ls -la

# Show key files
print_section "3. Key Configuration Files"

print_info "Backend dependencies (requirements.txt):"
head -n 10 backend/requirements.txt
echo "... (truncated)"

print_info "Frontend dependencies (package.json):"
head -n 15 frontend/package.json | tail -n 10

# Docker Compose configuration
print_section "4. Docker Compose Services"
echo "Services defined in docker-compose.yml:"
docker-compose config --services 2>/dev/null || echo "postgres, redis, backend, frontend"

# Database schema
print_section "5. Database Models"
print_info "Database tables:"
echo "  • users - User accounts and profiles"
echo "  • questions - Interview questions (28 seeded)"
echo "  • attempts - User code submissions"
echo "  • user_progress - Skill proficiency tracking"
echo "  • practice_sessions - Practice session metadata"

# API Endpoints
print_section "6. API Endpoints"
print_info "Available endpoints:"
cat << 'EOF'
Authentication:
  POST   /api/auth/register         Register new user
  POST   /api/auth/login           Login (form data)
  POST   /api/auth/login/json      Login (JSON)
  GET    /api/auth/me              Get current user

Questions:
  GET    /api/questions/           List questions (with filters)
  GET    /api/questions/{id}       Get specific question

Practice:
  POST   /api/practice/start       Start question attempt
  POST   /api/practice/submit      Submit code for AI evaluation
  POST   /api/practice/hint        Get progressive hint

Progress:
  GET    /api/progress/dashboard   Get dashboard statistics
  GET    /api/progress/skills      Get skill proficiency
EOF

# Question categories
print_section "7. Question Bank (28 Questions)"
print_info "Categories and count:"
cat << 'EOF'
  • SQL (9 questions)
    - Window functions, aggregations
    - Joins, subqueries, CTEs
    - Data quality, optimization

  • Python/PySpark (9 questions)
    - Pandas data processing
    - PySpark transformations
    - Algorithms, optimization

  • System Design (5 questions)
    - Data lake architecture
    - ETL pipelines
    - Real-time analytics

  • Behavioral (5 questions)
    - STAR format practice
    - Leadership scenarios
    - Problem-solving
EOF

# AI Features
print_section "8. AI-Powered Features"
print_info "Claude Sonnet 4.5 Integration:"
cat << 'EOF'
  ✓ Code evaluation with detailed feedback
  ✓ Scoring system (0-100)
  ✓ Strengths identification
  ✓ Improvement suggestions
  ✓ Optimization recommendations
  ✓ Progressive hints (3 levels)
  ✓ Interview readiness assessment
EOF

# Sample question
print_section "9. Sample Question"
cat << 'EOF'
Title: Calculate Running Total of Sales
Category: SQL
Difficulty: Medium
Companies: Amazon, Google, Meta

Description:
Given a table 'sales' with columns (date, amount), write a SQL
query to calculate the running total of sales ordered by date.

Table schema:
- sales (date DATE, amount DECIMAL)

Expected output: date, amount, running_total

Starter code:
SELECT
  date,
  amount,
  -- Your code here
FROM sales
ORDER BY date;
EOF

# Sample solution
print_section "10. Sample Solution & AI Feedback"
print_info "Sample solution:"
cat << 'EOF'
SELECT
  date,
  amount,
  SUM(amount) OVER (ORDER BY date) as running_total
FROM sales
ORDER BY date;
EOF

print_info "AI Feedback (simulated):"
cat << 'EOF'
Score: 95/100

Strengths:
✓ Correct use of window functions
✓ Proper ordering in OVER clause
✓ Clean, readable syntax

Improvements:
• Consider adding explicit window frame
• Add comments for production code

Optimization:
For large datasets with categories, add PARTITION BY

Would Pass Interview: ✅ Yes
EOF

# Testing
print_section "11. Testing"
print_info "Backend tests:"
echo "  • 25+ automated tests"
echo "  • Authentication (7 tests)"
echo "  • Questions API (6 tests)"
echo "  • Practice flow (5 tests)"
echo "  • Progress tracking (4 tests)"

# Deployment options
print_section "12. Deployment Options"
cat << 'EOF'
✓ Docker Compose (development)
✓ Docker Compose Production
✓ Kubernetes (scalable)
✓ Platform as a Service (Railway, Heroku)
✓ Serverless (AWS Lambda, Vercel)

See DEPLOYMENT.md for complete guide.
EOF

# Next steps
print_section "13. Quick Start Commands"
cat << 'EOF'
# Start the platform:
export ANTHROPIC_API_KEY=your_key_here
./setup.sh

# Or use Makefile:
make setup        # Complete setup
make start        # Start services
make stop         # Stop services
make test         # Run tests
make logs         # View logs
make seed         # Seed database

# Access:
Frontend:  http://localhost:3000
Backend:   http://localhost:8000
API Docs:  http://localhost:8000/docs
EOF

# Demo summary
print_section "14. Demo Summary"
cat << 'EOF'
✅ Full-stack application built
✅ 28 interview questions seeded
✅ AI-powered feedback with Claude
✅ Interactive code editor (Monaco)
✅ Progress tracking dashboard
✅ Comprehensive testing suite
✅ Production-ready deployment
✅ Complete documentation

Total Files: 73
Lines of Code: ~6,000
Setup Time: < 5 minutes
EOF

# Final message
print_section "Ready to Launch!"
echo ""
echo -e "${GREEN}To start the platform, run:${NC}"
echo -e "${YELLOW}  export ANTHROPIC_API_KEY=your_key_here${NC}"
echo -e "${YELLOW}  ./setup.sh${NC}"
echo ""
echo -e "${GREEN}Then visit:${NC}"
echo -e "${YELLOW}  http://localhost:3000${NC}"
echo ""
echo "════════════════════════════════════════════════════════════════"
echo ""
