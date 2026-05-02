# SentinelX AI - Project Structure

## 📁 Clean Project Organization

```
SentinelX_AI/
│
├── 📄 README.md                    # Main project documentation
├── 📄 QUICK_START.md               # Quick start guide
├── 📄 ARCHITECTURE.md              # System architecture
├── 📄 TECHNICAL_SPECS.md           # Technical specifications
├── 📄 IMPLEMENTATION_GUIDE.md      # Implementation details
│
├── 📂 backend/                     # Python FastAPI Backend
│   ├── 📄 .env                     # Environment variables (DO NOT COMMIT)
│   ├── 📄 .env.example             # Environment template
│   ├── 📄 requirements.txt         # Python dependencies
│   ├── 📄 restart-backend.bat      # Windows restart script
│   ├── 📄 restart-backend.ps1      # PowerShell restart script
│   ├── 📄 start-backend.py         # Cross-platform start script
│   │
│   └── 📂 app/                     # Application code
│       ├── 📄 __init__.py
│       ├── 📄 main.py              # FastAPI application entry
│       ├── 📄 config.py            # Configuration management
│       │
│       ├── 📂 routes/              # API endpoints
│       │   ├── 📄 __init__.py
│       │   ├── 📄 phishing.py      # Phishing detection routes
│       │   ├── 📄 osint.py         # OSINT investigation routes
│       │   ├── 📄 threat.py        # Threat intelligence routes
│       │   ├── 📄 report.py        # Report generation routes
│       │   ├── 📄 chat.py          # Chat assistant routes
│       │   └── 📄 dashboard.py     # Dashboard routes
│       │
│       ├── 📂 services/            # Business logic
│       │   ├── 📄 __init__.py
│       │   ├── 📄 ai_service.py    # IBM Granite AI integration
│       │   ├── 📄 phishing_service.py
│       │   ├── 📄 osint_service.py
│       │   ├── 📄 threat_service.py
│       │   ├── 📄 report_service.py
│       │   └── 📄 chat_service.py
│       │
│       ├── 📂 models/              # Data models
│       │   ├── 📄 __init__.py
│       │   ├── 📄 phishing.py
│       │   ├── 📄 osint.py
│       │   ├── 📄 threat.py
│       │   ├── 📄 report.py
│       │   └── 📄 chat.py
│       │
│       ├── 📂 database/            # Database connections
│       │   ├── 📄 __init__.py
│       │   └── 📄 mongodb.py
│       │
│       └── 📂 utils/               # Utility functions
│           ├── 📄 __init__.py
│           ├── 📄 validators.py
│           └── 📄 helpers.py
│
├── 📂 frontend/                    # React TypeScript Frontend
│   ├── 📄 package.json             # Node dependencies
│   ├── 📄 tsconfig.json            # TypeScript config
│   ├── 📄 tailwind.config.js       # Tailwind CSS config
│   ├── 📄 .env                     # Frontend environment variables
│   │
│   ├── 📂 public/                  # Static assets
│   │   └── 📄 index.html
│   │
│   └── 📂 src/                     # Source code
│       ├── 📄 App.tsx              # Main app component
│       ├── 📄 index.tsx            # Entry point
│       ├── 📄 index.css            # Global styles
│       │
│       ├── 📂 pages/               # Page components
│       │   ├── 📄 Dashboard.tsx
│       │   ├── 📄 PhishingDetector.tsx
│       │   ├── 📄 OSINTInvestigation.tsx
│       │   ├── 📄 ThreatIntelligence.tsx
│       │   ├── 📄 IncidentReports.tsx
│       │   └── 📄 ChatAssistant.tsx
│       │
│       ├── 📂 components/          # Reusable components
│       │   ├── 📂 shared/          # Shared UI components
│       │   │   ├── 📄 Button.tsx
│       │   │   ├── 📄 Card.tsx
│       │   │   ├── 📄 Input.tsx
│       │   │   ├── 📄 Badge.tsx
│       │   │   ├── 📄 Loading.tsx
│       │   │   └── 📄 Modal.tsx
│       │   │
│       │   ├── 📂 layout/          # Layout components
│       │   │   ├── 📄 Layout.tsx
│       │   │   ├── 📄 Sidebar.tsx
│       │   │   └── 📄 Header.tsx
│       │   │
│       │   └── 📂 dashboard/       # Dashboard-specific
│       │       ├── 📄 StatCard.tsx
│       │       ├── 📄 ThreatChart.tsx
│       │       ├── 📄 ThreatDistribution.tsx
│       │       └── 📄 ActivityFeed.tsx
│       │
│       ├── 📂 services/            # API services
│       │   └── 📄 api.ts           # API client
│       │
│       └── 📂 types/               # TypeScript types
│           └── 📄 index.ts
│
└── 📂 .venv/                       # Python virtual environment (DO NOT COMMIT)
```

## 🎯 Key Files

### Essential Documentation
- **README.md** - Project overview and setup instructions
- **QUICK_START.md** - Fast setup guide for developers
- **ARCHITECTURE.md** - System design and architecture
- **TECHNICAL_SPECS.md** - Detailed technical specifications
- **IMPLEMENTATION_GUIDE.md** - Implementation details and patterns

### Backend Entry Points
- **backend/app/main.py** - FastAPI application
- **backend/start-backend.py** - Start script
- **backend/requirements.txt** - Python dependencies

### Frontend Entry Points
- **frontend/src/index.tsx** - React entry point
- **frontend/src/App.tsx** - Main application component
- **frontend/package.json** - Node dependencies

## 🚀 Quick Commands

### Start Backend
```bash
cd backend
python start-backend.py
# or
restart-backend.bat  # Windows
```

### Start Frontend
```bash
cd frontend
npm start
```

### Install Dependencies

**Backend:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install
```

## 📝 Notes

- `.env` files contain sensitive data - never commit them
- `.venv/` is the Python virtual environment - excluded from git
- `node_modules/` contains npm packages - excluded from git
- All documentation is in Markdown format
- Backend uses Python 3.11+
- Frontend uses React 18 + TypeScript

## 🔒 Security

**Files to NEVER commit:**
- `backend/.env`
- `frontend/.env`
- `backend/.venv/`
- `frontend/node_modules/`
- Any files containing API keys or credentials

**Safe to commit:**
- `.env.example` files (templates without real values)
- All source code files
- Documentation files
- Configuration files (without secrets)