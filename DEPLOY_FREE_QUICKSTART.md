# 🚀 Deploy SentinelX AI for FREE - Quick Start

## ⚡ 15-Minute Free Deployment

### 🎯 What You'll Get (100% Free)
- ✅ Live production website
- ✅ Backend API with AI capabilities
- ✅ MongoDB database (512MB)
- ✅ Automatic HTTPS
- ✅ Global CDN
- ✅ Custom domain support
- **💰 Total Cost: $0/month forever**

---

## 📋 Prerequisites (5 minutes)

### 1. Create Free Accounts (No Credit Card Required)
- [ ] **GitHub** - https://github.com/signup
- [ ] **MongoDB Atlas** - https://www.mongodb.com/cloud/atlas/register
- [ ] **Render** - https://render.com (sign up with GitHub)
- [ ] **Vercel** - https://vercel.com/signup (sign up with GitHub)

### 2. Get Free API Keys
- [ ] **VirusTotal** - https://www.virustotal.com/gui/join-us
- [ ] **Shodan** - https://account.shodan.io/register
- [ ] **AbuseIPDB** - https://www.abuseipdb.com/register
- [ ] **IBM Watsonx** - https://www.ibm.com/watsonx (free trial)

---

## 🗄️ Step 1: Setup MongoDB Atlas (5 minutes)

### 1.1 Create Free Cluster
1. Go to https://www.mongodb.com/cloud/atlas
2. Click **"Try Free"**
3. Sign up with Google/GitHub
4. Choose **"M0 FREE"** cluster
5. Select cloud provider (AWS/GCP/Azure - any)
6. Choose region closest to you
7. Cluster name: `sentinelx-cluster`
8. Click **"Create"**

### 1.2 Create Database User
1. Go to **"Database Access"**
2. Click **"Add New Database User"**
3. Username: `sentinelx_user`
4. Password: Click **"Autogenerate Secure Password"**
5. **SAVE THIS PASSWORD!** You'll need it
6. Database User Privileges: **"Read and write to any database"**
7. Click **"Add User"**

### 1.3 Allow Network Access
1. Go to **"Network Access"**
2. Click **"Add IP Address"**
3. Click **"Allow Access from Anywhere"** (0.0.0.0/0)
4. Click **"Confirm"**

### 1.4 Get Connection String
1. Go to **"Database"** → Click **"Connect"**
2. Choose **"Connect your application"**
3. Copy the connection string:
   ```
   mongodb+srv://sentinelx_user:<password>@cluster.mongodb.net/sentinelx?retryWrites=true&w=majority
   ```
4. Replace `<password>` with your actual password
5. **SAVE THIS CONNECTION STRING!**

✅ **MongoDB Setup Complete!**

---

## 🔧 Step 2: Deploy Backend on Render (5 minutes)

### 2.1 Connect GitHub
1. Go to https://render.com
2. Click **"Get Started for Free"**
3. Sign up with GitHub
4. Authorize Render to access your repositories

### 2.2 Create Web Service
1. Click **"New +"** → **"Web Service"**
2. Click **"Connect account"** if needed
3. Find and select your `sentinelx-ai` repository
4. Click **"Connect"**

### 2.3 Configure Service
Fill in these settings:

**Basic Settings:**
```
Name: sentinelx-backend
Region: Oregon (US West) or closest to you
Branch: main
Root Directory: backend
Runtime: Python 3
```

**Build & Deploy:**
```
Build Command: pip install -r requirements.txt
Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

**Instance Type:**
```
Select: Free
```

### 2.4 Add Environment Variables
Click **"Advanced"** → **"Add Environment Variable"**

Add these one by one:

```bash
# Database
MONGODB_URI=mongodb+srv://sentinelx_user:YOUR_PASSWORD@cluster.mongodb.net/sentinelx?retryWrites=true&w=majority

# IBM Watsonx AI
IBM_WATSONX_API_KEY=your_watsonx_api_key
IBM_WATSONX_PROJECT_ID=your_project_id
IBM_WATSONX_URL=https://us-south.ml.cloud.ibm.com

# Security APIs
VIRUSTOTAL_API_KEY=your_virustotal_key
SHODAN_API_KEY=your_shodan_key
ABUSEIPDB_API_KEY=your_abuseipdb_key
HIBP_API_KEY=leave_empty_if_you_dont_have

# Application Settings
SECRET_KEY=your_random_32_character_secret_key_here_make_it_long
ENVIRONMENT=production
DEBUG=false
ALLOWED_ORIGINS=*
```

**Generate SECRET_KEY:**
```bash
# Run this in terminal to generate random key:
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 2.5 Deploy
1. Click **"Create Web Service"**
2. Wait 5-10 minutes for deployment
3. Once deployed, you'll see: **"Your service is live 🎉"**
4. Copy your backend URL: `https://sentinelx-backend.onrender.com`
5. Test it: Open `https://sentinelx-backend.onrender.com/health`
   - Should see: `{"status":"healthy"}`

✅ **Backend Deployed!**

---

## 🎨 Step 3: Deploy Frontend on Vercel (5 minutes)

### 3.1 Connect GitHub
1. Go to https://vercel.com
2. Click **"Start Deploying"**
3. Sign up with GitHub
4. Authorize Vercel to access your repositories

### 3.2 Import Project
1. Click **"Add New..."** → **"Project"**
2. Find and select your `sentinelx-ai` repository
3. Click **"Import"**

### 3.3 Configure Project
Fill in these settings:

**Framework Preset:**
```
Create React App (should auto-detect)
```

