# SentinelX AI - Technical Specifications

## Technology Stack Details

### Backend Stack

#### Core Framework
- **FastAPI 0.104+**
  - Async/await support for concurrent API calls
  - Automatic OpenAPI documentation
  - Pydantic validation
  - WebSocket support for real-time features

#### AI & ML
- **IBM Granite Models**
  - granite-13b-instruct-v2 for analysis
  - granite-20b-code-instruct for technical queries
- **IBM Bob** for AI orchestration
- **LangChain 0.1+** for RAG pipeline
- **ChromaDB** for vector storage
- **Sentence Transformers** for embeddings

#### External API Clients
- **VirusTotal API v3**
  - File scanning
  - URL analysis
  - Domain reputation
- **AbuseIPDB API v2**
  - IP reputation checks
  - Threat intelligence
- **HaveIBeenPwned API v3**
  - Breach data lookup
  - Password exposure checks
- **Shodan API**
  - Internet-wide scanning data
  - Vulnerability intelligence

#### Database
- **MongoDB 6.0+**
  - Document-based storage
  - Flexible schema
  - Aggregation pipeline
  - Time-series collections for threat data

#### Additional Libraries
```python
# requirements.txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0
motor==3.3.2  # Async MongoDB driver
pymongo==4.6.0
python-multipart==0.0.6
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-dotenv==1.0.0
aiohttp==3.9.1
httpx==0.25.2
langchain==0.1.0
langchain-community==0.0.10
chromadb==0.4.18
sentence-transformers==2.2.2
reportlab==4.0.7
weasyprint==60.1
pillow==10.1.0
python-magic==0.4.27
pdfplumber==0.10.3
beautifulsoup4==4.12.2
lxml==4.9.3
apscheduler==3.10.4
redis==5.0.1
celery==5.3.4
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0
black==23.12.0
flake8==6.1.0
mypy==1.7.1
```

---

### Frontend Stack

#### Core Framework
- **React 18.2+**
  - Hooks-based architecture
  - Concurrent rendering
  - Suspense for data fetching
- **Vite 5.0+** for build tooling
- **React Router 6.20+** for navigation

#### Styling & Animation
- **Tailwind CSS 3.3+**
  - Utility-first CSS
  - Custom design system
  - Dark mode support
- **Framer Motion 10.16+**
  - Page transitions
  - Component animations
  - Gesture handling

#### Data Visualization
- **Recharts 2.10+**
  - Line charts for trends
  - Bar charts for comparisons
  - Pie charts for distributions
- **React Flow 11.10+**
  - Relationship graphs
  - Network diagrams
- **Leaflet 1.9+** with React-Leaflet
  - Geographic heatmaps
  - Threat location mapping

#### State Management
- **Zustand 4.4+**
  - Lightweight state management
  - No boilerplate
  - DevTools support

#### HTTP Client
- **Axios 1.6+**
  - Request/response interceptors
  - Automatic retries
  - Progress tracking

#### Additional Libraries
```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.0",
    "axios": "^1.6.2",
    "zustand": "^4.4.7",
    "framer-motion": "^10.16.16",
    "recharts": "^2.10.3",
    "react-flow-renderer": "^11.10.1",
    "leaflet": "^1.9.4",
    "react-leaflet": "^4.2.1",
    "react-dropzone": "^14.2.3",
    "react-markdown": "^9.0.1",
    "react-syntax-highlighter": "^15.5.0",
    "date-fns": "^2.30.0",
    "clsx": "^2.0.0",
    "lucide-react": "^0.294.0"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.2.1",
    "vite": "^5.0.8",
    "tailwindcss": "^3.3.6",
    "autoprefixer": "^10.4.16",
    "postcss": "^8.4.32",
    "eslint": "^8.55.0",
    "eslint-plugin-react": "^7.33.2",
    "prettier": "^3.1.1"
  }
}
```

---

## API Integration Specifications

### 1. VirusTotal API

**Base URL:** `https://www.virustotal.com/api/v3`

**Endpoints Used:**
```python
# File scanning
POST /files
GET /files/{id}

# URL analysis
POST /urls
GET /urls/{id}

# Domain reputation
GET /domains/{domain}

# IP address info
GET /ip_addresses/{ip}
```

