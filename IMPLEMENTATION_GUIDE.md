# SentinelX AI - Implementation Guide

## Week-by-Week Implementation Plan

This guide provides a detailed, step-by-step approach to building SentinelX AI MVP in 2-3 weeks.

---

## Week 1: Foundation & Core Setup

### Day 1-2: Project Initialization

#### Backend Setup
```bash
# Create project structure
mkdir sentinelx-ai
cd sentinelx-ai
mkdir -p backend/app/{models,routes,services,integrations,database,utils}
mkdir -p backend/tests

# Initialize Python environment
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Create requirements.txt
cat > requirements.txt << EOF
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

# Install dependencies
pip install -r requirements.txt
```

#### Frontend Setup
```bash
# Create React app with Vite
cd ..
npm create vite@latest frontend -- --template react
cd frontend

# Install dependencies
npm install react-router-dom axios zustand framer-motion recharts react-flow-renderer leaflet react-leaflet react-dropzone react-markdown date-fns clsx lucide-react

# Install dev dependencies
npm install -D tailwindcss autoprefixer postcss

# Initialize Tailwind
npx tailwindcss init -p
```

#### Environment Configuration
```bash
# Backend .env
cd ../backend
cat > .env << EOF
# API Keys
VIRUSTOTAL_API_KEY=your_key_here
ABUSEIPDB_API_KEY=your_key_here
HIBP_API_KEY=your_key_here
SHODAN_API_KEY=your_key_here

# IBM Cloud
IBM_CLOUD_API_KEY=your_key_here
IBM_PROJECT_ID=your_project_id_here

# Database
MONGODB_URI=mongodb://localhost:27017/sentinelx

# App Config
DEBUG=True
LOG_LEVEL=INFO
EOF

# Frontend .env
cd ../frontend
cat > .env << EOF
VITE_API_URL=http://localhost:8000
EOF
```

---

### Day 3-4: Backend Core Structure

#### 1. Create Main Application (`backend/app/main.py`)
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import phishing, osint, threat_intel, reports, chat
from app.database.mongodb import connect_to_mongo, close_mongo_connection
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="SentinelX AI",
    description="AI-Powered Cyber Investigation & Threat Intelligence Assistant",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Events
@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()
    logger.info("Application started")

@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection()
    logger.info("Application shutdown")

# Routes
app.include_router(phishing.router, prefix="/api/phishing", tags=["Phishing"])
app.include_router(osint.router, prefix="/api/osint", tags=["OSINT"])
app.include_router(threat_intel.router, prefix="/api/threats", tags=["Threats"])
app.include_router(reports.router, prefix="/api/reports", tags=["Reports"])
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])

