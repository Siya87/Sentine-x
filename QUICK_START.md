# 🚀 SentinelX AI - Quick Start Guide

Get your SentinelX AI MVP up and running in under 30 minutes!

---

## ⚡ Prerequisites Checklist

Before you begin, ensure you have:

- [ ] **Python 3.11+** installed ([Download](https://www.python.org/downloads/))
- [ ] **Node.js 20+** installed ([Download](https://nodejs.org/))
- [ ] **MongoDB 6.0+** installed ([Download](https://www.mongodb.com/try/download/community))
- [ ] **Git** installed ([Download](https://git-scm.com/downloads))
- [ ] **API Keys** ready:
  - [ ] IBM Cloud API Key ([Get it](https://cloud.ibm.com/iam/apikeys))
  - [ ] VirusTotal API Key ([Get it](https://www.virustotal.com/gui/join-us))
  - [ ] AbuseIPDB API Key ([Get it](https://www.abuseipdb.com/register))
  - [ ] Shodan API Key ([Get it](https://account.shodan.io/register))
  - [ ] HaveIBeenPwned API Key (Optional - [Get it](https://haveibeenpwned.com/API/Key))

---

## 📦 Step 1: Project Setup (5 minutes)

### Create Project Structure

```bash
# Create main project directory
mkdir sentinelx-ai
cd sentinelx-ai

# Create backend structure
mkdir -p backend/app/{models,routes,services,integrations,database,utils,tests}

# Create frontend structure
mkdir frontend

# Create docs directory
mkdir docs
```

### Initialize Git Repository

```bash
git init
echo "venv/" > .gitignore
echo "node_modules/" >> .gitignore
echo ".env" >> .gitignore
echo "*.pyc" >> .gitignore
echo "__pycache__/" >> .gitignore
echo ".DS_Store" >> .gitignore
```

---

## 🐍 Step 2: Backend Setup (10 minutes)

### 2.1 Create Python Virtual Environment

```bash
cd backend
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 2.2 Create requirements.txt

```bash
cat > requirements.txt << 'EOF'
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0
motor==3.3.2
pymongo==4.6.0
python-multipart==0.0.6
python-dotenv==1.0.0
aiohttp==3.9.1
httpx==0.25.2
langchain==0.1.0
langchain-community==0.0.10
chromadb==0.4.18
sentence-transformers==2.2.2
reportlab==4.0.7
pillow==10.1.0
pdfplumber==0.10.3
beautifulsoup4==4.12.2
apscheduler==3.10.4
pytest==7.4.3
pytest-asyncio==0.21.1
black==23.12.0
EOF
```

### 2.3 Install Dependencies

```bash
pip install -r requirements.txt
```

### 2.4 Create Environment File

```bash
cat > .env << 'EOF'
# API Keys
VIRUSTOTAL_API_KEY=your_virustotal_key_here
ABUSEIPDB_API_KEY=your_abuseipdb_key_here
HIBP_API_KEY=your_hibp_key_here
SHODAN_API_KEY=your_shodan_key_here

# IBM Cloud
IBM_CLOUD_API_KEY=your_ibm_cloud_key_here
IBM_PROJECT_ID=your_ibm_project_id_here

# Database
MONGODB_URI=mongodb://localhost:27017/sentinelx

# App Config
DEBUG=True
LOG_LEVEL=INFO
EOF
```

**⚠️ IMPORTANT**: Replace all `your_*_key_here` placeholders with your actual API keys!

### 2.5 Create Basic Backend Structure

```bash
# Create __init__.py files
touch app/__init__.py
touch app/models/__init__.py
touch app/routes/__init__.py
touch app/services/__init__.py
touch app/integrations/__init__.py
touch app/database/__init__.py
touch app/utils/__init__.py
```

### 2.6 Create Main Application File

```bash
cat > app/main.py << 'EOF'
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="SentinelX AI",
    description="AI-Powered Cyber Investigation & Threat Intelligence Assistant",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "SentinelX AI API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
EOF
```

### 2.7 Test Backend

```bash
# Start the backend server
uvicorn app.main:app --reload

# In another terminal, test the API
curl http://localhost:8000/health
# Expected: {"status":"healthy"}
```

---

## ⚛️ Step 3: Frontend Setup (10 minutes)

### 3.1 Create React App with Vite

```bash
cd ../frontend
npm create vite@latest . -- --template react
```

### 3.2 Install Dependencies

```bash
npm install react-router-dom axios zustand framer-motion recharts react-flow-renderer leaflet react-leaflet react-dropzone react-markdown date-fns clsx lucide-react
```

### 3.3 Install Dev Dependencies

```bash
npm install -D tailwindcss autoprefixer postcss
npx tailwindcss init -p
```

### 3.4 Configure Tailwind CSS

```bash
cat > tailwind.config.js << 'EOF'
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f0f9ff',
          500: '#0ea5e9',
          600: '#0284c7',
          700: '#0369a1',
        },
      },
    },
  },
  plugins: [],
}
EOF
```

### 3.5 Update CSS

```bash
cat > src/index.css << 'EOF'
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
EOF
```

### 3.6 Create Environment File

```bash
cat > .env << 'EOF'
VITE_API_URL=http://localhost:8000
EOF
```

### 3.7 Create Basic App Structure

```bash
cat > src/App.jsx << 'EOF'
import { useState } from 'react'

function App() {
  const [message, setMessage] = useState('')

  const testAPI = async () => {
    try {
      const response = await fetch('http://localhost:8000/health')
      const data = await response.json()
      setMessage(`API Status: ${data.status}`)
    } catch (error) {
      setMessage('API connection failed')
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-primary-600 mb-4">
          🛡️ SentinelX AI
        </h1>
        <p className="text-gray-600 mb-8">
          AI-Powered Cyber Investigation Platform
        </p>
        <button
          onClick={testAPI}
          className="bg-primary-600 text-white px-6 py-3 rounded-lg hover:bg-primary-700 transition"
        >
          Test API Connection
        </button>
        {message && (
          <p className="mt-4 text-lg font-semibold text-green-600">
            {message}
          </p>
        )}
      </div>
    </div>
  )
}

export default App
EOF
```

### 3.8 Test Frontend

```bash
# Start the development server
npm run dev

# Open browser to http://localhost:5173
# Click "Test API Connection" button
# Should see "API Status: healthy"
```

---

## 🗄️ Step 4: Database Setup (5 minutes)

### 4.1 Start MongoDB

```bash
# On Windows (if installed as service):
net start MongoDB

# On macOS (with Homebrew):
brew services start mongodb-community

# On Linux:
sudo systemctl start mongod

# Or run manually:
mongod --dbpath /path/to/data/directory
```

### 4.2 Verify MongoDB Connection

```bash
# Connect to MongoDB shell
mongosh

# Create database
use sentinelx

# Create a test collection
db.test.insertOne({message: "SentinelX AI is ready!"})

# Verify
db.test.find()

# Exit
exit
```

---

## ✅ Step 5: Verification (2 minutes)

### Check All Services

1. **Backend**: http://localhost:8000/docs
   - Should see FastAPI Swagger documentation
   
2. **Frontend**: http://localhost:5173
   - Should see SentinelX AI landing page
   - Click "Test API Connection" - should succeed
   
3. **MongoDB**: 
   ```bash
   mongosh --eval "db.adminCommand('ping')"
   ```
   - Should return `{ ok: 1 }`

---

## 🎯 Next Steps

Now that your environment is set up, you're ready to start building! Follow these guides in order:

1. **[Implementation Guide](IMPLEMENTATION_GUIDE.md)** - Detailed step-by-step implementation
2. **[Architecture Guide](ARCHITECTURE.md)** - Understand the system design
3. **[Technical Specs](TECHNICAL_SPECS.md)** - Deep dive into technical details
4. **[Project Timeline](PROJECT_TIMELINE.md)** - Track your progress

---

## 🐛 Troubleshooting

### Backend Issues

**Problem**: `ModuleNotFoundError: No module named 'fastapi'`
```bash
# Solution: Ensure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

**Problem**: `Connection refused` when accessing API
```bash
# Solution: Check if backend is running
ps aux | grep uvicorn  # macOS/Linux
tasklist | findstr uvicorn  # Windows

# Restart backend
uvicorn app.main:app --reload
```

### Frontend Issues

**Problem**: `npm ERR! code ENOENT`
```bash
# Solution: Ensure you're in the frontend directory
cd frontend
npm install
```

**Problem**: Tailwind styles not working
```bash
# Solution: Rebuild the project
npm run build
npm run dev
```

### Database Issues

**Problem**: `MongoServerError: connect ECONNREFUSED`
```bash
# Solution: Start MongoDB
# Windows:
net start MongoDB

# macOS:
brew services start mongodb-community

# Linux:
sudo systemctl start mongod
```

**Problem**: `Authentication failed`
```bash
# Solution: Check MongoDB URI in .env
# Default should be: mongodb://localhost:27017/sentinelx
```

---

## 📚 Useful Commands

### Backend Commands
```bash
# Start backend
uvicorn app.main:app --reload

# Run tests
pytest tests/ -v

# Format code
black app/

# Check code quality
flake8 app/
```

### Frontend Commands
```bash
# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Run linter
npm run lint
```

### Database Commands
```bash
# Connect to MongoDB
mongosh

# Show databases
show dbs

# Use SentinelX database
use sentinelx

# Show collections
show collections

# Query collection
db.collection_name.find()
```

---

## 🎓 Learning Resources

- **FastAPI Tutorial**: https://fastapi.tiangolo.com/tutorial/
- **React Documentation**: https://react.dev/learn
- **MongoDB University**: https://university.mongodb.com/
- **IBM Granite Models**: https://www.ibm.com/products/watsonx-ai
- **Tailwind CSS**: https://tailwindcss.com/docs

---

## 💡 Pro Tips

1. **Use VS Code Extensions**:
   - Python
   - Pylance
   - ES7+ React/Redux/React-Native snippets
   - Tailwind CSS IntelliSense
   - MongoDB for VS Code

2. **Keep Services Running**:
   - Use separate terminal windows for backend, frontend, and MongoDB
   - Consider using `tmux` or `screen` for session management

3. **Version Control**:
   - Commit frequently with meaningful messages
   - Create branches for new features
   - Never commit `.env` files

4. **API Testing**:
   - Use Postman or Thunder Client for API testing
   - FastAPI provides built-in Swagger UI at `/docs`

5. **Hot Reload**:
   - Both backend (`--reload`) and frontend (`npm run dev`) support hot reload
   - Changes will reflect automatically

---

## 🎉 You're Ready!

Your development environment is now fully set up! You have:

✅ Backend running on http://localhost:8000  
✅ Frontend running on http://localhost:5173  
✅ MongoDB running and connected  
✅ All dependencies installed  
✅ API connection verified  

**Time to start building! 🚀**

Proceed to the [Implementation Guide](IMPLEMENTATION_GUIDE.md) to begin developing the features.

---

<div align="center">

**Need Help?** Check the [Troubleshooting](#-troubleshooting) section or refer to the [Technical Specs](TECHNICAL_SPECS.md)

[← Back to README](README.md) | [Start Building →](IMPLEMENTATION_GUIDE.md)

</div>