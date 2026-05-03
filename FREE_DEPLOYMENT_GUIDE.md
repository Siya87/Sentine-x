# 🆓 SentinelX AI - 100% Free Deployment Guide

## ✅ Completely Free Deployment Options

This guide focuses on platforms that offer **permanent free tiers** with no credit card required (or optional).

---

## 🎯 Recommended Free Stack

### Best Free Combination:
- **Frontend:** Vercel (Free Forever)
- **Backend:** Render (Free tier)
- **Database:** MongoDB Atlas (Free 512MB)
- **Total Cost:** $0/month permanently

---

## Option 1: Vercel (Frontend) + Render (Backend) ⭐ RECOMMENDED

### Why This Stack?
- ✅ 100% Free forever
- ✅ No credit card required
- ✅ Automatic HTTPS
- ✅ Global CDN
- ✅ Automatic deployments from Git
- ✅ Easy setup (15 minutes)

---

### Step 1: Deploy Backend on Render

**Render Free Tier:**
- 512 MB RAM
- Shared CPU
- 100 GB bandwidth/month
- Automatic HTTPS
- Free custom domains
- **Limitation:** Spins down after 15 min of inactivity (cold start ~30 seconds)

#### 1.1 Create Render Account
1. Go to https://render.com
2. Sign up with GitHub (no credit card needed)
3. Authorize Render to access your repositories

#### 1.2 Deploy Backend
1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository
3. Configure:
   ```
   Name: sentinelx-backend
   Region: Choose closest to you
   Branch: main
   Root Directory: backend
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

4. Click **"Advanced"** and add environment variables:
   ```
   MONGODB_URI=your_mongodb_atlas_uri
   IBM_WATSONX_API_KEY=your_api_key
   IBM_WATSONX_PROJECT_ID=your_project_id
   IBM_WATSONX_URL=https://us-south.ml.cloud.ibm.com
   VIRUSTOTAL_API_KEY=your_key
   SHODAN_API_KEY=your_key
   ABUSEIPDB_API_KEY=your_key
   HIBP_API_KEY=your_key
   SECRET_KEY=generate_random_32_char_string
   ENVIRONMENT=production
   DEBUG=false
   ALLOWED_ORIGINS=https://your-frontend.vercel.app
   ```

5. Click **"Create Web Service"**
6. Wait 5-10 minutes for deployment
7. Copy your backend URL: `https://sentinelx-backend.onrender.com`

---

### Step 2: Deploy Frontend on Vercel

**Vercel Free Tier:**
- Unlimited bandwidth
- Unlimited deployments
- Automatic HTTPS
- Global CDN
- Custom domains
- **No limitations for hobby projects**

#### 2.1 Create Vercel Account
1. Go to https://vercel.com
2. Sign up with GitHub (no credit card needed)
3. Authorize Vercel to access your repositories

#### 2.2 Deploy Frontend
1. Click **"Add New..."** → **"Project"**
2. Import your GitHub repository
3. Configure:
   ```
   Framework Preset: Create React App
   Root Directory: frontend
   Build Command: npm run build
   Output Directory: build
   Install Command: npm install
   ```

4. Add environment variable:
   ```
   REACT_APP_API_URL=https://sentinelx-backend.onrender.com
   ```

5. Click **"Deploy"**
6. Wait 2-3 minutes for deployment
7. Your app is live at: `https://your-project.vercel.app`

---

## Option 2: Netlify (Frontend) + Render (Backend)

### Step 1: Deploy Backend on Render
(Same as Option 1 above)

### Step 2: Deploy Frontend on Netlify

**Netlify Free Tier:**
- 100 GB bandwidth/month
- Unlimited sites
- Automatic HTTPS
- Custom domains
- Form handling

#### 2.1 Create Netlify Account
1. Go to https://netlify.com
2. Sign up with GitHub (no credit card needed)

#### 2.2 Deploy Frontend
1. Click **"Add new site"** → **"Import an existing project"**
2. Connect to GitHub and select your repository
3. Configure:
   ```
   Base directory: frontend
   Build command: npm run build
   Publish directory: frontend/build
   ```

4. Add environment variable:
   ```
   REACT_APP_API_URL=https://sentinelx-backend.onrender.com
   ```

5. Click **"Deploy site"**
6. Your app is live at: `https://your-site.netlify.app`

---

## Option 3: GitHub Pages (Frontend) + Render (Backend)

### Step 1: Deploy Backend on Render
(Same as Option 1 above)

### Step 2: Deploy Frontend on GitHub Pages

**GitHub Pages Free Tier:**
- 1 GB storage
- 100 GB bandwidth/month
- Automatic HTTPS
- Custom domains
- **Best for:** Static sites

#### 2.1 Install gh-pages Package
```bash
cd frontend
npm install --save-dev gh-pages
```

#### 2.2 Update package.json
Add to `frontend/package.json`:
```json
{
  "homepage": "https://your-username.github.io/sentinelx-ai",
  "scripts": {
    "predeploy": "npm run build",
    "deploy": "gh-pages -d build"
  }
}
```