**Rate Limits:**
- Free tier: 4 requests/minute
- Premium: 1000 requests/day

**Implementation Strategy:**
```python
class VirusTotalClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://www.virustotal.com/api/v3"
        self.session = aiohttp.ClientSession()
    
    async def scan_url(self, url: str) -> dict:
        # Implement with rate limiting and caching
        pass
    
    async def get_file_report(self, file_hash: str) -> dict:
        # Implement with error handling
        pass
```

---

### 2. AbuseIPDB API

**Base URL:** `https://api.abuseipdb.com/api/v2`

**Endpoints Used:**
```python
# Check IP reputation
GET /check?ipAddress={ip}

# Report IP
POST /report

# Get blacklist
GET /blacklist
```

**Rate Limits:**
- Free tier: 1000 requests/day
- Premium: 100,000 requests/day

**Implementation Strategy:**
```python
class AbuseIPDBClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.abuseipdb.com/api/v2"
    
    async def check_ip(self, ip: str) -> dict:
        # Return abuse confidence score
        pass
```

---

### 3. HaveIBeenPwned API

**Base URL:** `https://haveibeenpwned.com/api/v3`

**Endpoints Used:**
```python
# Check breached account
GET /breachedaccount/{account}

# Get all breaches
GET /breaches

# Check password
GET /range/{hash_prefix}
```

**Rate Limits:**
- Free tier: 1 request every 1.5 seconds
- Requires User-Agent header

**Implementation Strategy:**
```python
class HIBPClient:
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.base_url = "https://haveibeenpwned.com/api/v3"
    
    async def check_email(self, email: str) -> list:
        # Return list of breaches
        pass
    
    async def check_password(self, password: str) -> int:
        # Return number of times seen in breaches
        pass
```

---

### 4. Shodan API

**Base URL:** `https://api.shodan.io`

**Endpoints Used:**
```python
# Search
GET /shodan/host/search?query={query}

# Host information
GET /shodan/host/{ip}

# DNS lookup
GET /dns/resolve?hostnames={hostnames}

# Exploits
GET /api/search?query={query}
```

**Rate Limits:**
- Free tier: 1 query credit/month
- Premium: 100 query credits/month

**Implementation Strategy:**
```python
class ShodanClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.shodan.io"
    
    async def search(self, query: str) -> dict:
        # Search for hosts
        pass
    
    async def get_host_info(self, ip: str) -> dict:
        # Get detailed host information
        pass
```

---

## IBM Granite Integration

### Model Configuration

```python
from ibm_watson_machine_learning.foundation_models import Model

# Initialize Granite model
granite_model = Model(
    model_id="ibm/granite-13b-instruct-v2",
    credentials={
        "url": "https://us-south.ml.cloud.ibm.com",
        "apikey": os.getenv("IBM_CLOUD_API_KEY")
    },
    project_id=os.getenv("IBM_PROJECT_ID"),
    params={
        "decoding_method": "greedy",
        "max_new_tokens": 1000,
        "temperature": 0.7,
        "top_p": 0.9,
        "repetition_penalty": 1.1
    }
)
```

### Prompt Engineering Templates

#### 1. Phishing Analysis Prompt
```python
PHISHING_ANALYSIS_PROMPT = """You are a cybersecurity expert specializing in phishing detection.

Analyze the following content for phishing indicators:

Content Type: {content_type}
Content: {content}
Sender: {sender}
URLs Found: {urls}
VirusTotal Results: {vt_results}

Provide a detailed analysis in JSON format:
{{
  "threat_score": <0-100>,
  "is_phishing": <true/false>,
  "confidence": <0-100>,
  "indicators": [
    {{
      "type": "urgency|spoofing|suspicious_link|grammar|etc",
      "description": "detailed explanation",
      "severity": "low|medium|high|critical"
    }}
  ],
  "explanation": "comprehensive analysis",
  "recommendations": [
    "specific action items"
  ]
}}

Be thorough and precise in your analysis."""
```

