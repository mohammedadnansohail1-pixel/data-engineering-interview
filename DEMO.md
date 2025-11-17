# Live Demo Guide: Data Engineering Interview Prep Platform

This guide walks you through a complete demo of the platform, from setup to getting AI feedback.

## 🚀 Step 1: Starting the Application

### Quick Start
```bash
# Navigate to the project
cd data-engineering-interview

# Set your Anthropic API key
export ANTHROPIC_API_KEY=sk-ant-api03-your-key-here

# Run the automated setup
./setup.sh
```

**What happens:**
```
🚀 Setting up Data Engineering Interview Prep Platform...
✅ Docker is installed
✅ Docker Compose is installed
📝 Creating backend/.env file...
📝 Creating frontend/.env.local file...
🐳 Starting Docker containers...
⏳ Waiting for services to be ready...
✅ PostgreSQL is ready!
🌱 Seeding database with interview questions...
Successfully seeded 28 questions!

✅ Setup complete!

🎉 Your Data Engineering Interview Prep Platform is ready!

📍 Access the application:
   Frontend: http://localhost:3000
   Backend API: http://localhost:8000
   API Docs: http://localhost:8000/docs
```

---

## 📱 Step 2: Register an Account

Navigate to http://localhost:3000

**What you see:**
```
┌────────────────────────────────────────────┐
│                                            │
│    Data Engineering Interview Prep         │
│         Sign in to your account            │
│                                            │
│    ┌────────────────────────────────┐     │
│    │ Email address                  │     │
│    │ [email input field]            │     │
│    ├────────────────────────────────┤     │
│    │ Password                       │     │
│    │ [password input field]         │     │
│    └────────────────────────────────┘     │
│                                            │
│         [Sign in button]                   │
│                                            │
│    Don't have an account? Sign up          │
│                                            │
└────────────────────────────────────────────┘
```

Click **"Sign up"** and fill in the form:

```
┌────────────────────────────────────────────┐
│         Create your account                │
│  Start preparing for data engineering      │
│           interviews                        │
│                                            │
│    Email address                           │
│    ┌────────────────────────────────┐     │
│    │ demo@example.com              │     │
│    └────────────────────────────────┘     │
│                                            │
│    Password                                │
│    ┌────────────────────────────────┐     │
│    │ ••••••••                      │     │
│    └────────────────────────────────┘     │
│                                            │
│    Full name                               │
│    ┌────────────────────────────────┐     │
│    │ Demo User                     │     │
│    └────────────────────────────────┘     │
│                                            │
│    Experience level                        │
│    ┌────────────────────────────────┐     │
│    │ Mid (3-5 years)        ▼      │     │
│    └────────────────────────────────┘     │
│                                            │
│    Target role                             │
│    ┌────────────────────────────────┐     │
│    │ Senior Data Engineer          │     │
│    └────────────────────────────────┘     │
│                                            │
│         [Create account]                   │
│                                            │
│    Already have an account? Sign in        │
└────────────────────────────────────────────┘
```

**API Request (automatically sent):**
```bash
POST http://localhost:8000/api/auth/register
Content-Type: application/json

{
  "email": "demo@example.com",
  "password": "securepassword123",
  "full_name": "Demo User",
  "experience_level": "mid",
  "target_role": "Senior Data Engineer"
}
```

**Response:**
```json
{
  "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "email": "demo@example.com",
  "full_name": "Demo User",
  "experience_level": "mid",
  "target_role": "Senior Data Engineer",
  "created_at": "2024-01-17T10:30:00Z"
}
```

---

## 📊 Step 3: View Dashboard

After login, you're redirected to the dashboard:

