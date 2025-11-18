.PHONY: help setup start stop restart logs seed test clean api-examples health backup

help:
	@echo "Data Engineering Interview Prep Platform - Makefile Commands"
	@echo ""
	@echo "Available commands:"
	@echo "  make setup         - Initial setup (create env files and start services)"
	@echo "  make start         - Start all services"
	@echo "  make stop          - Stop all services"
	@echo "  make restart       - Restart all services"
	@echo "  make logs          - View logs from all services"
	@echo "  make seed          - Seed database with interview questions"
	@echo "  make test          - Run backend tests"
	@echo "  make test-watch    - Run tests in watch mode"
	@echo "  make clean         - Clean up containers and volumes"
	@echo "  make shell         - Open backend shell"
	@echo "  make db-shell      - Open database shell"
	@echo ""
	@echo "Utility commands:"
	@echo "  make api-examples  - Run API example requests"
	@echo "  make health        - Check health of all services"
	@echo "  make backup        - Backup database"
	@echo "  make backup-list   - List available backups"
	@echo ""

setup:
	@echo "🚀 Setting up Data Engineering Interview Prep Platform..."
	@bash setup.sh || cmd /c setup.bat

start:
	@echo "Starting services..."
	docker-compose up -d
	@echo "✅ Services started!"
	@echo "Frontend: http://localhost:3000"
	@echo "Backend: http://localhost:8000"
	@echo "API Docs: http://localhost:8000/docs"

stop:
	@echo "Stopping services..."
	docker-compose down
	@echo "✅ Services stopped"

restart: stop start

logs:
	docker-compose logs -f

seed:
	@echo "🌱 Seeding database..."
	docker-compose exec backend python app/seed_questions.py
	@echo "✅ Database seeded"

test:
	@echo "Running tests..."
	docker-compose exec backend pytest tests/ -v
	@echo "✅ Tests complete"

test-watch:
	@echo "Running tests in watch mode..."
	docker-compose exec backend pytest tests/ -v --ff -x

clean:
	@echo "Cleaning up..."
	docker-compose down -v
	rm -f backend/test.db
	@echo "✅ Cleanup complete"

shell:
	docker-compose exec backend /bin/bash

db-shell:
	docker-compose exec postgres psql -U deprep -d interview_prep

status:
	docker-compose ps

build:
	docker-compose build

rebuild: clean
	docker-compose build --no-cache
	@echo "✅ Rebuild complete"

# Utility commands
api-examples:
	@echo "Running API examples..."
	@bash scripts/api_examples.sh

health:
	@bash scripts/health_check.sh

backup:
	@bash scripts/backup_db.sh backup

backup-restore:
	@bash scripts/backup_db.sh restore

backup-list:
	@bash scripts/backup_db.sh list

backup-clean:
	@bash scripts/backup_db.sh clean