#### 2. OSINT Summary Prompt
```python
OSINT_SUMMARY_PROMPT = """You are an OSINT analyst creating an investigation summary.

Target Information:
- Target: {target}
- Type: {target_type}

Data Collected:
- Breach Data: {breach_data}
- IP Reputation: {ip_reputation}
- Social Profiles: {social_profiles}
- Additional Data: {additional_data}

Create a comprehensive investigation summary in JSON format:
{{
  "risk_score": <0-100>,
  "risk_level": "low|medium|high|critical",
  "summary": "executive summary of findings",
  "key_findings": [
    "finding 1",
    "finding 2"
  ],
  "threats_identified": [
    {{
      "threat": "description",
      "severity": "low|medium|high|critical",
      "evidence": "supporting evidence"
    }}
  ],
  "recommendations": [
    "actionable recommendations"
  ],
  "timeline": [
    {{
      "date": "YYYY-MM-DD",
      "event": "description"
    }}
  ]
}}

Be objective and evidence-based."""
```

#### 3. Incident Report Prompt
```python
INCIDENT_REPORT_PROMPT = """You are a SOC analyst writing a professional incident report.

Incident Details:
- Type: {incident_type}
- Severity: {severity}
- Date: {date}
- Description: {description}
- Systems Affected: {systems}
- Timeline: {timeline}

Generate a comprehensive incident report with the following sections:

1. EXECUTIVE SUMMARY
   - Brief overview for management
   - Impact assessment
   - Current status

2. INCIDENT DETAILS
   - What happened
   - When it was detected
   - How it was discovered

3. TIMELINE
   - Chronological sequence of events
   - Key timestamps

4. ATTACK VECTOR
   - How the attack occurred
   - Entry points
   - Techniques used (MITRE ATT&CK)

5. AFFECTED SYSTEMS
   - List of impacted systems
   - Data exposure assessment

6. RESPONSE ACTIONS
   - Immediate actions taken
   - Containment measures

7. MITIGATION STEPS
   - Short-term fixes
   - Long-term improvements

8. RECOMMENDATIONS
   - Security improvements
   - Policy changes
   - Training needs

Format as structured text suitable for PDF generation."""
```

#### 4. Chat Assistant Prompt
```python
CHAT_ASSISTANT_PROMPT = """You are SentinelX AI, an expert cybersecurity assistant.

Context from knowledge base:
{context}

Conversation history:
{history}

User question: {question}

Provide a clear, accurate, and helpful response. If the question is about:
- Threats: Explain the threat, its impact, and mitigation
- Tools: Describe functionality and best practices
- Techniques: Reference MITRE ATT&CK when relevant
- Analysis: Provide step-by-step reasoning

Be concise but thorough. Use technical terms appropriately but explain them when needed."""
```

---

## Database Schema Design

### MongoDB Collections

#### 1. phishing_analyses
```javascript
{
  _id: ObjectId,
  analysis_id: String (UUID),
  content_type: String, // "email", "url", "sms", "file"
  content: {
    raw: String,
    parsed: Object,
    metadata: Object
  },
  sender: {
    email: String,
    name: String,
    ip: String
  },
  urls_found: Array,
  attachments: Array,
  virustotal_results: {
    scan_id: String,
    positives: Number,
    total: Number,
    permalink: String,
    results: Object
  },
  ai_analysis: {
    threat_score: Number,
    is_phishing: Boolean,
    confidence: Number,
    indicators: Array,
    explanation: String,
    recommendations: Array
  },
  status: String, // "pending", "completed", "failed"
  created_at: Date,
  updated_at: Date,
  user_id: String (optional)
}

// Indexes
db.phishing_analyses.createIndex({ analysis_id: 1 }, { unique: true })
db.phishing_analyses.createIndex({ created_at: -1 })
db.phishing_analyses.createIndex({ "ai_analysis.threat_score": -1 })
```

#### 2. osint_investigations
```javascript
{
  _id: ObjectId,
  investigation_id: String (UUID),
  target: String,
  target_type: String, // "username", "email", "phone", "domain", "ip"
  data_sources: {
    hibp: {
      breaches: Array,
      pastes: Array,
      last_checked: Date
    },
    abuseipdb: {
      abuse_confidence_score: Number,
      reports: Array,
      last_checked: Date
    },
    shodan: {
      host_info: Object,
      vulnerabilities: Array,
      last_checked: Date
    },
    social_profiles: Array
  },
  relationships: [
    {
      entity: String,
      type: String,
      confidence: Number
    }
  ],
  ai_summary: {
    risk_score: Number,
    risk_level: String,
    summary: String,
    key_findings: Array,
    threats_identified: Array,
    recommendations: Array,
    timeline: Array
  },
  status: String,
  created_at: Date,
  updated_at: Date,
  user_id: String (optional)
}

// Indexes
db.osint_investigations.createIndex({ investigation_id: 1 }, { unique: true })
db.osint_investigations.createIndex({ target: 1 })
db.osint_investigations.createIndex({ created_at: -1 })
```

