#!/bin/bash

# API Examples - Test the platform endpoints
# This script demonstrates how to interact with the API

set -e

API_URL="${API_URL:-http://localhost:8000}"
TOKEN=""
USER_EMAIL="demo@example.com"
USER_PASSWORD="demopassword123"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo "════════════════════════════════════════════════════════════════"
echo "  API Examples - Data Engineering Interview Prep Platform"
echo "════════════════════════════════════════════════════════════════"
echo ""

# Function to print section
print_section() {
    echo ""
    echo -e "${BLUE}━━━ $1 ━━━${NC}"
    echo ""
}

# Function to make API request
api_request() {
    local method=$1
    local endpoint=$2
    local data=$3
    local description=$4

    echo -e "${YELLOW}➤ $description${NC}"
    echo "  Method: $method"
    echo "  Endpoint: $endpoint"

    if [ -n "$data" ]; then
        echo "  Data: $data"
    fi

    local auth_header=""
    if [ -n "$TOKEN" ]; then
        auth_header="-H 'Authorization: Bearer $TOKEN'"
    fi

    echo ""
    if [ "$method" = "GET" ]; then
        response=$(curl -s -w "\n%{http_code}" "$API_URL$endpoint" $auth_header)
    else
        response=$(curl -s -w "\n%{http_code}" -X "$method" \
            -H "Content-Type: application/json" \
            $auth_header \
            -d "$data" \
            "$API_URL$endpoint")
    fi

    http_code=$(echo "$response" | tail -n 1)
    body=$(echo "$response" | sed '$d')

    if [ "$http_code" -ge 200 ] && [ "$http_code" -lt 300 ]; then
        echo -e "${GREEN}✓ Success (HTTP $http_code)${NC}"
    else
        echo -e "${RED}✗ Error (HTTP $http_code)${NC}"
    fi

    echo "$body" | python3 -m json.tool 2>/dev/null || echo "$body"
    echo ""
}

# 1. Health Check
print_section "1. Health Check"
api_request "GET" "/health" "" "Check if the API is healthy"

# 2. Register User
print_section "2. Register New User"
register_data='{
  "email": "'"$USER_EMAIL"'",
  "password": "'"$USER_PASSWORD"'",
  "full_name": "Demo User",
  "experience_level": "mid",
  "target_role": "Senior Data Engineer"
}'
api_request "POST" "/api/auth/register" "$register_data" "Register a new user account"

# 3. Login
print_section "3. Login"
login_data='{
  "email": "'"$USER_EMAIL"'",
  "password": "'"$USER_PASSWORD"'"
}'
response=$(curl -s -X POST \
    -H "Content-Type: application/json" \
    -d "$login_data" \
    "$API_URL/api/auth/login/json")

TOKEN=$(echo "$response" | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])" 2>/dev/null || echo "")

if [ -n "$TOKEN" ]; then
    echo -e "${GREEN}✓ Login successful${NC}"
    echo "Token: ${TOKEN:0:20}..."
else
    echo -e "${RED}✗ Login failed${NC}"
    exit 1
fi

# 4. Get Current User
print_section "4. Get Current User Info"
api_request "GET" "/api/auth/me" "" "Fetch authenticated user information"

# 5. List All Questions
print_section "5. List All Questions"
api_request "GET" "/api/questions/" "" "Get all available questions"

# 6. Filter Questions by Category
print_section "6. Filter Questions (SQL only)"
api_request "GET" "/api/questions/?category=sql" "" "Get SQL questions"

# 7. Filter Questions by Difficulty
print_section "7. Filter Questions (Easy difficulty)"
api_request "GET" "/api/questions/?difficulty=easy" "" "Get easy questions"

# 8. Search Questions
print_section "8. Search Questions"
api_request "GET" "/api/questions/?search=pandas" "" "Search for 'pandas' in questions"

# 9. Get Specific Question
print_section "9. Get Specific Question"
# First get a question ID
question_id=$(curl -s -H "Authorization: Bearer $TOKEN" \
    "$API_URL/api/questions/" | \
    python3 -c "import sys, json; print(json.load(sys.stdin)[0]['id'])" 2>/dev/null || echo "")

if [ -n "$question_id" ]; then
    api_request "GET" "/api/questions/$question_id" "" "Get question details"

    # 10. Start Question Attempt
    print_section "10. Start Question Attempt"
    start_data='{
      "question_id": "'"$question_id"'",
      "status": "in_progress"
    }'
    api_request "POST" "/api/practice/start" "$start_data" "Start practicing a question"

    # 11. Submit Code
    print_section "11. Submit Code for Evaluation"
    submit_data='{
      "question_id": "'"$question_id"'",
      "code": "SELECT date, amount, SUM(amount) OVER (ORDER BY date) as running_total FROM sales ORDER BY date;",
      "language": "sql"
    }'
    api_request "POST" "/api/practice/submit" "$submit_data" "Submit SQL solution"

    # 12. Get Hint
    print_section "12. Get Hint"
    hint_data='{
      "question_id": "'"$question_id"'",
      "current_code": "SELECT * FROM sales",
      "hint_number": 1
    }'
    api_request "POST" "/api/practice/hint" "$hint_data" "Request first hint"
fi

# 13. Get Dashboard Stats
print_section "13. Get Dashboard Statistics"
api_request "GET" "/api/progress/dashboard" "" "Fetch user dashboard data"

# 14. Get Skills Progress
print_section "14. Get Skills Progress"
api_request "GET" "/api/progress/skills" "" "Get skill proficiency breakdown"

echo ""
echo "════════════════════════════════════════════════════════════════"
echo -e "${GREEN}API Examples Complete!${NC}"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "API Documentation: $API_URL/docs"
echo ""
