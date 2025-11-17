# Production Deployment Guide

This guide covers deploying the Data Engineering Interview Prep Platform to production.

## Table of Contents
- [Pre-deployment Checklist](#pre-deployment-checklist)
- [Environment Variables](#environment-variables)
- [Database Setup](#database-setup)
- [Deployment Options](#deployment-options)
- [Security Best Practices](#security-best-practices)
- [Monitoring & Logging](#monitoring--logging)
- [Backup & Recovery](#backup--recovery)

## Pre-deployment Checklist

Before deploying to production, ensure you have:

- [ ] Valid Anthropic API key with appropriate quota
- [ ] PostgreSQL database (managed service recommended)
- [ ] Redis instance (managed service recommended)
- [ ] Domain name and SSL certificate
- [ ] Secure secret keys generated
- [ ] Environment variables configured
- [ ] Database migrations tested
- [ ] Backup strategy in place
- [ ] Monitoring setup
- [ ] Load testing completed

## Environment Variables

### Backend (.env)

```bash
# Database (use managed PostgreSQL in production)
DATABASE_URL=postgresql://username:password@host:port/dbname

# Redis (use managed Redis in production)
REDIS_URL=redis://username:password@host:port

# Anthropic API
ANTHROPIC_API_KEY=sk-ant-api03-your-production-key

# Security
JWT_SECRET=generate-a-strong-random-secret-key-here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Environment
ENVIRONMENT=production

# CORS (update with your frontend domain)
BACKEND_CORS_ORIGINS=["https://yourdomain.com"]

# API settings
API_V1_STR=/api
PROJECT_NAME=Data Engineering Interview Prep
```

### Frontend (.env.production)

```bash
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
NEXT_PUBLIC_WS_URL=wss://api.yourdomain.com
```

## Database Setup

### 1. Provision Database

Use a managed PostgreSQL service:
- **AWS**: RDS for PostgreSQL
- **Google Cloud**: Cloud SQL
- **Azure**: Database for PostgreSQL
- **DigitalOcean**: Managed Databases

Recommended specifications:
- PostgreSQL 15+
- Minimum: 2 vCPUs, 4GB RAM
- Storage: 100GB SSD with auto-scaling

### 2. Initialize Schema

```bash
# Connect to your production database
export DATABASE_URL=postgresql://user:pass@host:port/dbname

# Create tables (already handled by SQLAlchemy)
python backend/app/main.py

# Seed initial questions
python backend/app/seed_questions.py
```

### 3. Database Security

- Enable SSL/TLS connections
- Restrict network access (VPC, firewall rules)
- Use strong passwords (32+ characters)
- Enable automated backups
- Set up point-in-time recovery
- Monitor slow queries

## Deployment Options

### Option 1: Docker Compose (Simple VPS)

For small-scale deployments on a single server:

```bash
# 1. Clone repository to server
git clone <repository-url>
cd data-engineering-interview

# 2. Configure environment
cp backend/.env.example backend/.env
# Edit .env with production values

# 3. Update docker-compose for production
# Use production docker-compose.prod.yml

# 4. Deploy
docker-compose -f docker-compose.prod.yml up -d

# 5. Set up SSL with Let's Encrypt (using Nginx/Caddy)
```

### Option 2: Kubernetes (Scalable)

For production-scale deployments:

```yaml
# Example Kubernetes deployment structure
apiVersion: apps/v1
kind: Deployment
metadata:
  name: interview-prep-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: interview-prep-backend
  template:
    metadata:
      labels:
        app: interview-prep-backend
    spec:
      containers:
      - name: backend
        image: your-registry/interview-prep-backend:latest
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: database-url
        # ... more config
```

### Option 3: Platform as a Service

#### Railway

1. Connect GitHub repository
2. Configure environment variables
3. Deploy automatically on push

#### Heroku

```bash
# Install Heroku CLI
heroku create interview-prep-app

# Set environment variables
heroku config:set ANTHROPIC_API_KEY=your_key
heroku config:set DATABASE_URL=postgres://...

# Deploy
git push heroku main

# Run migrations
heroku run python backend/app/seed_questions.py
```

#### AWS Elastic Beanstalk

```bash
# Install EB CLI
eb init

# Create environment
eb create production

# Deploy
eb deploy

# Configure scaling
eb scale 3
```

### Option 4: Serverless

Deploy backend as serverless functions:
- **AWS Lambda** + API Gateway
- **Google Cloud Functions**
- **Vercel** (for Next.js frontend)

## Security Best Practices

### 1. Environment Security

```bash
# Generate secure JWT secret
openssl rand -hex 64

# Never commit .env files
echo ".env" >> .gitignore
```

### 2. API Security

- Enable HTTPS only (redirect HTTP to HTTPS)
- Implement rate limiting
- Add request size limits
- Use CORS properly
- Enable CSRF protection
- Sanitize all inputs
- Use parameterized queries

### 3. Database Security

- Enable encryption at rest
- Use encrypted connections (SSL/TLS)
- Regular security patches
- Principle of least privilege
- Audit logging enabled

### 4. Application Security

```python
# backend/app/core/config.py
# Production settings

class Settings(BaseSettings):
    # ... existing settings

    # Security headers
    SECURE_HEADERS = True

    # Rate limiting
    RATE_LIMIT_PER_MINUTE = 60

    # Session settings
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "strict"
```

### 5. Dependency Security

```bash
# Regularly update dependencies
pip list --outdated
npm audit

# Use security scanners
pip-audit
npm audit fix

# Pin dependency versions
pip freeze > requirements.txt
```

## Monitoring & Logging

### Application Monitoring

Use monitoring services:
- **Datadog**: Full-stack monitoring
- **New Relic**: APM
- **Sentry**: Error tracking
- **Prometheus + Grafana**: Metrics

```python
# Example: Add Sentry to backend
import sentry_sdk

sentry_sdk.init(
    dsn="your-sentry-dsn",
    environment="production",
    traces_sample_rate=1.0,
)
```

### Logging

```python
# backend/app/core/logging_config.py
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('/var/log/app.log')
    ]
)
```

### Health Checks

```python
# backend/app/main.py
@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    try:
        # Check database
        db.execute("SELECT 1")

        # Check Redis
        # redis_client.ping()

        return {
            "status": "healthy",
            "database": "connected",
            "redis": "connected"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }, 503
```

## Performance Optimization

### Backend

```python
# Enable gzip compression
from fastapi.middleware.gzip import GZipMiddleware
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Database connection pooling
engine = create_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=40,
    pool_pre_ping=True
)

# Caching
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="cache")
```

### Frontend

```javascript
// next.config.mjs
const nextConfig = {
  compress: true,
  swcMinify: true,
  images: {
    formats: ['image/avif', 'image/webp'],
  },
  // Enable production optimizations
  productionBrowserSourceMaps: false,
};
```

### CDN Setup

Serve static assets via CDN:
- **Cloudflare**: Free tier available
- **AWS CloudFront**
- **Fastly**

## Backup & Recovery

### Database Backups

```bash
# Automated daily backups
0 2 * * * pg_dump -h localhost -U deprep interview_prep | gzip > /backups/db_$(date +%Y%m%d).sql.gz

# Retention: keep 30 days
find /backups -name "db_*.sql.gz" -mtime +30 -delete

# Test restore monthly
```

### Application Backups

- Code: Git repository (GitHub, GitLab)
- Environment configs: Secure vault (AWS Secrets Manager, HashiCorp Vault)
- User data: Database backups
- File uploads: S3/Cloud Storage with versioning

## Scaling Strategy

### Horizontal Scaling

```yaml
# docker-compose scale
docker-compose up -d --scale backend=3

# Kubernetes HPA
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: backend-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: interview-prep-backend
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

### Load Balancing

Use a load balancer:
- **Nginx**: Reverse proxy + load balancer
- **HAProxy**: High-performance load balancer
- **AWS ALB/ELB**: Managed load balancer
- **Google Cloud Load Balancing**

### Caching Strategy

```python
# Cache expensive operations
from functools import lru_cache
from datetime import timedelta

@lru_cache(maxsize=100)
def get_question_by_id(question_id: str):
    # Cached for performance
    pass

# Redis caching for API responses
@app.get("/api/questions/")
@cache(expire=300)  # 5 minutes
async def list_questions():
    pass
```

## Deployment Checklist

Pre-launch:
- [ ] All tests passing
- [ ] Security scan completed
- [ ] Performance testing done
- [ ] SSL certificate installed
- [ ] Environment variables set
- [ ] Database migrations applied
- [ ] Monitoring configured
- [ ] Backup system tested
- [ ] Load balancer configured
- [ ] CDN set up
- [ ] Error tracking enabled
- [ ] Documentation updated

Post-launch:
- [ ] Monitor error rates
- [ ] Check performance metrics
- [ ] Verify backups running
- [ ] Test user flows
- [ ] Monitor API usage
- [ ] Check database performance
- [ ] Review logs

## Rollback Plan

In case of deployment issues:

```bash
# 1. Revert to previous version
git checkout <previous-commit>

# 2. Redeploy
docker-compose down
docker-compose up -d --build

# 3. Restore database if needed
psql interview_prep < backup.sql

# 4. Verify health
curl https://api.yourdomain.com/health
```

## Cost Optimization

- Use auto-scaling to match demand
- Choose appropriate instance sizes
- Enable database query caching
- Use CDN for static assets
- Implement API response caching
- Monitor and optimize API usage
- Use spot instances for non-critical workloads
- Set up budget alerts

## Support & Maintenance

### Regular Tasks

- **Daily**: Monitor error rates and performance
- **Weekly**: Review security advisories, update dependencies
- **Monthly**: Test backups, review costs, capacity planning
- **Quarterly**: Security audit, load testing, disaster recovery drill

### Updates

```bash
# Update dependencies
pip install --upgrade -r requirements.txt
npm update

# Run tests
pytest
npm test

# Deploy update
git push origin main  # triggers CI/CD
```

---

For additional support or questions about deployment, please refer to the main README or open an issue on GitHub.