```
┌────────────────────────────────────────────────────────────────┐
│  DE Interview Prep    Dashboard    Questions         [Logout]  │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  Dashboard                                                     │
│                                                                │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐     │
│  │   📝          │  │   🔥          │  │   ⭐          │     │
│  │ Questions     │  │ Current       │  │ Average       │     │
│  │ Completed     │  │ Streak        │  │ Score         │     │
│  │               │  │               │  │               │     │
│  │     0         │  │   0 days      │  │     0         │     │
│  └───────────────┘  └───────────────┘  └───────────────┘     │
│                                                                │
│  Recent Activity                                               │
│  ┌──────────────────────────────────────────────────────┐     │
│  │ No recent activity. Start practicing to see          │     │
│  │ your progress here!                                   │     │
│  └──────────────────────────────────────────────────────┘     │
│                                                                │
│  Quick Actions                                                 │
│  ┌──────────────────────┐  ┌──────────────────────┐          │
│  │ Browse Questions     │  │ Practice Easy        │          │
│  │                      │  │ Questions            │          │
│  └──────────────────────┘  └──────────────────────┘          │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

---

## 🔍 Step 4: Browse Questions

Click **"Browse Questions"** or **"Questions"** in the navbar:

```
┌────────────────────────────────────────────────────────────────┐
│  DE Interview Prep    Dashboard    Questions         [Logout]  │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  Practice Questions                                            │
│                                                                │
│  ┌──────────────────────────────────────────────────────┐     │
│  │ Category          Difficulty         Search          │     │
│  │ [All Categories▼] [All Difficulties▼] [Search...]   │     │
│  └──────────────────────────────────────────────────────┘     │
│                                                                │
│  ┌──────────────────────────────────────────────────────┐     │
│  │ 🗄️  Calculate Running Total of Sales                 │     │
│  │                                                       │     │
│  │ Given a table 'sales' with columns (date, amount),   │     │
│  │ write a SQL query to calculate the running total...  │     │
│  │                                                       │     │
│  │ [medium] [sql]  Amazon, Google, Meta      [Start]    │     │
│  └──────────────────────────────────────────────────────┘     │
│                                                                │
│  ┌──────────────────────────────────────────────────────┐     │
│  │ 🗄️  Find Duplicate Records                            │     │
│  │                                                       │     │
│  │ Write a SQL query to find duplicate email            │     │
│  │ addresses in a 'users' table...                      │     │
│  │                                                       │     │
│  │ [easy] [sql]  Uber, Airbnb                [Start]    │     │
│  └──────────────────────────────────────────────────────┘     │
│                                                                │
│  ┌──────────────────────────────────────────────────────┐     │
│  │ 🐍  Process CSV with Pandas                           │     │
│  │                                                       │     │
│  │ Write a Python function to read a CSV file, filter   │     │
│  │ rows where 'age' > 25, and calculate the average...  │     │
│  │                                                       │     │
│  │ [easy] [python]  Netflix, Spotify         [Start]    │     │
│  └──────────────────────────────────────────────────────┘     │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

**Try filtering:**
- Select **Category: SQL**
- Select **Difficulty: Medium**
- Click search

---

## 💻 Step 5: Practice a Question

Click **[Start]** on "Calculate Running Total of Sales":

```
┌────────────────────────────────────────────────────────────────────────────────────┐
│  DE Interview Prep                                                      [Logout]   │
├──────────────────────────────────┬─────────────────────────────────────────────────┤
│                                  │                                                 │
│  ← Back to Questions             │  Code Editor                                    │
│                                  │  [Get Hint (0/3)]  [Submit Code]                │
│  Calculate Running Total         ├─────────────────────────────────────────────────┤
│  [medium] [sql]                  │                                                 │
│                                  │  1  SELECT                                      │
│  Description                     │  2    date,                                     │
│                                  │  3    amount,                                   │
│  Given a table 'sales' with      │  4    -- Your code here                         │
│  columns (date, amount), write   │  5  FROM sales                                  │
│  a SQL query to calculate the    │  6  ORDER BY date;                              │
│  running total of sales          │  7                                              │
│  ordered by date.                │  8                                              │
│                                  │  9                                              │
│  Table schema:                   │ 10                                              │
│  - sales (date DATE, amount      │                                                 │
│    DECIMAL)                      │                                                 │
│                                  │                                                 │
│  Expected output columns:        │  ← Monaco Editor (VS Code)                      │
│  date, amount, running_total     │  ← Syntax highlighting                          │
│                                  │  ← Auto-completion                              │
│                                  │                                                 │
│                                  │                                                 │
│                                  │                                                 │
│                                  │                                                 │
│                                  │                                                 │
└──────────────────────────────────┴─────────────────────────────────────────────────┘
```