#### 3. threat_intelligence
```javascript
{
  _id: ObjectId,
  threat_id: String (UUID),
  threat_type: String, // "malware", "phishing", "ransomware", "ddos", "vulnerability"
  source: String, // "shodan", "virustotal", "abuseipdb", "manual"
  severity: String, // "low", "medium", "high", "critical"
  title: String,
  description: String,
  indicators: {
    ips: Array,
    domains: Array,
    urls: Array,
    file_hashes: Array,
    cve_ids: Array
  },
  location: {
    type: "Point",
    coordinates: [Number, Number], // [longitude, latitude]
    country: String,
    city: String
  },
  metadata: Object,
  timestamp: Date,
  expires_at: Date
}

// Indexes
db.threat_intelligence.createIndex({ threat_id: 1 }, { unique: true })
db.threat_intelligence.createIndex({ timestamp: -1 })
db.threat_intelligence.createIndex({ threat_type: 1, severity: 1 })
db.threat_intelligence.createIndex({ location: "2dsphere" })
db.threat_intelligence.createIndex({ expires_at: 1 }, { expireAfterSeconds: 0 })
```

#### 4. incident_reports
```javascript
{
  _id: ObjectId,
  report_id: String (UUID),
  incident_id: String,
  incident_type: String,
  severity: String,
  title: String,
  sections: {
    executive_summary: String,
    incident_details: String,
    timeline: Array,
    attack_vector: String,
    affected_systems: Array,
    response_actions: Array,
    mitigation_steps: Array,
    recommendations: Array
  },
  mitre_attack: {
    tactics: Array,
    techniques: Array
  },
  metadata: {
    generated_by: String,
    generation_time: Number, // seconds
    model_used: String
  },
  pdf_url: String,
  status: String, // "draft", "final", "archived"
  created_at: Date,
  updated_at: Date,
  user_id: String (optional)
}

// Indexes
db.incident_reports.createIndex({ report_id: 1 }, { unique: true })
db.incident_reports.createIndex({ incident_id: 1 })
db.incident_reports.createIndex({ created_at: -1 })
```

#### 5. chat_sessions
```javascript
{
  _id: ObjectId,
  session_id: String (UUID),
  messages: [
    {
      message_id: String (UUID),
      role: String, // "user", "assistant"
      content: String,
      context_used: Array, // References to knowledge base
      timestamp: Date
    }
  ],
  metadata: {
    total_messages: Number,
    total_tokens: Number,
    model_used: String
  },
  created_at: Date,
  updated_at: Date,
  last_activity: Date,
  user_id: String (optional)
}

// Indexes
db.chat_sessions.createIndex({ session_id: 1 }, { unique: true })
db.chat_sessions.createIndex({ last_activity: -1 })
db.chat_sessions.createIndex({ created_at: -1 })
```

---

## Performance Optimization

### Backend Optimizations

1. **Async Operations**
   - Use `asyncio` for concurrent API calls
   - Implement connection pooling
   - Use `aiohttp` for HTTP requests

2. **Caching Strategy**
   ```python
   # Redis caching for API responses
   - VirusTotal results: 24 hours
   - AbuseIPDB results: 6 hours
   - HIBP results: 12 hours
   - Shodan results: 48 hours
   ```

3. **Database Optimization**
   - Use indexes on frequently queried fields
   - Implement pagination for large result sets
   - Use aggregation pipeline for complex queries

4. **Rate Limiting**
   ```python
   # Implement token bucket algorithm
   - Per-user rate limits
   - Per-endpoint rate limits
   - Graceful degradation
   ```

### Frontend Optimizations

1. **Code Splitting**
   ```javascript
   // Lazy load routes
   const PhishingPage = lazy(() => import('./pages/PhishingPage'))
   const OSINTPage = lazy(() => import('./pages/OSINTPage'))
   ```

