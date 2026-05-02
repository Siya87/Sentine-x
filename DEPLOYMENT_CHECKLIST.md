# SentinelX AI - Deployment Checklist

## Pre-Deployment Verification

### ✅ Backend Files
- [x] `backend/Procfile` - Heroku process configuration
- [x] `backend/runtime.txt` - Python version specification
- [x] `backend/requirements.txt` - Python dependencies
- [x] `backend/.env.example` - Environment variable template
- [x] `backend/Dockerfile` - Docker container configuration
- [x] `backend/app/main.py` - FastAPI application entry point

### ✅ Frontend Files
- [x] `frontend/package.json` - Node.js dependencies
- [x] `frontend/.env` - Frontend environment variables
- [x] `frontend/Dockerfile` - Docker container configuration
- [x] `frontend/nginx.conf` - Nginx web server configuration
- [x] `frontend/src/` - React application source code

### ✅ Root Files
- [x] `docker-compose.yml` - Multi-container orchestration
- [x] `.env.example` - Complete environment template
- [x] `DEPLOYMENT_GUIDE.md` - Comprehensive deployment instructions
- [x] `README.md` - Project documentation

---

## Deployment Options

### Option 1: Docker Compose (Recommended for VPS/Local)

**Prerequisites:**
- Docker and Docker Compose installed
- MongoDB Atlas account (or local MongoDB)
- All API keys obtained

**Steps:**
1. Clone repository
2. Copy `.env.example` to `.env` and fill in values
3. Run: `docker-compose up -d`
4. Access: `http://localhost:3000`

**Estimated Time:** 10 minutes

---

### Option 2: Heroku (Easiest Cloud Deployment)

**Prerequisites:**
- Heroku account
- Heroku CLI installed
- MongoDB Atlas account
- All API keys obtained

**Backend Deployment:**
```bash
cd backend
heroku create sentinelx-backend
heroku config:set MONGODB_URI="your_mongodb_uri"
heroku config:set IBM_WATSONX_API_KEY="your_api_key"
heroku config:set IBM_WATSONX_PROJECT_ID="your_project_id"
heroku config:set VIRUSTOTAL_API_KEY="your_key"
heroku config:set SHODAN_API_KEY="your_key"
heroku config:set ABUSEIPDB_API_KEY="your_key"
heroku config:set HIBP_API_KEY="your_key"
git push heroku main
```

**Frontend Deployment:**
```bash
cd frontend
heroku create sentinelx-frontend
heroku buildpacks:set heroku/nodejs
heroku config:set REACT_APP_API_URL="https://sentinelx-backend.herokuapp.com"
git push heroku main
```

**Estimated Time:** 20 minutes

---

### Option 3: Vercel (Frontend) + Railway (Backend)

**Prerequisites:**
- Vercel account
- Railway account
- MongoDB Atlas account
- All API keys obtained

**Backend on Railway:**
1. Go to railway.app
2. Click "New Project" → "Deploy from GitHub"
3. Select your repository
4. Set root directory to `backend`
5. Add all environment variables
6. Deploy

**Frontend on Vercel:**
1. Go to vercel.com
2. Click "Import Project"
3. Select your repository
4. Set root directory to `frontend`
5. Add environment variable: `REACT_APP_API_URL=<railway_backend_url>`
6. Deploy

**Estimated Time:** 15 minutes

---

### Option 4: AWS Elastic Beanstalk

**Prerequisites:**
- AWS account
- AWS CLI installed and configured
- MongoDB Atlas account
- All API keys obtained

**Backend Deployment:**
```bash
cd backend
eb init -p python-3.11 sentinelx-backend
eb create sentinelx-backend-env
eb setenv MONGODB_URI="your_uri" IBM_WATSONX_API_KEY="your_key" ...
eb deploy
```

**Frontend Deployment:**
```bash
cd frontend
npm run build
# Upload build folder to S3 + CloudFront
```

**Estimated Time:** 30 minutes

---

### Option 5: Azure App Service

**Prerequisites:**
- Azure account
- Azure CLI installed
- MongoDB Atlas account
- All API keys obtained

**Backend Deployment:**
```bash
cd backend
az webapp up --name sentinelx-backend --runtime "PYTHON:3.11"
az webapp config appsettings set --name sentinelx-backend --settings @env-vars.json
```

