# 🛡️ SentinelX AI

**AI-Powered Cyber Investigation & Threat Intelligence Assistant**

An intelligent platform that helps SOC teams, investigators, and security professionals analyze cyber threats, phishing attacks, and OSINT evidence automatically using IBM Granite AI models.

---

## 🌟 Features

### 1. 🎣 AI Phishing Detector
- Analyze emails, URLs, SMS, and files for phishing indicators
- Integration with VirusTotal for malware scanning
- AI-powered threat scoring (0-100)
- Detailed explanations and recommendations
- Real-time analysis with IBM Granite models

### 2. 🔍 OSINT Investigation Agent
- Investigate usernames, emails, phone numbers, and domains
- Aggregate data from multiple sources (HaveIBeenPwned, AbuseIPDB, Shodan)
- Generate comprehensive investigation summaries
- Visualize relationships with interactive graphs
- AI-powered risk assessment

### 3. 📊 Threat Intelligence Dashboard
- Real-time threat monitoring
- Interactive charts and visualizations
- Geographic attack heatmaps
- Trend analysis and predictions
- Live updates every 30 seconds

### 4. 📝 AI Incident Report Generator
- Automated report generation
- Professional formatting with multiple sections
- MITRE ATT&CK technique mapping
- PDF export functionality
- Customizable templates

### 5. 💬 AI Chat Assistant
- Natural language cybersecurity queries
- Context-aware responses
- MITRE ATT&CK framework knowledge
- CVE database integration
- Conversational interface with memory

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (React)                         │
│  Phishing Detector │ OSINT │ Dashboard │ Reports │ Chat     │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                  API Gateway (FastAPI)                       │
│         Authentication │ Rate Limiting │ Validation          │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
┌──────────────┐ ┌──────────┐ ┌──────────────┐
│ IBM Granite  │ │ External │ │   MongoDB    │
│   AI Models  │ │   APIs   │ │   Database   │
│              │ │          │ │              │
│ • Analysis   │ │ • VT     │ │ • Analyses   │
│ • Reports    │ │ • HIBP   │ │ • Reports    │
│ • Chat       │ │ • Shodan │ │ • Threats    │
└──────────────┘ └──────────┘ └──────────────┘
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 20+
- MongoDB 6.0+
- API Keys:
  - IBM Cloud (Granite models)
  - VirusTotal
  - AbuseIPDB
  - HaveIBeenPwned (optional)
  - Shodan

### Backend Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/sentinelx-ai.git
cd sentinelx-ai

# Setup backend
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your API keys

# Start MongoDB (if not running)
mongod --dbpath /path/to/data

# Run the backend
uvicorn app.main:app --reload
```

Backend will be available at `http://localhost:8000`

### Frontend Setup

```bash
# In a new terminal
cd frontend
npm install

# Configure environment
cp .env.example .env
# Edit .env if needed

# Start development server
npm run dev
```

Frontend will be available at `http://localhost:5173`

---

## 📚 Documentation

