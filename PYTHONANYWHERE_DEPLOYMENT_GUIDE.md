# 🐍 PythonAnywhere Deployment Guide for SentinelX AI Backend

## ⚠️ Important Note About PythonAnywhere

**PythonAnywhere Free Tier Limitations:**
- ❌ **No external API access** (can't call VirusTotal, Shodan, IBM Watsonx, etc.)
- ❌ **No MongoDB Atlas connection** (only whitelisted sites allowed)
- ❌ **Limited to specific Python packages**
- ✅ **Good for:** Simple web apps without external dependencies

**Verdict:** PythonAnywhere's free tier **won't work** for SentinelX AI because your app needs:
1. MongoDB Atlas connection
2. IBM Watsonx AI API
3. VirusTotal, Shodan, AbuseIPDB APIs
4. External HTTP requests

---

## 🎯 Better Free Alternatives

### Option 1: Railway ⭐ HIGHLY RECOMMENDED
**Why Railway is Better:**
- ✅ $5 free credit (lasts ~1 month)
- ✅ Full external API access
- ✅ MongoDB Atlas connection works
- ✅ Better Python support
- ✅ Automatic HTTPS
- ✅ Easy deployment from GitHub

**Setup Time:** 10 minutes

---

### Option 2: Fly.io
**Why Fly.io is Good:**
- ✅ Free tier with 3 VMs
- ✅ Full external API access
- ✅ Good for FastAPI apps
- ✅ Automatic HTTPS

**Setup Time:** 15 minutes

---

### Option 3: Koyeb
**Why Koyeb is Good:**
- ✅ Completely free tier
- ✅ External API access
- ✅ MongoDB connection works
- ✅ Docker support

**Setup Time:** 10 minutes

---

## 🚀 Recommended Deployment Stack

### Best Free Combination:
```
Frontend: Vercel (Free Forever)
Backend: Railway ($5 credit) or Koyeb (Free)
Database: MongoDB Atlas (Free 512MB)
```

**Total Cost:** $0 for first month, then $5/month for Railway

---

## 📋 Railway Deployment Guide (Recommended)

### Step 1: Create Railway Account
1. Go to https://railway.app
2. Click "Start a New Project"
3. Sign up with GitHub (no credit card needed)
4. You get $5 free credit automatically

### Step 2: Deploy Backend
1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose your `Sentine-x` repository
4. Railway will auto-detect it's a Python project

### Step 3: Configure Service
1. Click on your service
2. Go to "Settings"
3. Set **Root Directory:** `backend`
4. Set **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Step 4: Add Environment Variables
Click "Variables" tab and add:

```bash
MONGODB_URI=your_mongodb_atlas_uri
IBM_WATSONX_API_KEY=your_api_key
IBM_WATSONX_PROJECT_ID=your_project_id
IBM_WATSONX_URL=https://us-south.ml.cloud.ibm.com
VIRUSTOTAL_API_KEY=your_key
SHODAN_API_KEY=your_key
ABUSEIPDB_API_KEY=your_key
HIBP_API_KEY=your_key
SECRET_KEY=your_random_32_char_string
ENVIRONMENT=production
DEBUG=false
ALLOWED_ORIGINS=*
```

### Step 5: Deploy
1. Click "Deploy"
2. Wait 5-10 minutes
3. Your backend will be live at: `https://your-app.up.railway.app`

### Step 6: Test
```bash
curl https://your-app.up.railway.app/health
```

Expected response:
```json
{
  "status": "healthy",
  "database": "connected"
}
```

---

## 📋 Koyeb Deployment Guide (100% Free Alternative)

### Step 1: Create Koyeb Account
1. Go to https://www.koyeb.com
2. Sign up with GitHub
3. No credit card required

### Step 2: Create New App
1. Click "Create App"
2. Select "GitHub"
3. Choose your repository
4. Select `backend` directory

### Step 3: Configure
```
Name: sentinelx-backend
Region: Choose closest to you
Builder: Dockerfile
Dockerfile path: ./Dockerfile
Port: 8000
```

### Step 4: Add Environment Variables
Same as Railway (see above)

### Step 5: Deploy
1. Click "Deploy"
2. Wait 5-10 minutes
3. Your backend will be live

---

## 📋 Fly.io Deployment Guide

### Step 1: Install Fly CLI
```bash
# Windows (PowerShell)
iwr https://fly.io/install.ps1 -useb | iex
```

### Step 2: Sign Up and Login
```bash
fly auth signup
fly auth login
```

### Step 3: Deploy
```bash
cd backend
fly launch
# Follow prompts
fly secrets set MONGODB_URI="..." IBM_WATSONX_API_KEY="..." # etc.
fly deploy
```

---

## 🎯 My Recommendation

**Use Railway for Backend + Vercel for Frontend**

### Why This Combination?
1. **Railway:**
   - $5 credit lasts ~1 month
   - Perfect for Python/FastAPI
   - All external APIs work
   - Easy setup

2. **Vercel:**
   - Free forever for frontend
   - Automatic deployments
   - Global CDN
   - Perfect for React

### Total Cost:
- **Month 1:** $0 (Railway free credit)
- **Month 2+:** $5/month (Railway)
- **Frontend:** Always free (Vercel)

---

## 🔧 Quick Start with Railway

### 1. Sign Up
```
https://railway.app
→ Sign up with GitHub
→ Get $5 free credit
```

### 2. Deploy
```
New Project
→ Deploy from GitHub
→ Select Sentine-x repo
→ Add environment variables
→ Deploy
```

### 3. Get URL
```
Your backend: https://sentinelx-backend.up.railway.app
```

### 4. Update Frontend
```
In Vercel:
REACT_APP_API_URL=https://sentinelx-backend.up.railway.app
```

---

## ✅ Deployment Checklist

### Railway Deployment:
- [ ] Create Railway account
- [ ] Connect GitHub repository
- [ ] Set root directory to `backend`
- [ ] Add all environment variables
- [ ] Deploy and wait for build
- [ ] Test `/health` endpoint
- [ ] Update frontend with backend URL

### Vercel Deployment:
- [ ] Create Vercel account
- [ ] Import GitHub repository
- [ ] Set root directory to `frontend`
- [ ] Add `REACT_APP_API_URL` variable
- [ ] Deploy and test

---

## 🎉 Expected Result

After deployment:
- ✅ Backend live on Railway
- ✅ Frontend live on Vercel
- ✅ MongoDB Atlas connected
- ✅ All APIs working
- ✅ HTTPS enabled
- ✅ Global CDN

**Your URLs:**
- Frontend: `https://sentine-x.vercel.app`
- Backend: `https://sentinelx-backend.up.railway.app`

---

## 📞 Need Help?

### Railway Support:
- Docs: https://docs.railway.app
- Discord: https://discord.gg/railway

### Koyeb Support:
- Docs: https://www.koyeb.com/docs
- Community: https://community.koyeb.com

---

**Recommendation:** Start with Railway - it's the easiest and most reliable for your use case!

**Last Updated:** 2026-05-02