---

## ✍️ Step 6: Write Your Solution

Let's write the solution:

```sql
SELECT
  date,
  amount,
  SUM(amount) OVER (ORDER BY date) as running_total
FROM sales
ORDER BY date;
```

**Editor now shows:**
```
┌─────────────────────────────────────────────────────────────────┐
│  Code Editor                    [Get Hint (0/3)]  [Submit Code] │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1  SELECT                                                      │
│  2    date,                                                     │
│  3    amount,                                                   │
│  4    SUM(amount) OVER (ORDER BY date) as running_total        │
│  5  FROM sales                                                  │
│  6  ORDER BY date;                                              │
│  7                                                              │
│                                                                 │
│                   [Cursor blinking]                             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🎯 Step 7: Submit Code & Get AI Feedback

Click **[Submit Code]**

**Loading state:**
```
[Submitting... 🔄]
```

**API Request:**
```bash
POST http://localhost:8000/api/practice/submit
Content-Type: application/json
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

{
  "question_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "code": "SELECT \n  date,\n  amount,\n  SUM(amount) OVER (ORDER BY date) as running_total\nFROM sales\nORDER BY date;",
  "language": "sql"
}
```

**After ~3 seconds, feedback appears:**

```
┌──────────────────────────────────┐
│  Test Results                    │
├──────────────────────────────────┤
│  Passed: 1                       │
│  Failed: 0                       │
│  Total: 1                        │
└──────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│  AI Feedback (Score: 95/100)                                     │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Strengths:                                                      │
│  ✓ Correct use of window functions with SUM() OVER()            │
│  ✓ Proper ordering in the window function                       │
│  ✓ Clean, readable SQL syntax                                   │
│  ✓ Handles edge cases correctly                                 │
│                                                                  │
│  Areas for Improvement:                                          │
│  • Consider adding ROWS BETWEEN UNBOUNDED PRECEDING AND          │
│    CURRENT ROW for explicit window frame specification          │
│  • Could add comments for clarity in production code            │
│                                                                  │
│  Optimization Suggestion:                                        │
│  For very large datasets, consider partitioning if you need      │
│  running totals per category. You could add PARTITION BY         │
│  category to the OVER clause.                                   │
│                                                                  │
│  Would Pass Interview: ✅ Yes                                    │
│  This solution demonstrates strong understanding of window       │
│  functions and would be acceptable in most technical interviews. │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 💡 Step 8: Using Hints

Let's try a harder question. Click on "Pivot Table with CASE Statement" (Hard difficulty)

**Initial code:**
```sql
SELECT
  product_category,
  -- Your code here
FROM sales
GROUP BY product_category
```

Click **[Get Hint (0/3)]**

**Hint 1 appears:**
```
┌──────────────────────────────────────────────────────────────────┐
│  Hint 1/3                                                        │
├──────────────────────────────────────────────────────────────────┤
│  Think about how to transform rows into columns. You'll need to │
│  use CASE statements to check the quarter of each sale_date     │
│  and sum the amounts conditionally. Consider using EXTRACT()    │
│  or DATE_PART() to get the quarter from the date.               │
└──────────────────────────────────────────────────────────────────┘
```

Still stuck? Click **[Get Hint (1/3)]**

