# Documentation Index

Complete documentation for the AI-Powered Data Engineering Interview Prep Platform.

## 📚 Quick Navigation

### Getting Started
- **[README.md](README.md)** - Main project documentation and overview
- **[QUICKSTART.md](QUICKSTART.md)** - 5-minute setup guide
- **[DEMO.md](DEMO.md)** - Complete walkthrough with UI mockups

### Development
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Contribution guidelines and standards
- **[CHANGELOG.md](CHANGELOG.md)** - Version history and release notes
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Complete project summary

### Deployment & Operations
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Production deployment guide
- **[docker-compose.yml](docker-compose.yml)** - Development configuration
- **[docker-compose.prod.yml](docker-compose.prod.yml)** - Production configuration

### API & Testing
- **API Documentation** - http://localhost:8000/docs (when running)
- **[postman_collection.json](postman_collection.json)** - Postman API collection
- **[backend/tests/](backend/tests/)** - Test suite

## 📖 Documentation by Topic

### Setup & Installation

1. **Quick Setup (5 minutes)**
   - Read: [QUICKSTART.md](QUICKSTART.md)
   - Run: `./setup.sh` or `make setup`

2. **Manual Setup**
   - Read: [README.md](README.md#getting-started)
   - Configure: `backend/.env` and `frontend/.env.local`
   - Start: `docker-compose up -d`

3. **Development Setup**
   - Backend: `cd backend && pip install -r requirements.txt`
   - Frontend: `cd frontend && npm install`
   - See: [CONTRIBUTING.md](CONTRIBUTING.md#development-workflow)

### Using the Platform

1. **Demo Walkthrough**
   - Full guide: [DEMO.md](DEMO.md)
   - Interactive demo: `./QUICK_DEMO.sh`
   - Video tutorial: *(coming soon)*

2. **User Guide**
   - Registration & Login
   - Browsing Questions
   - Code Submission
   - Getting AI Feedback
   - Progress Tracking
   - See: [DEMO.md](DEMO.md#user-journey-demo)

### API Documentation

1. **OpenAPI/Swagger**
   - Interactive docs: http://localhost:8000/docs
   - JSON spec: http://localhost:8000/openapi.json

2. **Postman Collection**
   - Import: [postman_collection.json](postman_collection.json)
   - Run examples: `make api-examples` or `scripts/api_examples.sh`

3. **API Endpoints**
   ```
   Authentication:
     POST   /api/auth/register
     POST   /api/auth/login/json
     GET    /api/auth/me

   Questions:
     GET    /api/questions/
     GET    /api/questions/{id}

   Practice:
     POST   /api/practice/start
     POST   /api/practice/submit
     POST   /api/practice/hint

   Progress:
     GET    /api/progress/dashboard
     GET    /api/progress/skills
   ```

### Development

1. **Code Structure**
   ```
   backend/
     app/
       api/endpoints/  - REST API endpoints
       core/          - Config, database, security
       models/        - SQLAlchemy models
       schemas/       - Pydantic schemas
       services/      - Business logic
     tests/           - Test suite

   frontend/
     app/             - Next.js pages
     components/      - React components
     hooks/           - Custom hooks
     lib/             - Utilities
   ```

2. **Running Tests**
   ```bash
   # Backend tests
   make test
   cd backend && pytest tests/ -v

   # Frontend tests
   cd frontend && npm test

   # With coverage
   pytest tests/ --cov=app
   ```

3. **Contributing**
   - Guidelines: [CONTRIBUTING.md](CONTRIBUTING.md)
   - Code style: Follow PEP 8 (Python), ESLint (TypeScript)
   - PR process: [CONTRIBUTING.md](CONTRIBUTING.md#pull-request-process)

### Deployment

1. **Docker Deployment**
   - Development: `docker-compose up`
   - Production: `docker-compose -f docker-compose.prod.yml up`
   - See: [DEPLOYMENT.md](DEPLOYMENT.md#docker-compose-simple-vps)

2. **Cloud Platforms**
   - AWS: [DEPLOYMENT.md](DEPLOYMENT.md#aws-elastic-beanstalk)
   - Heroku: [DEPLOYMENT.md](DEPLOYMENT.md#heroku)
   - Railway: [DEPLOYMENT.md](DEPLOYMENT.md#railway)
   - Kubernetes: [DEPLOYMENT.md](DEPLOYMENT.md#kubernetes-scalable)

3. **Production Checklist**
   - Security: [DEPLOYMENT.md](DEPLOYMENT.md#security-best-practices)
   - Monitoring: [DEPLOYMENT.md](DEPLOYMENT.md#monitoring--logging)
   - Backup: [DEPLOYMENT.md](DEPLOYMENT.md#backup--recovery)

### Maintenance & Operations

1. **Health Monitoring**
   ```bash
   make health                    # Run health checks
   scripts/health_check.sh        # Detailed health report
   ```

2. **Database Backups**
   ```bash
   make backup                    # Create backup
   make backup-list               # List backups
   scripts/backup_db.sh restore   # Restore from backup
   ```

3. **Logs & Debugging**
   ```bash
   make logs                      # View all logs
   docker-compose logs backend    # Backend logs only
   docker-compose logs -f         # Follow logs
   ```

### Utility Scripts

Located in `scripts/` directory:

1. **[api_examples.sh](scripts/api_examples.sh)**
   - Test all API endpoints
   - Example requests and responses
   - Run: `make api-examples`

2. **[health_check.sh](scripts/health_check.sh)**
   - Monitor service health
   - Check database connections
   - Resource usage
   - Run: `make health`

3. **[backup_db.sh](scripts/backup_db.sh)**
   - Database backup/restore
   - Backup management
   - Run: `make backup`

## 🎯 Common Tasks

### I want to...

**...start the platform**
→ Read [QUICKSTART.md](QUICKSTART.md) → Run `./setup.sh`

**...add new questions**
→ Edit `backend/app/seed_questions.py` → Run `make seed`

**...test the API**
→ Import [postman_collection.json](postman_collection.json) or run `make api-examples`

**...deploy to production**
→ Read [DEPLOYMENT.md](DEPLOYMENT.md) → Follow deployment guide for your platform

**...contribute**
→ Read [CONTRIBUTING.md](CONTRIBUTING.md) → Create PR

**...understand the architecture**
→ Read [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md#architecture)

**...run tests**
→ Run `make test`

**...monitor the platform**
→ Run `make health`

**...backup the database**
→ Run `make backup`

**...view API documentation**
→ Visit http://localhost:8000/docs

## 📊 Documentation Status

| Document | Status | Last Updated | Completeness |
|----------|--------|--------------|--------------|
| README.md | ✅ Complete | Jan 2024 | 100% |
| QUICKSTART.md | ✅ Complete | Jan 2024 | 100% |
| DEMO.md | ✅ Complete | Jan 2024 | 100% |
| DEPLOYMENT.md | ✅ Complete | Jan 2024 | 100% |
| CONTRIBUTING.md | ✅ Complete | Jan 2024 | 100% |
| CHANGELOG.md | ✅ Complete | Jan 2024 | 100% |
| PROJECT_SUMMARY.md | ✅ Complete | Jan 2024 | 100% |
| API Docs (OpenAPI) | ✅ Complete | Jan 2024 | 100% |
| Postman Collection | ✅ Complete | Jan 2024 | 100% |

## 🔗 External Resources

### Technologies Used
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Anthropic Claude API](https://docs.anthropic.com/)
- [Docker Documentation](https://docs.docker.com/)

### Learning Resources
- [Data Engineering Interview Guide](https://github.com/alexeygrigorev/data-science-interviews)
- [SQL Practice](https://www.sql-practice.com/)
- [Python for Data Engineering](https://realpython.com/)

## 💬 Getting Help

1. **Check Documentation**
   - Search this index for relevant topics
   - Read the specific guide

2. **Review Examples**
   - [DEMO.md](DEMO.md) for usage examples
   - [postman_collection.json](postman_collection.json) for API examples
   - `scripts/api_examples.sh` for command-line examples

3. **Run Diagnostics**
   - `make health` to check system status
   - `make logs` to view error logs
   - Review [DEPLOYMENT.md](DEPLOYMENT.md#troubleshooting)

4. **Community Support**
   - GitHub Issues: *(add your repo URL)*
   - Discussions: *(add discussions URL)*

## 📝 Contributing to Documentation

Documentation improvements are welcome!

1. Fix typos or unclear sections
2. Add missing examples
3. Update outdated information
4. Add new guides or tutorials

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

**Last Updated**: January 2024
**Version**: 1.0.0
**Maintained By**: Development Team