#### 2.3 Update Environment Variable
Create `frontend/.env.production`:
```bash
REACT_APP_API_URL=https://sentinelx-backend.onrender.com
```

#### 2.4 Deploy
```bash
cd frontend
npm run deploy
```

Your app is live at: `https://your-username.github.io/sentinelx-ai`

---

## Option 4: Railway (Backend) - Free Trial

**Railway Free Trial:**
- $5 free credit (no credit card needed initially)
- Lasts ~1 month for small apps
- After trial: $5/month minimum

### Deploy Backend on Railway

1. Go to https://railway.app
2. Sign up with GitHub
3. Click **"New Project"** → **"Deploy from GitHub repo"**
4. Select your repository
5. Configure:
   ```
   Root Directory: backend
   Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```
6. Add all environment variables
7. Deploy

**Note:** After free trial ends, you'll need to add payment method.

---

## Option 5: Cyclic (Backend) - Free Tier

**Cyclic Free Tier:**
- 10,000 requests/month
- 1 GB storage
- Automatic HTTPS
- Custom domains

### Deploy Backend on Cyclic

1. Go to https://cyclic.sh
2. Sign up with GitHub
3. Click **"Link Your Own"**
4. Select your repository
5. Set root directory: `backend`
6. Add environment variables
7. Deploy

**Limitation:** 10,000 requests/month might be limiting for production.

---

## Option 6: Fly.io (Backend) - Free Tier

**Fly.io Free Tier:**
- 3 shared-cpu-1x VMs
- 160 GB bandwidth/month
- Automatic HTTPS

### Deploy Backend on Fly.io

1. Install Fly CLI:
   ```bash
   # Windows (PowerShell)
   iwr https://fly.io/install.ps1 -useb | iex
   ```

2. Sign up and login:
   ```bash
   fly auth signup
   fly auth login
   ```

3. Deploy:
   ```bash
   cd backend
   fly launch
   # Follow prompts, select region
   fly secrets set MONGODB_URI="..." IBM_WATSONX_API_KEY="..." # etc.
   fly deploy
   ```

---

## 🗄️ Free Database: MongoDB Atlas

**MongoDB Atlas Free Tier (M0):**
- 512 MB storage
- Shared RAM
- Shared vCPU
- **Free forever**

### Setup MongoDB Atlas

1. Go to https://www.mongodb.com/cloud/atlas
2. Sign up (no credit card required)
3. Create a **FREE M0 cluster**:
   - Provider: AWS/GCP/Azure (any)
   - Region: Choose closest to you
   - Cluster Name: sentinelx-cluster

4. Create Database User:
   - Username: `sentinelx_user`
   - Password: Generate strong password
   - Save credentials securely

5. Network Access:
   - Click **"Add IP Address"**
   - Select **"Allow Access from Anywhere"** (0.0.0.0/0)
   - Or add specific IPs of your deployment platforms

6. Get Connection String:
   - Click **"Connect"** → **"Connect your application"**
   - Copy connection string:
     ```
     mongodb+srv://sentinelx_user:<password>@cluster.mongodb.net/sentinelx?retryWrites=true&w=majority
     ```
   - Replace `<password>` with your actual password

---

## 🔑 Free API Keys

### 1. IBM Watsonx AI
- **Free Trial:** Available
- **URL:** https://www.ibm.com/watsonx
- **Setup:**
  1. Create IBM Cloud account
  2. Create Watsonx.ai instance (Lite plan)
  3. Get API key and Project ID

### 2. VirusTotal
- **Free Tier:** 4 requests/minute
- **URL:** https://www.virustotal.com/gui/join-us
- **Setup:**
  1. Create account
  2. Go to API Key section
  3. Copy API key

### 3. Shodan
- **Free Tier:** 1 result per search
- **URL:** https://account.shodan.io/register
- **Setup:**
  1. Create account
  2. Go to Account page
  3. Copy API key

### 4. AbuseIPDB
- **Free Tier:** 1,000 checks/day
- **URL:** https://www.abuseipdb.com/register
- **Setup:**
  1. Create account
  2. Go to API section
  3. Generate API key

### 5. HaveIBeenPwned (Optional)
- **Cost:** $3.50/month (not free)
- **Alternative:** Skip this API, app will work without it

---

## 📋 Complete Free Deployment Checklist

### Prerequisites (All Free)
- [ ] GitHub account
- [ ] MongoDB Atlas account (Free M0 cluster)
- [ ] Render account (for backend)
- [ ] Vercel account (for frontend)
- [ ] All free API keys obtained

### Backend Deployment
- [ ] Push code to GitHub
- [ ] Create Render web service
- [ ] Configure environment variables
- [ ] Deploy backend
- [ ] Test health endpoint: `https://your-backend.onrender.com/health`

### Frontend Deployment
- [ ] Update `REACT_APP_API_URL` in Vercel
- [ ] Create Vercel project
- [ ] Deploy frontend
- [ ] Test frontend: `https://your-project.vercel.app`

### Post-Deployment
- [ ] Test all features
- [ ] Check browser console for errors
- [ ] Verify API integrations
- [ ] Monitor Render logs for backend errors