@app.get("/")
async def root():
    return {"message": "SentinelX AI API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

#### 2. Configuration Management (`backend/app/config.py`)
```python
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # API Keys
    virustotal_api_key: str
    abuseipdb_api_key: str
    hibp_api_key: str = ""
    shodan_api_key: str
    
    # IBM Cloud
    ibm_cloud_api_key: str
    ibm_project_id: str
    
    # Database
    mongodb_uri: str
    
    # App Config
    debug: bool = False
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

@lru_cache()
def get_settings():
    return Settings()
```

#### 3. Database Connection (`backend/app/database/mongodb.py`)
```python
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import get_settings
import logging

logger = logging.getLogger(__name__)
settings = get_settings()

class Database:
    client: AsyncIOMotorClient = None
    db = None

db = Database()

async def connect_to_mongo():
    logger.info("Connecting to MongoDB...")
    db.client = AsyncIOMotorClient(settings.mongodb_uri)
    db.db = db.client.sentinelx
    logger.info("Connected to MongoDB")

async def close_mongo_connection():
    logger.info("Closing MongoDB connection...")
    db.client.close()
    logger.info("MongoDB connection closed")

def get_database():
    return db.db
```

---

### Day 5-7: Frontend Core Structure

#### 1. Setup Routing (`frontend/src/App.jsx`)
```javascript
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { Suspense, lazy } from 'react'
import Layout from './components/Layout'
import Loader from './components/common/Loader'

const Home = lazy(() => import('./pages/Home'))
const PhishingPage = lazy(() => import('./pages/PhishingPage'))
const OSINTPage = lazy(() => import('./pages/OSINTPage'))
const DashboardPage = lazy(() => import('./pages/DashboardPage'))
const ReportsPage = lazy(() => import('./pages/ReportsPage'))
const ChatPage = lazy(() => import('./pages/ChatPage'))

function App() {
  return (
    <BrowserRouter>
      <Suspense fallback={<Loader />}>
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route index element={<Home />} />
            <Route path="phishing" element={<PhishingPage />} />
            <Route path="osint" element={<OSINTPage />} />
            <Route path="dashboard" element={<DashboardPage />} />
            <Route path="reports" element={<ReportsPage />} />
            <Route path="chat" element={<ChatPage />} />
          </Route>
        </Routes>
      </Suspense>
    </BrowserRouter>
  )
}

export default App
```

#### 2. API Client (`frontend/src/services/api.js`)
```javascript
import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor
api.interceptors.request.use(
  config => {
    // Add auth token if available
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => Promise.reject(error)
)

// Response interceptor
api.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 429) {
      console.error('Rate limit exceeded')
    }
    return Promise.reject(error)
  }
)

export default api
```

#### 3. Tailwind Configuration (`frontend/tailwind.config.js`)
```javascript
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
        danger: {
          500: '#ef4444',
          600: '#dc2626',
        },
        success: {
          500: '#10b981',
          600: '#059669',
        },
      },
    },
  },
  plugins: [],
}
```

---

## Week 2: Core Features Implementation

### Day 8-10: Phishing Detector & OSINT Investigation

#### Phishing Detector Backend

**1. Models (`backend/app/models/phishing.py`)**
```python
from pydantic import BaseModel, validator
from typing import Optional, List, Dict
from datetime import datetime

class PhishingAnalysisRequest(BaseModel):
    content_type: str  # email, url, sms, file
    content: str
    sender: Optional[str] = None
    metadata: Optional[Dict] = None
    
    @validator('content_type')
    def validate_content_type(cls, v):
        allowed = ['email', 'url', 'sms', 'file']
        if v not in allowed:
            raise ValueError(f'content_type must be one of {allowed}')
        return v

class PhishingIndicator(BaseModel):
    type: str
    description: str
    severity: str

class PhishingAnalysisResponse(BaseModel):
    analysis_id: str
    threat_score: int
    is_phishing: bool
    confidence: int
    indicators: List[PhishingIndicator]
    explanation: str
    recommendations: List[str]
    virustotal_results: Optional[Dict] = None
    created_at: datetime
```

**2. Service (`backend/app/services/phishing_service.py`)**
```python
import uuid
from datetime import datetime
from app.integrations.virustotal import VirusTotalClient
from app.services.ai_service import AIService
from app.database.mongodb import get_database
import logging

logger = logging.getLogger(__name__)

class PhishingService:
    def __init__(self):
        self.vt_client = VirusTotalClient()
        self.ai_service = AIService()
    
    async def analyze(self, request: dict) -> dict:
        analysis_id = str(uuid.uuid4())
        logger.info(f"Starting phishing analysis: {analysis_id}")
        
        # Extract URLs from content
        urls = self._extract_urls(request['content'])
        
        # Check with VirusTotal
        vt_results = None
        if urls:
            vt_results = await self.vt_client.check_urls(urls)
        
        # AI Analysis
        ai_analysis = await self.ai_service.analyze_phishing({
            'content': request['content'],
            'content_type': request['content_type'],
            'urls': urls,
            'vt_results': vt_results
        })
        
        # Store in database
        db = get_database()
        analysis_doc = {
            'analysis_id': analysis_id,
            'content_type': request['content_type'],
            'content': request['content'],
            'urls_found': urls,
            'virustotal_results': vt_results,
            'ai_analysis': ai_analysis,
            'created_at': datetime.utcnow()
        }
        await db.phishing_analyses.insert_one(analysis_doc)
        
        return {
            'analysis_id': analysis_id,
            **ai_analysis,
            'virustotal_results': vt_results,
            'created_at': datetime.utcnow()
        }
    
    def _extract_urls(self, content: str) -> list:
        import re
        url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
        return re.findall(url_pattern, content)
```

**3. Routes (`backend/app/routes/phishing.py`)**
```python
from fastapi import APIRouter, HTTPException
from app.models.phishing import PhishingAnalysisRequest, PhishingAnalysisResponse
from app.services.phishing_service import PhishingService

router = APIRouter()
service = PhishingService()

@router.post("/analyze", response_model=PhishingAnalysisResponse)
async def analyze_phishing(request: PhishingAnalysisRequest):
    try:
        result = await service.analyze(request.dict())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history")
async def get_history(limit: int = 10):
    # Implementation
    pass

@router.get("/{analysis_id}")
async def get_analysis(analysis_id: str):
    # Implementation
    pass
```

#### Phishing Detector Frontend

**Component (`frontend/src/components/phishing/PhishingDetector.jsx`)**
```javascript
import { useState } from 'react'
import { motion } from 'framer-motion'
import api from '../../services/api'
import ThreatScore from './ThreatScore'
import UploadZone from './UploadZone'

export default function PhishingDetector() {
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [contentType, setContentType] = useState('email')
  const [content, setContent] = useState('')

  const handleAnalyze = async () => {
    setLoading(true)
    try {
      const response = await api.post('/api/phishing/analyze', {
        content_type: contentType,
        content: content
      })
      setResult(response.data)
    } catch (error) {
      console.error('Analysis failed:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-4xl mx-auto p-6">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-white rounded-lg shadow-lg p-6"
      >
        <h2 className="text-2xl font-bold mb-6">AI Phishing Detector</h2>
        
        <div className="mb-4">
          <label className="block text-sm font-medium mb-2">Content Type</label>
          <select
            value={contentType}
            onChange={(e) => setContentType(e.target.value)}
            className="w-full p-2 border rounded"
          >
            <option value="email">Email</option>
            <option value="url">URL</option>
            <option value="sms">SMS</option>
            <option value="file">File</option>
          </select>
        </div>

        <div className="mb-4">
          <label className="block text-sm font-medium mb-2">Content</label>
          <textarea
            value={content}
            onChange={(e) => setContent(e.target.value)}
            className="w-full p-2 border rounded h-32"
            placeholder="Paste email content, URL, or SMS text..."
          />
        </div>

        <button
          onClick={handleAnalyze}
          disabled={loading || !content}
          className="w-full bg-primary-600 text-white py-2 rounded hover:bg-primary-700 disabled:opacity-50"
        >
          {loading ? 'Analyzing...' : 'Analyze'}
        </button>

        {result && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="mt-6"
          >
            <ThreatScore score={result.threat_score} />
            
            <div className="mt-4">
              <h3 className="font-semibold mb-2">Indicators Found:</h3>
              <ul className="space-y-2">
                {result.indicators.map((indicator, idx) => (
                  <li key={idx} className="flex items-start">
                    <span className={`px-2 py-1 rounded text-xs mr-2 ${
                      indicator.severity === 'critical' ? 'bg-red-100 text-red-800' :
                      indicator.severity === 'high' ? 'bg-orange-100 text-orange-800' :
                      'bg-yellow-100 text-yellow-800'
                    }`}>
                      {indicator.severity}
                    </span>
                    <span>{indicator.description}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div className="mt-4">
              <h3 className="font-semibold mb-2">Recommendations:</h3>
              <ul className="list-disc list-inside space-y-1">
                {result.recommendations.map((rec, idx) => (
                  <li key={idx}>{rec}</li>
                ))}
              </ul>
            </div>
          </motion.div>
        )}
      </motion.div>
    </div>
  )
}
```

---

### Day 11-12: Threat Intelligence Dashboard

#### Backend Implementation

**Service (`backend/app/services/threat_service.py`)**
```python
from app.integrations.shodan import ShodanClient
from app.integrations.virustotal import VirusTotalClient
from app.database.mongodb import get_database
from datetime import datetime, timedelta
import asyncio

class ThreatIntelligenceService:
    def __init__(self):
        self.shodan = ShodanClient()
        self.vt = VirusTotalClient()
    
    async def get_dashboard_data(self):
        # Fetch recent threats
        db = get_database()
        recent_threats = await db.threat_intelligence.find(
            {'timestamp': {'$gte': datetime.utcnow() - timedelta(days=7)}}
        ).sort('timestamp', -1).limit(100).to_list(100)
        
        # Aggregate statistics
        stats = await self._calculate_stats(recent_threats)
        
        return {
            'threats': recent_threats,
            'stats': stats,
            'trends': await self._calculate_trends(),
            'heatmap_data': await self._get_heatmap_data()
        }
    
    async def _calculate_stats(self, threats):
        # Calculate threat statistics
        return {
            'total_threats': len(threats),
            'critical': len([t for t in threats if t['severity'] == 'critical']),
            'high': len([t for t in threats if t['severity'] == 'high']),
            'medium': len([t for t in threats if t['severity'] == 'medium']),
            'low': len([t for t in threats if t['severity'] == 'low'])
        }
```

#### Frontend Dashboard

**Component (`frontend/src/components/dashboard/ThreatDashboard.jsx`)**
```javascript
import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts'
import api from '../../services/api'
import AttackHeatmap from './AttackHeatmap'
import StatCards from './StatCards'

export default function ThreatDashboard() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchDashboardData()
    const interval = setInterval(fetchDashboardData, 30000) // Refresh every 30s
    return () => clearInterval(interval)
  }, [])

  const fetchDashboardData = async () => {
    try {
      const response = await api.get('/api/threats/dashboard')
      setData(response.data)
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) return <div>Loading...</div>

  return (
    <div className="p-6 space-y-6">
      <h1 className="text-3xl font-bold">Threat Intelligence Dashboard</h1>
      
      <StatCards stats={data.stats} />
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white p-6 rounded-lg shadow"
        >
          <h2 className="text-xl font-semibold mb-4">Threat Trends</h2>
          <LineChart width={500} height={300} data={data.trends}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="threats" stroke="#0ea5e9" />
          </LineChart>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="bg-white p-6 rounded-lg shadow"
        >
          <h2 className="text-xl font-semibold mb-4">Threat Types</h2>
          <BarChart width={500} height={300} data={data.threat_types}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="type" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="count" fill="#0ea5e9" />
          </BarChart>
        </motion.div>
      </div>

      <AttackHeatmap data={data.heatmap_data} />
    </div>
  )
}
```

---

### Day 13-14: Report Generator & Chat Assistant

#### Report Generator Backend

**Service (`backend/app/services/report_service.py`)**
```python
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from app.services.ai_service import AIService
import uuid
from datetime import datetime

class ReportService:
    def __init__(self):
        self.ai_service = AIService()
    
    async def generate_report(self, incident_data: dict) -> dict:
        report_id = str(uuid.uuid4())
        
        # Generate report content with AI
        report_content = await self.ai_service.generate_incident_report(incident_data)
        
        # Generate PDF
        pdf_path = f"reports/{report_id}.pdf"
        self._create_pdf(report_content, pdf_path)
        
        # Store in database
        # ... implementation
        
        return {
            'report_id': report_id,
            'content': report_content,
            'pdf_url': pdf_path,
            'created_at': datetime.utcnow()
        }
    
    def _create_pdf(self, content: dict, path: str):
        doc = SimpleDocTemplate(path, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        # Add content sections
        story.append(Paragraph(content['title'], styles['Title']))
        story.append(Spacer(1, 12))
        story.append(Paragraph(content['executive_summary'], styles['Normal']))
        # ... add more sections
        
        doc.build(story)
```

#### Chat Assistant Backend

**Service (`backend/app/services/chat_service.py`)**
```python
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from app.services.ai_service import AIService
import uuid

class ChatService:
    def __init__(self):
        self.ai_service = AIService()
        self.sessions = {}
    
    async def send_message(self, session_id: str, message: str) -> dict:
        if session_id not in self.sessions:
            session_id = str(uuid.uuid4())
            self.sessions[session_id] = {
                'messages': [],
                'memory': ConversationBufferMemory()
            }
        
        # Get response from AI
        response = await self.ai_service.chat(
            message=message,
            history=self.sessions[session_id]['messages']
        )
        
        # Store message
        self.sessions[session_id]['messages'].extend([
            {'role': 'user', 'content': message},
            {'role': 'assistant', 'content': response}
        ])
        
        return {
            'session_id': session_id,
            'response': response
        }
```

---

## Week 3: Polish, Testing & Documentation

### Day 15-17: Integration Testing

**Test Suite (`backend/tests/test_integration.py`)**
```python
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_phishing_analysis_flow():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/phishing/analyze", json={
            "content_type": "email",
            "content": "Urgent: Your account will be suspended..."
        })
        assert response.status_code == 200
        data = response.json()
        assert "analysis_id" in data
        assert data["threat_score"] > 0

@pytest.mark.asyncio
async def test_osint_investigation_flow():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/osint/investigate", json={
            "target": "test@example.com",
            "target_type": "email"
        })
        assert response.status_code == 200
```

### Day 18-19: UI/UX Polish

- Add loading states and animations
- Implement error boundaries
- Add toast notifications
- Improve responsive design
- Add dark mode support (optional)

### Day 20-21: Documentation & Demo

**Create README.md**
```markdown
# SentinelX AI

AI-Powered Cyber Investigation & Threat Intelligence Assistant

## Features
- AI Phishing Detector
- OSINT Investigation Agent
- Threat Intelligence Dashboard
- AI Incident Report Generator
- AI Chat Assistant

## Quick Start

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Demo Scenarios
1. Phishing Email Analysis
2. OSINT Investigation
3. Threat Dashboard Monitoring
4. Incident Report Generation
5. Chat Assistant Queries
```

---

## Deployment Checklist

- [ ] All features implemented and tested
- [ ] API documentation complete
- [ ] Environment variables configured
- [ ] Database indexes created
- [ ] Error handling implemented
- [ ] Logging configured
- [ ] Performance optimized
- [ ] Security review completed
- [ ] Demo scenarios prepared
- [ ] User documentation written

---

## Success Criteria

✅ All 5 features working end-to-end
✅ Real API integrations functional
✅ IBM Granite responses accurate and relevant
✅ UI is intuitive and responsive
✅ API response times < 3 seconds
✅ Dashboard loads < 2 seconds
✅ Chat responses < 5 seconds
✅ No critical bugs
✅ Code is well-documented
✅ Demo is impressive and smooth

---

This implementation guide provides a clear path to building SentinelX AI MVP. Follow the steps sequentially, test thoroughly, and iterate based on feedback.