**Frontend Deployment:**
```bash
cd frontend
npm run build
az storage blob upload-batch -s build -d '$web' --account-name sentinelxfrontend
```

**Estimated Time:** 25 minutes

---

## Required API Keys and Services

### 1. MongoDB Atlas (Database)
- **URL:** https://www.mongodb.com/cloud/atlas
- **Free Tier:** Yes (512MB)
- **Setup Time:** 5 minutes
- **Required:** Yes

**Steps:**
1. Create account
2. Create cluster (M0 Free tier)
3. Create database user
4. Whitelist IP (0.0.0.0/0 for all IPs)
5. Get connection string

### 2. IBM Watsonx AI (Core AI Engine)
- **URL:** https://www.ibm.com/watsonx
- **Free Tier:** Trial available
- **Setup Time:** 10 minutes
- **Required:** Yes

**Steps:**
1. Create IBM Cloud account
2. Create Watsonx.ai instance
3. Get API key and Project ID
4. Note the service URL

### 3. VirusTotal (Malware Scanning)
- **URL:** https://www.virustotal.com/gui/join-us
- **Free Tier:** Yes (4 requests/minute)
- **Setup Time:** 2 minutes
- **Required:** Yes

**Steps:**
1. Create account
2. Go to API Key section
3. Copy API key

### 4. Shodan (Threat Intelligence)
- **URL:** https://account.shodan.io/register
- **Free Tier:** Limited (1 result per search)
- **Setup Time:** 2 minutes
- **Required:** Yes

**Steps:**
1. Create account
2. Go to Account page
3. Copy API key

### 5. AbuseIPDB (IP Reputation)
- **URL:** https://www.abuseipdb.com/register
- **Free Tier:** Yes (1000 checks/day)
- **Setup Time:** 2 minutes
- **Required:** Yes

**Steps:**
1. Create account
2. Go to API section
3. Generate API key

### 6. HaveIBeenPwned (Breach Data)
- **URL:** https://haveibeenpwned.com/API/Key
- **Free Tier:** No (Paid API)
- **Setup Time:** 5 minutes
- **Required:** Optional (can work without it)

**Steps:**
1. Purchase API key ($3.50/month)
2. Receive key via email

---

## Environment Variables Setup

### Backend (.env)
```bash
# Database
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/sentinelx?retryWrites=true&w=majority

# IBM Watsonx AI
IBM_WATSONX_API_KEY=your_api_key_here
IBM_WATSONX_PROJECT_ID=your_project_id_here
IBM_WATSONX_URL=https://us-south.ml.cloud.ibm.com

# Security APIs
VIRUSTOTAL_API_KEY=your_virustotal_key
SHODAN_API_KEY=your_shodan_key
ABUSEIPDB_API_KEY=your_abuseipdb_key
HIBP_API_KEY=your_hibp_key

# Application
SECRET_KEY=your_secret_key_here_min_32_chars
ENVIRONMENT=production
DEBUG=false
ALLOWED_ORIGINS=https://your-frontend-domain.com
```

### Frontend (.env)
```bash
REACT_APP_API_URL=https://your-backend-domain.com
```

---

## Post-Deployment Verification

### 1. Backend Health Check
```bash
curl https://your-backend-url.com/health
```
Expected response:
```json
{
  "status": "healthy",
  "database": "connected",
  "ai_service": "available"
}
```

### 2. Frontend Access
- Open browser: `https://your-frontend-url.com`
- Should see SentinelX AI dashboard
- Check console for errors

### 3. API Integration Test
- Go to Phishing Detector page
- Upload a test file or URL
- Verify analysis results appear

### 4. Database Connection
- Check MongoDB Atlas dashboard
- Verify connections are active
- Check for any error logs

---

## Troubleshooting

### Backend Issues

**Problem:** "Module not found" error
**Solution:** 
```bash
pip install -r requirements.txt
```

**Problem:** "Database connection failed"
**Solution:**
- Verify MongoDB URI is correct
- Check IP whitelist in MongoDB Atlas
- Ensure database user has correct permissions