2. **Data Fetching**
   - Use SWR or React Query for caching
   - Implement optimistic updates
   - Debounce search inputs

3. **Asset Optimization**
   - Compress images
   - Use WebP format
   - Lazy load images
   - Tree-shake unused code

---

## Security Implementation

### 1. Input Validation
```python
from pydantic import BaseModel, validator, EmailStr

class PhishingAnalysisRequest(BaseModel):
    content_type: str
    content: str
    
    @validator('content_type')
    def validate_content_type(cls, v):
        allowed = ['email', 'url', 'sms', 'file']
        if v not in allowed:
            raise ValueError(f'content_type must be one of {allowed}')
        return v
    
    @validator('content')
    def validate_content(cls, v):
        if len(v) > 1_000_000:  # 1MB limit
            raise ValueError('content too large')
        return v
```

### 2. API Key Management
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    virustotal_api_key: str
    abuseipdb_api_key: str
    hibp_api_key: str
    shodan_api_key: str
    ibm_cloud_api_key: str
    ibm_project_id: str
    mongodb_uri: str
    
    class Config:
        env_file = ".env"
        case_sensitive = False
```

### 3. CORS Configuration
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Error Handling Strategy

### Backend Error Responses
```python
from fastapi import HTTPException

class APIError(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail

# Usage
if not api_key:
    raise APIError(401, "API key required")

# Global exception handler
@app.exception_handler(APIError)
async def api_error_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )
```

### Frontend Error Handling
```javascript
// API client with error handling
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  timeout: 30000,
})

api.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 429) {
      toast.error('Rate limit exceeded. Please try again later.')
    } else if (error.response?.status >= 500) {
      toast.error('Server error. Please try again.')
    }
    return Promise.reject(error)
  }
)
```

---

## Testing Specifications

### Backend Tests
```python
# tests/test_phishing_service.py
import pytest
from app.services.phishing_service import PhishingService

@pytest.mark.asyncio
async def test_analyze_phishing_email():
    service = PhishingService()
    result = await service.analyze({
        "content_type": "email",
        "content": "Urgent: Verify your account..."
    })
    assert result["threat_score"] > 70
    assert result["is_phishing"] == True

@pytest.mark.asyncio
async def test_virustotal_integration():
    # Test with mocked responses
    pass
```

### Frontend Tests
```javascript
// tests/PhishingDetector.test.jsx
import { render, screen, fireEvent } from '@testing-library/react'
import PhishingDetector from '../components/phishing/PhishingDetector'

test('uploads file and displays results', async () => {
  render(<PhishingDetector />)
  const file = new File(['test'], 'test.txt', { type: 'text/plain' })
  const input = screen.getByLabelText(/upload/i)
  fireEvent.change(input, { target: { files: [file] } })
  // Assert results displayed
})
```

---

## Deployment Configuration

### Docker Setup
```dockerfile
# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```dockerfile
# frontend/Dockerfile
FROM node:20-alpine AS build

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
```

### Docker Compose
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - MONGODB_URI=mongodb://mongo:27017/sentinelx
    depends_on:
      - mongo
    volumes:
      - ./backend:/app

  frontend:
    build: ./frontend
    ports:
      - "5173:80"
    depends_on:
      - backend

  mongo:
    image: mongo:6.0
    ports:
      - "27017:27017"
    volumes:
      - mongo_data:/data/db

volumes:
  mongo_data:
```

---

## Monitoring & Logging

### Backend Logging
```python
import logging
from logging.handlers import RotatingFileHandler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        RotatingFileHandler('app.log', maxBytes=10485760, backupCount=5),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Usage
logger.info(f"Analyzing phishing content: {analysis_id}")
logger.error(f"API error: {str(e)}", exc_info=True)
```

### Performance Monitoring
```python
import time
from functools import wraps

def monitor_performance(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.time()
        result = await func(*args, **kwargs)
        duration = time.time() - start
        logger.info(f"{func.__name__} took {duration:.2f}s")
        return result
    return wrapper
```

---

This technical specification provides the detailed implementation guidelines needed to build SentinelX AI. All components are designed to work together seamlessly while maintaining security, performance, and scalability.