**Hint 2 appears:**
```
┌──────────────────────────────────────────────────────────────────┐
│  Hint 2/3                                                        │
├──────────────────────────────────────────────────────────────────┤
│  Here's the structure you need:                                 │
│                                                                  │
│  SELECT                                                          │
│    product_category,                                             │
│    SUM(CASE WHEN EXTRACT(QUARTER FROM sale_date) = 1            │
│        THEN amount ELSE 0 END) as Q1_sales,                     │
│    -- Repeat for Q2, Q3, Q4                                     │
│  FROM sales                                                      │
│  GROUP BY product_category                                       │
│                                                                  │
│  Now complete the pattern for quarters 2, 3, and 4.             │
└──────────────────────────────────────────────────────────────────┘
```

---

## 📈 Step 9: View Updated Dashboard

After completing a few questions, navigate back to Dashboard:

```
┌────────────────────────────────────────────────────────────────┐
│  DE Interview Prep    Dashboard    Questions         [Logout]  │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  Dashboard                                                     │
│                                                                │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐     │
│  │   📝          │  │   🔥          │  │   ⭐          │     │
│  │ Questions     │  │ Current       │  │ Average       │     │
│  │ Completed     │  │ Streak        │  │ Score         │     │
│  │               │  │               │  │               │     │
│  │     3         │  │   0 days      │  │    88         │     │
│  └───────────────┘  └───────────────┘  └───────────────┘     │
│                                                                │
│  Recent Activity                                               │
│  ┌──────────────────────────────────────────────────────┐     │
│  │ Question ID: a1b2c3d4...    Jan 17, 2024             │     │
│  │ [completed] Score: 95/100                            │     │
│  ├──────────────────────────────────────────────────────┤     │
│  │ Question ID: b2c3d4e5...    Jan 17, 2024             │     │
│  │ [completed] Score: 85/100                            │     │
│  ├──────────────────────────────────────────────────────┤     │
│  │ Question ID: c3d4e5f6...    Jan 17, 2024             │     │
│  │ [completed] Score: 85/100                            │     │
│  └──────────────────────────────────────────────────────┘     │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

---

## 🔧 Step 10: Explore API Documentation

Navigate to http://localhost:8000/docs

**Swagger UI shows:**
```
┌────────────────────────────────────────────────────────────────┐
│  Data Engineering Interview Prep - API Documentation           │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  auth                                                          │
│    POST   /api/auth/register     Register a new user          │
│    POST   /api/auth/login        Login and get access token   │
│    POST   /api/auth/login/json   Login with JSON payload      │
│    GET    /api/auth/me           Get current user             │
│                                                                │
│  questions                                                     │
│    GET    /api/questions/        List questions with filters  │
│    GET    /api/questions/{id}    Get specific question        │
│                                                                │
│  practice                                                      │
│    POST   /api/practice/start    Start question attempt       │
│    POST   /api/practice/submit   Submit code for evaluation   │
│    POST   /api/practice/hint     Get contextual hint          │
│                                                                │
│  progress                                                      │
│    GET    /api/progress/dashboard Get dashboard stats         │
│    GET    /api/progress/skills    Get skill proficiency       │
│                                                                │
│  Schemas                                                       │
│    UserCreate, QuestionResponse, AttemptResponse, ...         │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

You can test any endpoint directly from the Swagger UI!

---

## 🧪 Step 11: Testing the API Directly