**Problem:** "IBM Watsonx authentication failed"
**Solution:**
- Verify API key and Project ID
- Check service URL is correct
- Ensure Watsonx.ai instance is active

### Frontend Issues

**Problem:** "API request failed"
**Solution:**
- Verify REACT_APP_API_URL is correct
- Check CORS settings in backend
- Ensure backend is running

**Problem:** "Build failed"
**Solution:**
```bash
rm -rf node_modules package-lock.json
npm install
npm run build
```

### Docker Issues

**Problem:** "Container exits immediately"
**Solution:**
- Check logs: `docker logs <container_id>`
- Verify environment variables
- Check Dockerfile syntax

---

## Security Checklist

- [ ] All API keys stored in environment variables (not in code)
- [ ] MongoDB IP whitelist configured
- [ ] HTTPS enabled for production
- [ ] CORS properly configured
- [ ] Rate limiting enabled
- [ ] Input validation implemented
- [ ] Error messages don't expose sensitive info
- [ ] Logs don't contain API keys or passwords
- [ ] Database backups configured
- [ ] Monitoring and alerts set up

---

## Performance Optimization

### Backend
- [ ] Enable caching for frequent queries
- [ ] Use connection pooling for MongoDB
- [ ] Implement request rate limiting
- [ ] Add response compression
- [ ] Monitor API response times

### Frontend
- [ ] Enable code splitting
- [ ] Optimize images and assets
- [ ] Use lazy loading for components
- [ ] Enable browser caching
- [ ] Minify CSS and JavaScript

---

## Monitoring and Maintenance

### Recommended Tools
1. **Sentry** - Error tracking
2. **LogRocket** - Session replay
3. **New Relic** - Performance monitoring
4. **UptimeRobot** - Uptime monitoring
5. **MongoDB Atlas Monitoring** - Database metrics

### Regular Tasks
- [ ] Check error logs daily
- [ ] Monitor API usage and costs
- [ ] Review security alerts
- [ ] Update dependencies monthly
- [ ] Backup database weekly
- [ ] Review performance metrics

---

## Cost Estimation

### Free Tier (Development/Testing)
- MongoDB Atlas: Free (M0)
- Heroku: Free (with limitations)
- VirusTotal: Free (4 req/min)
- Shodan: Free (limited)
- AbuseIPDB: Free (1000/day)
- **Total: $0/month**

### Production (Low Traffic)
- MongoDB Atlas: $9/month (M10)
- Heroku: $14/month (Hobby dyno × 2)
- VirusTotal: Free
- Shodan: $59/month (Membership)
- AbuseIPDB: Free
- HaveIBeenPwned: $3.50/month
- **Total: ~$85/month**

### Production (High Traffic)
- MongoDB Atlas: $57/month (M30)
- AWS/Azure: $100-200/month
- Shodan: $59/month
- HaveIBeenPwned: $3.50/month
- CDN: $20/month
- **Total: ~$240-320/month**

---

## Quick Start Commands

### Local Development
```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm start
```

### Docker Deployment
```bash
docker-compose up -d
docker-compose logs -f
docker-compose down
```

### Heroku Deployment
```bash
# Backend
cd backend
heroku create sentinelx-backend
git push heroku main

# Frontend
cd frontend
heroku create sentinelx-frontend
git push heroku main
```

---

## Support and Resources

- **Documentation:** See DEPLOYMENT_GUIDE.md
- **Architecture:** See ARCHITECTURE.md
- **API Docs:** See TECHNICAL_SPECS.md
- **Quick Start:** See QUICK_START.md

---

## Next Steps After Deployment

1. **Test All Features**
   - Phishing Detector
   - OSINT Investigation
   - Threat Intelligence
   - Report Generator
   - Chat Assistant

2. **Configure Custom Domain**
   - Purchase domain
   - Configure DNS
   - Enable SSL/TLS

3. **Set Up Monitoring**
   - Error tracking
   - Performance monitoring
   - Uptime monitoring

4. **Create Demo Account**
   - Prepare sample data
   - Create demo scenarios
   - Document demo flow

5. **Marketing Materials**
   - Screenshots
   - Demo video
   - Feature highlights
   - Use cases

---

**Deployment Status:** Ready for production deployment
**Last Updated:** 2026-05-02
**Version:** 1.0.0