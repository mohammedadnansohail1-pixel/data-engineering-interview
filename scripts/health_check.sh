#!/bin/bash

# Health Monitoring Script
# Monitors the health and status of all services

set -e

API_URL="${API_URL:-http://localhost:8000}"
FRONTEND_URL="${FRONTEND_URL:-http://localhost:3000}"
DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-5432}"
REDIS_HOST="${REDIS_HOST:-localhost}"
REDIS_PORT="${REDIS_PORT:-6379}"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo "════════════════════════════════════════════════════════════════"
echo "  Health Monitoring - Interview Prep Platform"
echo "  $(date '+%Y-%m-%d %H:%M:%S')"
echo "════════════════════════════════════════════════════════════════"
echo ""

# Check service health
check_service() {
    local service_name=$1
    local check_command=$2

    echo -n "Checking $service_name... "

    if eval "$check_command" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Healthy${NC}"
        return 0
    else
        echo -e "${RED}✗ Unhealthy${NC}"
        return 1
    fi
}

# Check HTTP endpoint
check_http() {
    local service_name=$1
    local url=$2

    echo -n "Checking $service_name... "

    http_code=$(curl -s -o /dev/null -w "%{http_code}" "$url" 2>/dev/null || echo "000")

    if [ "$http_code" -ge 200 ] && [ "$http_code" -lt 400 ]; then
        echo -e "${GREEN}✓ Healthy (HTTP $http_code)${NC}"
        return 0
    else
        echo -e "${RED}✗ Unhealthy (HTTP $http_code)${NC}"
        return 1
    fi
}

# Initialize counters
total_checks=0
passed_checks=0

# Docker Services
echo -e "${BLUE}Docker Services:${NC}"
if command -v docker &> /dev/null; then
    check_service "PostgreSQL Container" "docker ps | grep -q de-interview-postgres"
    total_checks=$((total_checks + 1))
    [ $? -eq 0 ] && passed_checks=$((passed_checks + 1))

    check_service "Redis Container" "docker ps | grep -q de-interview-redis"
    total_checks=$((total_checks + 1))
    [ $? -eq 0 ] && passed_checks=$((passed_checks + 1))

    check_service "Backend Container" "docker ps | grep -q de-interview-backend"
    total_checks=$((total_checks + 1))
    [ $? -eq 0 ] && passed_checks=$((passed_checks + 1))

    check_service "Frontend Container" "docker ps | grep -q de-interview-frontend"
    total_checks=$((total_checks + 1))
    [ $? -eq 0 ] && passed_checks=$((passed_checks + 1))
else
    echo -e "${YELLOW}Docker not available, skipping container checks${NC}"
fi

echo ""

# Network Services
echo -e "${BLUE}Network Services:${NC}"

# PostgreSQL
echo -n "Checking PostgreSQL... "
if command -v pg_isready &> /dev/null; then
    if pg_isready -h $DB_HOST -p $DB_PORT > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Accepting connections${NC}"
        passed_checks=$((passed_checks + 1))
    else
        echo -e "${RED}✗ Not accepting connections${NC}"
    fi
    total_checks=$((total_checks + 1))
else
    if nc -z $DB_HOST $DB_PORT 2>/dev/null; then
        echo -e "${GREEN}✓ Port open${NC}"
        passed_checks=$((passed_checks + 1))
    else
        echo -e "${RED}✗ Port closed${NC}"
    fi
    total_checks=$((total_checks + 1))
fi

# Redis
check_service "Redis" "nc -z $REDIS_HOST $REDIS_PORT"
total_checks=$((total_checks + 1))
[ $? -eq 0 ] && passed_checks=$((passed_checks + 1))

echo ""

# HTTP Endpoints
echo -e "${BLUE}HTTP Endpoints:${NC}"

check_http "Backend Health" "$API_URL/health"
total_checks=$((total_checks + 1))
[ $? -eq 0 ] && passed_checks=$((passed_checks + 1))

check_http "Backend API" "$API_URL/api/questions/"
total_checks=$((total_checks + 1))
[ $? -eq 0 ] && passed_checks=$((passed_checks + 1))

check_http "Frontend" "$FRONTEND_URL"
total_checks=$((total_checks + 1))
[ $? -eq 0 ] && passed_checks=$((passed_checks + 1))

echo ""

# API Response Time
echo -e "${BLUE}Performance:${NC}"
echo -n "Backend API response time... "
response_time=$(curl -s -o /dev/null -w "%{time_total}" "$API_URL/health" 2>/dev/null || echo "N/A")
if [ "$response_time" != "N/A" ]; then
    echo "${response_time}s"

    # Check if response time is acceptable (< 2 seconds)
    if (( $(echo "$response_time < 2" | bc -l 2>/dev/null || echo 0) )); then
        echo -e "${GREEN}✓ Response time acceptable${NC}"
    else
        echo -e "${YELLOW}⚠ Response time high${NC}"
    fi
else
    echo "N/A"
fi

echo ""

# Database Statistics
if command -v docker &> /dev/null; then
    echo -e "${BLUE}Database Statistics:${NC}"

    # Get question count
    question_count=$(docker exec de-interview-postgres psql -U deprep -d interview_prep -t -c "SELECT COUNT(*) FROM questions;" 2>/dev/null | tr -d ' ' || echo "N/A")
    echo "Questions in database: $question_count"

    # Get user count
    user_count=$(docker exec de-interview-postgres psql -U deprep -d interview_prep -t -c "SELECT COUNT(*) FROM users;" 2>/dev/null | tr -d ' ' || echo "N/A")
    echo "Registered users: $user_count"

    # Get attempt count
    attempt_count=$(docker exec de-interview-postgres psql -U deprep -d interview_prep -t -c "SELECT COUNT(*) FROM attempts;" 2>/dev/null | tr -d ' ' || echo "N/A")
    echo "Total attempts: $attempt_count"
fi

echo ""

# Resource Usage
if command -v docker &> /dev/null; then
    echo -e "${BLUE}Resource Usage:${NC}"
    docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}" | grep de-interview || echo "No containers found"
fi

echo ""

# Summary
echo "════════════════════════════════════════════════════════════════"
echo "Health Check Summary"
echo "════════════════════════════════════════════════════════════════"
echo "Checks passed: $passed_checks/$total_checks"

if [ $passed_checks -eq $total_checks ]; then
    echo -e "${GREEN}Status: All systems operational ✓${NC}"
    exit 0
elif [ $passed_checks -gt $((total_checks / 2)) ]; then
    echo -e "${YELLOW}Status: Some issues detected ⚠${NC}"
    exit 1
else
    echo -e "${RED}Status: Critical issues detected ✗${NC}"
    exit 2
fi
