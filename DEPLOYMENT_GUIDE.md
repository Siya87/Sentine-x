# 🚀 SentinelX AI - Deployment Guide

Complete guide for deploying SentinelX AI to production environments.

## 📋 Table of Contents

1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [Environment Variables](#environment-variables)
3. [Deployment Options](#deployment-options)
   - [Docker Deployment](#docker-deployment)
   - [Heroku Deployment](#heroku-deployment)
   - [AWS Deployment](#aws-deployment)
   - [Azure Deployment](#azure-deployment)
   - [Vercel + Railway](#vercel--railway)
4. [Database Setup](#database-setup)
5. [Post-Deployment](#post-deployment)

---

## 🔍 Pre-Deployment Checklist

Before deploying, ensure you have:

- [ ] GitHub repository with latest code
- [ ] All API keys ready (IBM Watsonx, VirusTotal, Shodan, etc.)
- [ ] MongoDB database (Atlas or self-hosted)
- [ ] Domain name (optional but recommended)
- [ ] SSL certificate (most platforms provide free ones)

---

## 🔐 Environment Variables

### Backend (.env)
```env
# MongoDB
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/sentinelx?retryWrites=true&w=majority

# IBM Watsonx AI
WATSONX_API_KEY=your_watsonx_api_key
WATSONX_PROJECT_ID=your_project_id
WATSONX_URL=https://us-south.ml.cloud.ibm.com

# Security APIs
VIRUSTOTAL_API_KEY=your_virustotal_key
SHODAN_API_KEY=your_shodan_key
ABUSEIPDB_API_KEY=your_abuseipdb_key
HAVEIBEENPWNED_API_KEY=your_hibp_key

# Application
DEBUG=false
CORS_ORIGINS=https://your-frontend-domain.com

# Optional
SECRET_KEY=your-secret-key-for-jwt
```

### Frontend (.env)
```env
REACT_APP_API_URL=https://your-backend-domain.com
```

---

## 🐳 Docker Deployment

### 1. Create Dockerfile for Backend

**File:** `backend/Dockerfile`
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 2. Create Dockerfile for Frontend

**File:** `frontend/Dockerfile`
```dockerfile
# Build stage
FROM node:18-alpine AS build

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine

COPY --from=build /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

### 3. Create nginx.conf

**File:** `frontend/nginx.conf`
```nginx
server {
    listen 80;
    server_name localhost;
    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 4. Create docker-compose.yml

**File:** `docker-compose.yml`
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - MONGODB_URI=${MONGODB_URI}
      - WATSONX_API_KEY=${WATSONX_API_KEY}
      - WATSONX_PROJECT_ID=${WATSONX_PROJECT_ID}
      - VIRUSTOTAL_API_KEY=${VIRUSTOTAL_API_KEY}
      - SHODAN_API_KEY=${SHODAN_API_KEY}
      - ABUSEIPDB_API_KEY=${ABUSEIPDB_API_KEY}
      - HAVEIBEENPWNED_API_KEY=${HAVEIBEENPWNED_API_KEY}
    restart: unless-stopped
    networks:
      - sentinelx-network

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    environment:
      - REACT_APP_API_URL=http://backend:8000
    depends_on:
      - backend
    restart: unless-stopped
    networks:
      - sentinelx-network

networks:
  sentinelx-network:
    driver: bridge
```

### 5. Deploy with Docker

```bash
# Build and start containers
docker-compose up -d

# View logs
docker-compose logs -f

# Stop containers
docker-compose down
```

---

## 🟣 Heroku Deployment

### Backend Deployment

1. **Create Procfile**
```bash
# backend/Procfile
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

2. **Create runtime.txt**
```bash
# backend/runtime.txt
python-3.11.0
```

3. **Deploy to Heroku**
```bash
# Login to Heroku
heroku login

# Create app
heroku create sentinelx-backend

# Set environment variables
heroku config:set MONGODB_URI="your_mongodb_uri"
heroku config:set WATSONX_API_KEY="your_key"
# ... set all other env vars

# Deploy
git subtree push --prefix backend heroku main

# Or if using separate repo
cd backend
git init
heroku git:remote -a sentinelx-backend
git add .
git commit -m "Deploy backend"
git push heroku main
```

### Frontend Deployment (Heroku)

1. **Add buildpack**
```bash
heroku create sentinelx-frontend
heroku buildpacks:set mars/create-react-app
```

2. **Set environment variables**
```bash
heroku config:set REACT_APP_API_URL="https://sentinelx-backend.herokuapp.com"
```

3. **Deploy**
```bash
git subtree push --prefix frontend heroku main
```

---

## ☁️ AWS Deployment

### Option 1: AWS Elastic Beanstalk

1. **Install EB CLI**
```bash
pip install awsebcli
```

2. **Initialize EB**
```bash
cd backend
eb init -p python-3.11 sentinelx-backend

cd ../frontend
eb init -p node.js sentinelx-frontend
```

3. **Create environment and deploy**
```bash
eb create sentinelx-backend-env
eb deploy
```

### Option 2: AWS ECS (Docker)

1. **Push Docker images to ECR**
```bash
# Authenticate Docker to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

# Build and push
docker build -t sentinelx-backend ./backend
docker tag sentinelx-backend:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/sentinelx-backend:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/sentinelx-backend:latest
```

2. **Create ECS task definition and service** (use AWS Console or CLI)

---

## 🔷 Azure Deployment

### Backend (Azure App Service)

```bash
# Login to Azure
az login

# Create resource group
az group create --name sentinelx-rg --location eastus

# Create App Service plan
az appservice plan create --name sentinelx-plan --resource-group sentinelx-rg --sku B1 --is-linux

# Create web app
az webapp create --resource-group sentinelx-rg --plan sentinelx-plan --name sentinelx-backend --runtime "PYTHON:3.11"

# Configure deployment
az webapp deployment source config --name sentinelx-backend --resource-group sentinelx-rg --repo-url https://github.com/yourusername/sentinelx --branch main --manual-integration

# Set environment variables
az webapp config appsettings set --resource-group sentinelx-rg --name sentinelx-backend --settings MONGODB_URI="your_uri" WATSONX_API_KEY="your_key"
```

### Frontend (Azure Static Web Apps)

```bash
# Create static web app
az staticwebapp create --name sentinelx-frontend --resource-group sentinelx-rg --source https://github.com/yourusername/sentinelx --branch main --app-location "/frontend" --output-location "build"
```

---

## 🚀 Vercel + Railway (Recommended for Quick Deploy)

### Backend on Railway

1. Go to [Railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Set root directory to `backend`
5. Add environment variables
6. Deploy!

### Frontend on Vercel

1. Go to [Vercel.com](https://vercel.com)
2. Click "New Project" → Import from GitHub
3. Select your repository
4. Set root directory to `frontend`
5. Add environment variable: `REACT_APP_API_URL=https://your-railway-backend.up.railway.app`
6. Deploy!

---

## 🗄️ Database Setup

### MongoDB Atlas (Recommended)

1. **Create Cluster**
   - Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
   - Create free M0 cluster
   - Choose region closest to your deployment

2. **Configure Access**
   - Database Access → Add user
   - Network Access → Add IP (0.0.0.0/0 for production)

3. **Get Connection String**
   ```
   mongodb+srv://username:password@cluster.mongodb.net/sentinelx?retryWrites=true&w=majority
   ```

4. **Create Indexes** (Run once)
   ```javascript
   // Connect to MongoDB and run:
   db.phishing_analyses.createIndex({ "created_at": -1 })
   db.osint_investigations.createIndex({ "target": 1 })
   db.threats.createIndex({ "timestamp": -1 })
   db.reports.createIndex({ "created_at": -1 })
   db.chat_sessions.createIndex({ "created_at": -1 })
   ```

---

## ✅ Post-Deployment

### 1. Health Check

Test your deployment:
```bash
# Backend health
curl https://your-backend-domain.com/health

# Frontend
curl https://your-frontend-domain.com
```

### 2. API Documentation

Access Swagger docs:
```
https://your-backend-domain.com/docs
```

### 3. Monitoring Setup

**Backend Monitoring:**
- Set up logging (Sentry, LogRocket)
- Configure uptime monitoring (UptimeRobot, Pingdom)
- Set up error tracking

**Frontend Monitoring:**
- Google Analytics
- Sentry for error tracking
- Performance monitoring

### 4. Security Checklist

- [ ] HTTPS enabled
- [ ] Environment variables secured
- [ ] CORS properly configured
- [ ] Rate limiting enabled
- [ ] API keys rotated
- [ ] Database backups configured
- [ ] Firewall rules set

### 5. Performance Optimization

**Backend:**
- Enable caching
- Use CDN for static assets
- Optimize database queries
- Enable compression

**Frontend:**
- Enable gzip compression
- Optimize images
- Code splitting
- Lazy loading

---

## 🔧 Troubleshooting

### Common Issues

**1. CORS Errors**
```python
# backend/app/main.py
CORS_ORIGINS = ["https://your-frontend-domain.com"]
```

**2. MongoDB Connection Failed**
- Check connection string
- Verify IP whitelist
- Check credentials

**3. API Keys Not Working**
- Verify environment variables are set
- Check API key validity
- Review rate limits

**4. Build Failures**
- Check Node/Python versions
- Verify all dependencies installed
- Review build logs

---

## 📞 Support

For deployment issues:
- Check logs: `docker-compose logs` or platform-specific logs
- Review [GitHub Issues](https://github.com/yourusername/sentinelx/issues)
- Contact: your-email@example.com

---

**Made with ❤️ by Bob**