---

## ⚠️ Free Tier Limitations

### Render (Backend)
- **Cold Start:** App sleeps after 15 min of inactivity
- **First Request:** Takes ~30 seconds to wake up
- **Solution:** Use a free uptime monitor (UptimeRobot) to ping every 14 minutes

### MongoDB Atlas (M0)
- **Storage:** 512 MB limit
- **Connections:** Limited concurrent connections
- **Solution:** Sufficient for development and small-scale production

### Vercel (Frontend)
- **Bandwidth:** Unlimited for hobby projects
- **Builds:** 100 hours/month
- **Solution:** More than enough for most projects

---

## 🚀 Quick Start Commands

### 1. Setup MongoDB Atlas
```bash
# Get connection string from MongoDB Atlas dashboard
# Format: mongodb+srv://username:password@cluster.mongodb.net/sentinelx
```

### 2. Deploy Backend on Render
```bash
# No CLI needed - use Render dashboard
# Just connect GitHub repo and configure
```

### 3. Deploy Frontend on Vercel
```bash
# Option A: Use Vercel dashboard (recommended)
# Option B: Use Vercel CLI
npm install -g vercel
cd frontend
vercel --prod
```

---

## 🔧 Troubleshooting Free Deployments

### Issue: Render backend is slow
**Cause:** Cold start after inactivity
**Solution:** 
- Use UptimeRobot to ping every 14 minutes
- Or accept 30-second first load time

### Issue: MongoDB connection timeout
**Cause:** IP not whitelisted
**Solution:**
- Add 0.0.0.0/0 to MongoDB Atlas IP whitelist
- Or add Render's IP addresses

### Issue: Vercel build fails
**Cause:** Missing dependencies or environment variables
**Solution:**
```bash
# Test build locally first
cd frontend
npm install
npm run build
# If successful, push to GitHub and redeploy
```

### Issue: CORS errors
**Cause:** Backend ALLOWED_ORIGINS not configured
**Solution:**
- Add your Vercel URL to ALLOWED_ORIGINS in Render
- Format: `https://your-project.vercel.app`

---

## 📊 Free Tier Comparison

| Platform | Backend | Frontend | Database | Cost |
|----------|---------|----------|----------|------|
| **Render + Vercel** | ✅ Free | ✅ Free | MongoDB Atlas | $0 |
| **Netlify + Render** | ✅ Free | ✅ Free | MongoDB Atlas | $0 |
| **GitHub Pages + Render** | ✅ Free | ✅ Free | MongoDB Atlas | $0 |
| **Cyclic + Vercel** | ⚠️ Limited | ✅ Free | MongoDB Atlas | $0 |
| **Fly.io + Vercel** | ✅ Free | ✅ Free | MongoDB Atlas | $0 |

---

## 🎯 Recommended Free Setup

### For Best Performance (Free):
```
Frontend: Vercel
Backend: Render
Database: MongoDB Atlas (M0)
Monitoring: UptimeRobot (free)
```

### Setup Time: ~20 minutes
### Monthly Cost: $0
### Limitations: Cold starts on backend

---

## 📈 Keeping Backend Awake (Free)

### Use UptimeRobot (Free Monitoring)

1. Go to https://uptimerobot.com
2. Sign up (free account)
3. Add new monitor:
   ```
   Monitor Type: HTTP(s)
   Friendly Name: SentinelX Backend
   URL: https://sentinelx-backend.onrender.com/health
   Monitoring Interval: 5 minutes
   ```
4. This pings your backend every 5 minutes, preventing cold starts

**Free Tier:**
- 50 monitors
- 5-minute intervals
- Email alerts

---

## 🎉 Success Checklist

After deployment, verify:
- [ ] Backend health check returns 200 OK
- [ ] Frontend loads without errors
- [ ] Dashboard shows statistics
- [ ] Phishing detector analyzes files
- [ ] OSINT investigation works
- [ ] Threat intelligence displays data
- [ ] Report generator creates reports
- [ ] Chat assistant responds

---

## 📞 Support Resources

### Free Deployment Platforms
- **Render Docs:** https://render.com/docs
- **Vercel Docs:** https://vercel.com/docs
- **Netlify Docs:** https://docs.netlify.com
- **MongoDB Atlas:** https://docs.atlas.mongodb.com

### Community Support
- **Render Community:** https://community.render.com
- **Vercel Discord:** https://vercel.com/discord
- **Stack Overflow:** Tag questions with platform names

---

## 🚀 Deploy Now!

### Quick Start (15 minutes):

1. **MongoDB Atlas** (5 min)
   - Create free M0 cluster
   - Get connection string

2. **Render Backend** (5 min)
   - Connect GitHub repo
   - Add environment variables
   - Deploy

3. **Vercel Frontend** (5 min)
   - Connect GitHub repo
   - Add REACT_APP_API_URL
   - Deploy

**Total Cost: $0/month forever** 🎉

---

**Last Updated:** 2026-05-02
**Version:** 1.0.0
**Status:** ✅ Ready for free deployment