**Example: List SQL questions**
```bash
curl -X GET "http://localhost:8000/api/questions/?category=sql" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

**Response:**
```json
[
  {
    "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "title": "Calculate Running Total of Sales",
    "description": "Given a table 'sales' with columns...",
    "category": "sql",
    "difficulty": "medium",
    "question_type": "coding",
    "starter_code": "SELECT ...",
    "companies": ["Amazon", "Google", "Meta"],
    "tags": ["window-functions", "sql", "aggregation"],
    "created_at": "2024-01-17T10:00:00Z"
  },
  {
    "id": "b2c3d4e5-f6g7-8901-bcde-fg2345678901",
    "title": "Find Duplicate Records",
    "description": "Write a SQL query to find...",
    "category": "sql",
    "difficulty": "easy",
    "question_type": "coding",
    "companies": ["Uber", "Airbnb"],
    "tags": ["sql", "grouping", "duplicates"],
    "created_at": "2024-01-17T10:01:00Z"
  }
]
```

---

## 📊 Backend Logs

View real-time logs:
```bash
docker-compose logs -f backend
```

**Sample output:**
```
backend_1  | INFO:     Started server process [1]
backend_1  | INFO:     Waiting for application startup.
backend_1  | INFO:     Application startup complete.
backend_1  | INFO:     127.0.0.1:52134 - "POST /api/auth/register HTTP/1.1" 201 Created
backend_1  | INFO:     127.0.0.1:52135 - "POST /api/auth/login/json HTTP/1.1" 200 OK
backend_1  | INFO:     127.0.0.1:52136 - "GET /api/questions/ HTTP/1.1" 200 OK
backend_1  | INFO:     127.0.0.1:52137 - "GET /api/questions/a1b2c3d4... HTTP/1.1" 200 OK
backend_1  | INFO:     Claude API: Evaluating code submission
backend_1  | INFO:     127.0.0.1:52138 - "POST /api/practice/submit HTTP/1.1" 200 OK
```

---

## 🎭 Demo Scenarios

### Scenario 1: Complete Beginner
1. Register → Dashboard shows 0 progress
2. Browse Easy questions
3. Start with "Find Duplicate Records" (SQL)
4. Use all 3 hints
5. Submit solution
6. Get feedback and learn

### Scenario 2: Experienced Engineer
1. Register as Senior level
2. Filter for Hard questions
3. Attempt "Pivot Table with CASE"
4. Submit without hints
5. Get high score (90+)
6. Move to System Design questions

### Scenario 3: Interview Prep
1. Practice 5 SQL questions
2. Practice 5 Python questions
3. Review dashboard analytics
4. Identify weak areas
5. Focus practice on those areas
6. Track improvement over time

---

## 🔍 Monitoring & Debugging

### Check Service Health
```bash
# Check all services are running
docker-compose ps

# Expected output:
NAME                    STATUS
de-interview-postgres   Up (healthy)
de-interview-redis      Up (healthy)
de-interview-backend    Up
de-interview-frontend   Up
```

### Access Database
```bash
docker-compose exec postgres psql -U deprep -d interview_prep

# Run queries
SELECT COUNT(*) FROM questions;
SELECT COUNT(*) FROM users;
SELECT * FROM attempts ORDER BY created_at DESC LIMIT 5;
```

### View All Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
```

---

## 🎬 Complete User Journey

```
1. Setup (1 min)
   ./setup.sh

2. Register (30 sec)
   http://localhost:3000
   → Sign up

3. Browse (1 min)
   → Questions tab
   → Filter by SQL
   → Select "Calculate Running Total"

4. Practice (5 min)
   → Write solution
   → Submit code
   → Review AI feedback

5. Learn (2 min)
   → Read improvements
   → Try optimization
   → Resubmit

6. Progress (1 min)
   → View dashboard
   → See score: 95/100
   → Continue practicing

Total: ~10 minutes for complete cycle
```

---

## 🎯 Key Features Demonstrated

✅ **Authentication** - Secure JWT-based login
✅ **28 Questions** - SQL, Python, System Design, Behavioral
✅ **AI Feedback** - Claude Sonnet 4.5 evaluation
✅ **Code Editor** - Monaco (VS Code) editor
✅ **Hints System** - Progressive 3-level hints
✅ **Progress Tracking** - Dashboard with stats
✅ **Filtering** - By category, difficulty, search
✅ **API Documentation** - Interactive Swagger UI

---

## 🚀 Next Steps After Demo

1. **Add more questions** - Edit `backend/app/seed_questions.py`
2. **Customize AI prompts** - Modify `backend/app/services/ai_service.py`
3. **Deploy to production** - Follow `DEPLOYMENT.md`
4. **Run tests** - `make test`
5. **Contribute** - See `CONTRIBUTING.md`

---

**The platform is ready to help you ace your data engineering interviews!** 🎉