**Root Directory:**
```
Click "Edit" → Select "frontend" folder
```

**Build Settings:**
```
Build Command: npm run build
Output Directory: build
Install Command: npm install
```

### 3.4 Add Environment Variable
Click **"Environment Variables"**

Add this variable:
```
Name: REACT_APP_API_URL
Value: https://sentinelx-backend.onrender.com
```
(Use your actual Render backend URL)

### 3.5 Deploy
1. Click **"Deploy"**
2. Wait 2-3 minutes for build
3. Once deployed, you'll see: **"Congratulations! 🎉"**
4. Click **"Visit"** to open your live app
5. Your URL: `https://your-project-name.vercel.app`

✅ **Frontend Deployed!**

---

## 🎉 Step 4: Test Your Deployment

### 4.1 Open Your App
1. Go to your Vercel URL: `https://your-project.vercel.app`
2. You should see the SentinelX AI dashboard

### 4.2 Test Features
- [ ] Dashboard loads with statistics
- [ ] Phishing Detector page opens
- [ ] OSINT Investigation page opens
- [ ] Threat Intelligence page opens
- [ ] Report Generator page opens
- [ ] Chat Assistant page opens

### 4.3 Test API Integration
1. Go to **Phishing Detector** page
2. Enter a test URL: `https://example.com`
3. Click **"Analyze"**
4. Should see analysis results

If you see results, **everything is working!** 🎉

---

## ⚠️ Important Notes

### Cold Starts (Render Free Tier)
- Your backend sleeps after 15 minutes of inactivity
- First request after sleep takes ~30 seconds to wake up
- Subsequent requests are instant

**Solution:** Use UptimeRobot (free) to ping every 14 minutes:
1. Go to https://uptimerobot.com
2. Sign up (free)
3. Add monitor: `https://sentinelx-backend.onrender.com/health`
4. Interval: 5 minutes

### MongoDB Free Tier
- 512 MB storage limit
- Sufficient for development and small production
- Monitor usage in MongoDB Atlas dashboard

### Vercel Free Tier
- Unlimited bandwidth for hobby projects
- No cold starts
- Automatic HTTPS and CDN

---

## 🔧 Troubleshooting

### Backend Issues

**Problem:** Backend URL returns 404
**Solution:** 
- Wait 10 minutes for initial deployment
- Check Render logs for errors
- Verify all environment variables are set

**Problem:** "Database connection failed"
**Solution:**
- Verify MongoDB URI is correct
- Check password has no special characters that need encoding
- Ensure IP whitelist includes 0.0.0.0/0

**Problem:** "IBM Watsonx authentication failed"
**Solution:**
- Verify API key and Project ID are correct
- Check Watsonx instance is active
- Ensure you have free trial credits

### Frontend Issues

**Problem:** "Failed to fetch" errors
**Solution:**
- Verify `REACT_APP_API_URL` is correct in Vercel
- Check backend is running (visit health endpoint)
- Clear browser cache and reload

**Problem:** Build fails on Vercel
**Solution:**
- Check build logs in Vercel dashboard
- Verify `frontend` root directory is set
- Try redeploying

---

## 📊 Your Free Stack

| Component | Platform | Tier | Cost |
|-----------|----------|------|------|
| Frontend | Vercel | Free | $0 |
| Backend | Render | Free | $0 |
| Database | MongoDB Atlas | M0 Free | $0 |
| APIs | Various | Free Tiers | $0 |
| **Total** | | | **$0/month** |

---

## 🚀 Next Steps

### 1. Custom Domain (Optional)
- Buy domain from Namecheap/GoDaddy (~$10/year)
- Add to Vercel: Settings → Domains
- Add to Render: Settings → Custom Domain

### 2. Keep Backend Awake
- Sign up for UptimeRobot (free)
- Add monitor for your backend
- Prevents cold starts

### 3. Monitor Your App
- Check Render logs regularly
- Monitor MongoDB Atlas usage
- Set up error alerts

### 4. Improve Performance
- Enable caching in backend
- Optimize images in frontend
- Use lazy loading for components

---

## 📞 Need Help?

### Documentation
- **Full Deployment Guide:** See `FREE_DEPLOYMENT_GUIDE.md`
- **Architecture:** See `ARCHITECTURE.md`
- **Technical Specs:** See `TECHNICAL_SPECS.md`

### Platform Support
- **Render:** https://render.com/docs
- **Vercel:** https://vercel.com/docs
- **MongoDB Atlas:** https://docs.atlas.mongodb.com

### Community
- **Render Community:** https://community.render.com
- **Vercel Discord:** https://vercel.com/discord
- **Stack Overflow:** Tag with platform names

---

## ✅ Deployment Checklist

- [ ] MongoDB Atlas cluster created
- [ ] Database user created
- [ ] Connection string saved
- [ ] All API keys obtained
- [ ] Backend deployed on Render
- [ ] Backend health check passes
- [ ] Frontend deployed on Vercel
- [ ] Frontend loads successfully
- [ ] All features tested
- [ ] UptimeRobot monitor set up (optional)

---

## 🎊 Congratulations!

Your SentinelX AI application is now live and accessible worldwide!

**Your URLs:**
- Frontend: `https://your-project.vercel.app`
- Backend: `https://sentinelx-backend.onrender.com`

**Share your project:**
- Add to portfolio
- Share on LinkedIn
- Demo to potential employers
- Show to friends and colleagues

---

**Total Setup Time:** ~15 minutes
**Total Cost:** $0/month
**Status:** ✅ Production Ready

**Last Updated:** 2026-05-02