- **[Architecture Guide](ARCHITECTURE.md)** - System design and component overview
- **[Technical Specifications](TECHNICAL_SPECS.md)** - Detailed technical documentation
- **[Implementation Guide](IMPLEMENTATION_GUIDE.md)** - Step-by-step development guide
- **[API Documentation](http://localhost:8000/docs)** - Interactive API docs (when running)

---

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **IBM Granite** - AI models for analysis and generation
- **LangChain** - RAG pipeline and conversational AI
- **MongoDB** - Document database
- **Motor** - Async MongoDB driver

### Frontend
- **React 18** - UI framework
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **Framer Motion** - Animations
- **Recharts** - Data visualization
- **React Flow** - Graph visualization

### External APIs
- **VirusTotal** - Malware scanning
- **AbuseIPDB** - IP reputation
- **HaveIBeenPwned** - Breach data
- **Shodan** - Internet-wide scanning

---

## 📖 Usage Examples

### Phishing Analysis

```bash
curl -X POST http://localhost:8000/api/phishing/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "content_type": "email",
    "content": "Urgent: Your account will be suspended. Click here to verify."
  }'
```

### OSINT Investigation

```bash
curl -X POST http://localhost:8000/api/osint/investigate \
  -H "Content-Type: application/json" \
  -d '{
    "target": "user@example.com",
    "target_type": "email"
  }'
```

### Chat Query

```bash
curl -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "unique-session-id",
    "message": "What is a phishing attack?"
  }'
```

---

## 🎯 Demo Scenarios

### Scenario 1: Phishing Email Detection
1. Navigate to Phishing Detector
2. Select "Email" as content type
3. Paste a suspicious email
4. Click "Analyze"
5. Review threat score and indicators

### Scenario 2: OSINT Investigation
1. Navigate to OSINT Investigation
2. Enter an email address
3. Click "Investigate"
4. Review breach data and risk assessment
5. Explore relationship graph

### Scenario 3: Threat Monitoring
1. Navigate to Dashboard
2. View real-time threat statistics
3. Explore geographic heatmap
4. Analyze trend charts
5. Monitor live updates

### Scenario 4: Incident Report
1. Navigate to Reports
2. Select incident type
3. Fill in incident details
4. Click "Generate Report"
5. Download PDF

### Scenario 5: AI Assistant
1. Navigate to Chat
2. Ask: "What is ransomware?"
3. Follow up: "How to prevent it?"
4. Ask: "Explain MITRE ATT&CK T1566"
5. Review detailed responses

---

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest tests/ -v --cov=app
```

### Frontend Tests
```bash
cd frontend
npm test
```

### Integration Tests
```bash
cd backend
pytest tests/test_integration.py -v
```

---

## 🔒 Security Considerations

- **API Keys**: Never commit API keys to version control
- **Input Validation**: All inputs are validated and sanitized
- **Rate Limiting**: Implemented on all endpoints
- **HTTPS**: Use HTTPS in production
- **Authentication**: Add authentication for production use
- **Data Encryption**: Encrypt sensitive data at rest

---

## 📈 Performance

- **API Response Time**: < 3 seconds
- **Dashboard Load Time**: < 2 seconds
- **Chat Response Time**: < 5 seconds
- **Concurrent Users**: Supports 100+ concurrent users
- **Database Queries**: Optimized with indexes

---

## 🚢 Deployment

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Production Deployment

See [DEPLOYMENT.md](docs/DEPLOYMENT.md) for detailed production deployment instructions including:
- Cloud deployment (AWS, Azure, GCP)
- Environment configuration
- Database setup
- SSL/TLS configuration
- Monitoring and logging

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **IBM Granite** for powerful AI models
- **VirusTotal** for malware scanning capabilities
- **AbuseIPDB** for IP reputation data
- **HaveIBeenPwned** for breach data
- **Shodan** for internet-wide scanning data
- **MITRE ATT&CK** for threat intelligence framework

---

## 📞 Support

- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/yourusername/sentinelx-ai/issues)
- **Email**: support@sentinelx-ai.com

---

## 🗺️ Roadmap

### Phase 1 (Current - MVP)
- ✅ AI Phishing Detector
- ✅ OSINT Investigation Agent
- ✅ Threat Intelligence Dashboard
- ✅ AI Incident Report Generator
- ✅ AI Chat Assistant

### Phase 2 (Future)
- [ ] User authentication and multi-tenancy
- [ ] Advanced threat correlation engine
- [ ] Automated threat hunting workflows
- [ ] SIEM integration
- [ ] Mobile application

### Phase 3 (Long-term)
- [ ] Real-time collaboration features
- [ ] Custom report templates
- [ ] API for third-party integrations
- [ ] Machine learning model training
- [ ] Blockchain-based evidence chain

---

## 📊 Project Status

**Current Version**: 1.0.0 (MVP)  
**Status**: Active Development  
**Last Updated**: May 2026

---

<div align="center">

**Built with ❤️ using IBM Granite AI**

[Website](https://sentinelx-ai.com) • [Documentation](docs/) • [Demo](https://demo.sentinelx-ai.com)

</div>