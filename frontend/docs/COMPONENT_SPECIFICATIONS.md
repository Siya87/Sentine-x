# SentinelX AI - Frontend Component Specifications

## Complete React Component Architecture (Part 1 of 2)

This document provides detailed specifications for all frontend components needed to build the SentinelX AI user interface.

---

## Table of Contents
1. [Project Setup](#project-setup)
2. [Core Components](#core-components)
3. [Feature Components](#feature-components)
4. [Shared Components](#shared-components)
5. [API Service Layer](#api-service-layer)

---

## Project Setup

### Dependencies
```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.0",
    "axios": "^1.6.0",
    "framer-motion": "^10.16.0",
    "tailwindcss": "^3.3.0",
    "@headlessui/react": "^1.7.0",
    "@heroicons/react": "^2.0.0",
    "recharts": "^2.10.0",
    "react-markdown": "^9.0.0",
    "date-fns": "^2.30.0",
    "react-hot-toast": "^2.4.0",
    "clsx": "^2.0.0"
  }
}
```

### Folder Structure
```
frontend/
├── src/
│   ├── components/
│   │   ├── layout/
│   │   │   ├── Sidebar.tsx (150 lines)
│   │   │   ├── Header.tsx (100 lines)
│   │   │   ├── Footer.tsx (50 lines)
│   │   │   └── Layout.tsx (80 lines)
│   │   ├── dashboard/
│   │   │   ├── StatCard.tsx (80 lines)
│   │   │   ├── ThreatChart.tsx (120 lines)
│   │   │   ├── ActivityFeed.tsx (150 lines)
│   │   │   └── QuickActions.tsx (100 lines)
│   │   ├── phishing/
│   │   │   ├── PhishingForm.tsx (200 lines)
│   │   │   ├── AnalysisResults.tsx (180 lines)
│   │   │   ├── ThreatScore.tsx (120 lines)
│   │   │   └── Recommendations.tsx (80 lines)
│   │   ├── osint/
│   │   │   ├── InvestigationForm.tsx (150 lines)
│   │   │   ├── ResultsTabs.tsx (200 lines)
│   │   │   ├── BreachData.tsx (120 lines)
│   │   │   └── RelationshipGraph.tsx (150 lines)
│   │   ├── threat/
│   │   │   ├── ThreatFeed.tsx (180 lines)
│   │   │   ├── ThreatCard.tsx (100 lines)
│   │   │   ├── ThreatMap.tsx (150 lines)
│   │   │   └── ThreatFilters.tsx (120 lines)
│   │   ├── report/
│   │   │   ├── ReportForm.tsx (250 lines)
│   │   │   ├── ReportPreview.tsx (180 lines)
│   │   │   ├── MitreSelector.tsx (200 lines)
│   │   │   └── TimelineBuilder.tsx (150 lines)
│   │   ├── chat/
│   │   │   ├── ChatInterface.tsx (200 lines)
│   │   │   ├── MessageBubble.tsx (100 lines)
│   │   │   ├── SuggestionChips.tsx (80 lines)
│   │   │   └── KnowledgeBase.tsx (120 lines)
│   │   └── shared/
│   │       ├── Button.tsx (100 lines)
│   │       ├── Card.tsx (80 lines)
│   │       ├── Input.tsx (80 lines)
│   │       ├── Modal.tsx (120 lines)
│   │       ├── Loading.tsx (60 lines)
│   │       └── Badge.tsx (60 lines)
│   ├── pages/
│   │   ├── Dashboard.tsx (200 lines)
│   │   ├── PhishingDetector.tsx (180 lines)
│   │   ├── OSINTInvestigator.tsx (180 lines)
│   │   ├── ThreatIntelligence.tsx (200 lines)
│   │   ├── ReportGenerator.tsx (220 lines)
│   │   └── ChatAssistant.tsx (180 lines)
│   ├── services/
│   │   ├── api.ts (150 lines)
│   │   ├── phishing.service.ts (100 lines)
│   │   ├── osint.service.ts (100 lines)
│   │   ├── threat.service.ts (100 lines)
│   │   ├── report.service.ts (100 lines)
│   │   └── chat.service.ts (100 lines)
│   ├── types/
│   │   └── index.ts (300 lines)
│   ├── App.tsx (100 lines)
│   └── index.tsx (50 lines)
```

**Total Estimated Lines: ~5,500 lines**

---

## Core Components

### 1. Layout Component (`components/layout/Layout.tsx`)

**Purpose**: Main application layout with sidebar navigation

**Props**: 
```typescript
interface LayoutProps {
  children: React.ReactNode;
}
```

**Key Features**:
- Responsive sidebar (collapsible on mobile)
- Sticky header
- Scrollable main content area
- Dark theme with cybersecurity aesthetics

**Implementation Structure**:
```tsx
import { useState } from 'react';
import Sidebar from './Sidebar';
import Header from './Header';
import Footer from './Footer';

export default function Layout({ children }: LayoutProps) {
  const [sidebarOpen, setSidebarOpen] = useState(true);

  return (
    <div className="flex h-screen bg-gray-900">
      <Sidebar isOpen={sidebarOpen} onToggle={() => setSidebarOpen(!sidebarOpen)} />
      <div className="flex-1 flex flex-col overflow-hidden">
        <Header onMenuClick={() => setSidebarOpen(!sidebarOpen)} />
        <main className="flex-1 overflow-y-auto p-6">
          {children}
        </main>
        <Footer />
      </div>
    </div>
  );
}
```

---

### 2. Sidebar Component (`components/layout/Sidebar.tsx`)

**Purpose**: Navigation menu for all features

**Props**:
```typescript
interface SidebarProps {
  isOpen: boolean;
  onToggle: () => void;
}
```

**Navigation Items**:
```typescript
const navItems = [
  { name: 'Dashboard', icon: HomeIcon, path: '/dashboard' },
  { name: 'Phishing Detector', icon: ShieldExclamationIcon, path: '/phishing' },
  { name: 'OSINT Investigator', icon: MagnifyingGlassIcon, path: '/osint' },
  { name: 'Threat Intelligence', icon: ExclamationTriangleIcon, path: '/threat' },
  { name: 'Report Generator', icon: DocumentTextIcon, path: '/report' },
  { name: 'Chat Assistant', icon: ChatBubbleLeftRightIcon, path: '/chat' }
];
```

**Styling Guidelines**:
- Width: 256px (expanded), 64px (collapsed)
- Background: bg-gray-800
- Active item: bg-blue-600 with left border
- Hover: bg-gray-700 transition
- Icons: 24x24px from @heroicons/react

---

### 3. Header Component (`components/layout/Header.tsx`)

**Purpose**: Top navigation bar with user info and actions

**Key Elements**:
- Logo and app name
- Search bar (global)
- Notifications icon with badge
- User profile dropdown

**Structure**:
```tsx
<header className="bg-gray-800 border-b border-gray-700 px-6 py-4">
  <div className="flex items-center justify-between">
    <div className="flex items-center space-x-4">
      <button onClick={onMenuClick} className="lg:hidden">
        <Bars3Icon className="w-6 h-6 text-gray-400" />
      </button>
      <h1 className="text-2xl font-bold text-white">SentinelX AI</h1>
    </div>
    <div className="flex items-center space-x-4">
      <NotificationBell count={3} />
      <UserMenu />
    </div>
  </div>
</header>
```

---

## Feature Components

### Dashboard Components

#### StatCard (`components/dashboard/StatCard.tsx`)

**Props**:
```typescript
interface StatCardProps {
  title: string;
  value: string | number;
  change?: string;
  icon?: React.ComponentType<{ className?: string }>;
  trend?: 'up' | 'down' | 'neutral';
}
```

**Animation**: Framer Motion fade-in with slide up

**Design Pattern**:
```tsx
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  className="bg-gray-800 rounded-lg p-6 border border-gray-700"
>
  <div className="flex items-center justify-between">
    <div>
      <p className="text-gray-400 text-sm">{title}</p>
      <p className="text-3xl font-bold text-white mt-2">{value}</p>
      {change && (
        <p className={`text-sm mt-2 ${getTrendColor(trend)}`}>
          {change}
        </p>
      )}
    </div>
    {icon && <Icon className="w-12 h-12 text-blue-500" />}
  </div>
</motion.div>
```

---

#### ThreatChart (`components/dashboard/ThreatChart.tsx`)

**Purpose**: Line chart showing threat trends over time

**Library**: Recharts

**Data Structure**:
```typescript
interface ChartData {
  date: string;
  threats: number;
  investigations: number;
  reports: number;
}
```

**Chart Configuration**:
- Type: LineChart
- Height: 300px
- Colors: Red (#EF4444), Blue (#3B82F6), Green (#10B981)
- Grid: Dashed with gray-700
- Tooltip: Dark theme with gray-800 background

---

#### ActivityFeed (`components/dashboard/ActivityFeed.tsx`)

**Purpose**: Real-time feed of recent activities

**Data Structure**:
```typescript
interface Activity {
  id: string;
  type: 'threat' | 'investigation' | 'report' | 'chat';
  title: string;
  description: string;
  timestamp: Date;
  severity?: 'low' | 'medium' | 'high' | 'critical';
}
```

**Features**:
- Auto-refresh every 30 seconds
- Animated entry with stagger effect
- Click to view details
- Severity badges
- Relative timestamps

---

### Phishing Detector Components

#### PhishingForm (`components/phishing/PhishingForm.tsx`)

**Props**:
```typescript
interface PhishingFormProps {
  type: 'email' | 'url' | 'file' | 'sms';
  onTypeChange: (type: string) => void;
  onSubmit: (data: FormData) => Promise<void>;
  isLoading: boolean;
}
```

**Form Types**:

1. **Email Analysis**:
   - Textarea for email content
   - File upload for .eml files
   - Headers extraction option

2. **URL Analysis**:
   - Input field with URL validation
   - Auto-fetch page title
   - Screenshot option

3. **File Analysis**:
   - Drag-and-drop zone
   - File type validation
   - Max size: 10MB

4. **SMS Analysis**:
   - Textarea for message content
   - Sender number field
   - Timestamp field

---

#### ThreatScore (`components/phishing/ThreatScore.tsx`)

**Purpose**: Visual representation of threat score with circular progress

**Props**:
```typescript
interface ThreatScoreProps {
  score: number; // 0-100
  isPhishing: boolean;
  confidence: number;
}
```

**Visual Design**:
- Circular progress indicator (SVG)
- Color coding:
  - 0-30: Green (#10B981)
  - 31-60: Yellow (#F59E0B)
  - 61-80: Orange (#F97316)
  - 81-100: Red (#EF4444)
- Animated fill on mount
- Large centered score number

---

#### AnalysisResults (`components/phishing/AnalysisResults.tsx`)

**Sections**:
1. Threat Score (prominent display)
2. Phishing Indicators (list with severity)
3. AI Explanation (markdown formatted)
4. Recommendations (actionable steps)
5. Technical Details (collapsible)

**Layout**: Grid with responsive columns

---

### OSINT Investigator Components

#### InvestigationForm (`components/osint/InvestigationForm.tsx`)

**Investigation Types**:
```typescript
type InvestigationType = 'email' | 'username' | 'phone' | 'domain' | 'ip';
```

**Form Fields by Type**:
- Email: Email address input
- Username: Username + platform selector
- Phone: Phone number with country code
- Domain: Domain name input
- IP: IP address input with validation

**Validation**:
- Email: RFC 5322 format
- Phone: E.164 format
- Domain: Valid domain regex
- IP: IPv4/IPv6 validation

---

#### ResultsTabs (`components/osint/ResultsTabs.tsx`)

**Tab Structure**:
```typescript
const tabs = [
  { id: 'summary', name: 'Summary', icon: DocumentTextIcon },
  { id: 'breaches', name: 'Breach Data', icon: ExclamationTriangleIcon },
  { id: 'social', name: 'Social Profiles', icon: UserGroupIcon },
  { id: 'ip', name: 'IP Information', icon: GlobeAltIcon },
  { id: 'risk', name: 'Risk Analysis', icon: ShieldExclamationIcon }
];
```

**Features**:
- Smooth tab transitions
- Badge counts on tabs
- Export button per tab
- Loading states

---

#### BreachData (`components/osint/BreachData.tsx`)

**Display Format**:
```tsx
<div className="space-y-4">
  {breaches.map(breach => (
    <div className="bg-gray-700 rounded-lg p-4 border-l-4 border-red-500">
      <div className="flex justify-between items-start">
        <div>
          <h4 className="text-white font-semibold">{breach.name}</h4>
          <p className="text-gray-400 text-sm">{breach.domain}</p>
          <p className="text-gray-500 text-xs mt-1">
            Breach Date: {formatDate(breach.breach_date)}
          </p>
        </div>
        <Badge severity="high">Compromised</Badge>
      </div>
      <div className="mt-3">
        <p className="text-gray-300 text-sm mb-2">Exposed Data:</p>
        <div className="flex flex-wrap gap-2">
          {breach.data_classes.map(dataClass => (
            <span className="px-2 py-1 bg-gray-800 rounded text-xs">
              {dataClass}
            </span>
          ))}
        </div>
      </div>
    </div>
  ))}
</div>
```

---

### Threat Intelligence Components

#### ThreatFeed (`components/threat/ThreatFeed.tsx`)

**Features**:
- Real-time updates (WebSocket or polling)
- Infinite scroll
- Filter by severity/type
- Search functionality
- Auto-refresh toggle

**Card Layout**:
- Severity indicator (left border)
- Threat type badge
- Title and description
- Source and timestamp
- Click to expand details

---

#### ThreatMap (`components/threat/ThreatMap.tsx`)

**Visualization Options**:

1. **Bar Chart** (Country-based):
   - X-axis: Countries
   - Y-axis: Threat count
   - Color: Severity-based

2. **Heatmap** (Alternative):
   - Grid layout by region
   - Color intensity by threat count

**Library**: Recharts for charts

---

### Report Generator Components

#### ReportForm (`components/report/ReportForm.tsx`)

**Form Sections**:

1. **Basic Information**:
   - Report title
   - Incident type (dropdown)
   - Severity level
   - Detection time
   - Reporter name

2. **Incident Details**:
   - Description (rich text)
   - Attack vector
   - Entry point
   - Scope

3. **Affected Systems**:
   - Dynamic list
   - System name/IP
   - Impact level

4. **Indicators of Compromise**:
   - IP addresses
   - Domains
   - File hashes
   - URLs

5. **MITRE ATT&CK**:
   - Tactic selector
   - Technique selector
   - Sub-technique (optional)

6. **Timeline**:
   - Event builder
   - Timestamp
   - Description
   - Evidence links

---

#### MitreSelector (`components/report/MitreSelector.tsx`)

**Structure**:
```typescript
interface MitreTactic {
  id: string;
  name: string;
  techniques: MitreTechnique[];
}

interface MitreTechnique {
  id: string;
  name: string;
  description: string;
  subtechniques?: MitreTechnique[];
}
```

**UI Design**:
- Accordion for tactics
- Checkboxes for techniques
- Search/filter functionality
- Selected count badge
- Quick select common techniques

---

#### ReportPreview (`components/report/ReportPreview.tsx`)

**Preview Sections**:
1. Executive Summary (auto-generated)
2. Incident Details
3. Timeline (visual)
4. Affected Systems (table)
5. IOCs (formatted list)
6. MITRE ATT&CK Mapping (visual)
7. Recommendations
8. Appendix

**Actions**:
- Edit button (back to form)
- Generate with AI button
- Export as PDF
- Save draft

---

### Chat Assistant Components

#### ChatInterface (`components/chat/ChatInterface.tsx`)

**Layout**:
```tsx
<div className="flex flex-col h-full">
  <ChatHeader sessionId={sessionId} />
  <div className="flex-1 overflow-y-auto p-6 space-y-4">
    {messages.map(msg => (
      <MessageBubble key={msg.id} message={msg} />
    ))}
    {isTyping && <TypingIndicator />}
    <div ref={messagesEndRef} />
  </div>
  <SuggestionChips suggestions={suggestions} onSelect={handleSend} />
  <ChatInput 
    value={input}
    onChange={setInput}
    onSend={handleSend}
    disabled={isTyping}
  />
</div>
```

**Features**:
- Auto-scroll to bottom
- Message grouping by time
- Markdown rendering
- Code syntax highlighting
- Copy message button

---

#### MessageBubble (`components/chat/MessageBubble.tsx`)

**Design**:
- User messages: Right-aligned, blue background
- AI messages: Left-aligned, gray background
- Avatar icons
- Timestamp
- Markdown support
- Copy button

**Animation**: Fade in with slide effect

---

#### KnowledgeBase (`components/chat/KnowledgeBase.tsx`)

**Display**:
```tsx
<div className="space-y-3">
  <h3 className="text-white font-semibold mb-4">Knowledge Base</h3>
  {entries.map(entry => (
    <div 
      className="bg-gray-700 rounded-lg p-3 cursor-pointer hover:bg-gray-600"
      onClick={() => onSelect(entry.question)}
    >
      <h4 className="text-white text-sm font-medium">{entry.question}</h4>
      <p className="text-gray-400 text-xs mt-1 line-clamp-2">
        {entry.answer}
      </p>
      <div className="flex flex-wrap gap-1 mt-2">
        {entry.keywords.slice(0, 3).map(keyword => (
          <span className="px-2 py-0.5 bg-gray-800 rounded text-xs">
            {keyword}
          </span>
        ))}
      </div>
    </div>
  ))}
</div>
```

---

## Shared Components

### Button (`components/shared/Button.tsx`)

**Variants**:
```typescript
const variants = {
  primary: 'bg-blue-600 hover:bg-blue-700 text-white',
  secondary: 'bg-gray-600 hover:bg-gray-700 text-white',
  outline: 'border-2 border-blue-600 text-blue-600 hover:bg-blue-600 hover:text-white',
  danger: 'bg-red-600 hover:bg-red-700 text-white'
};

const sizes = {
  sm: 'px-3 py-1.5 text-sm',
  md: 'px-4 py-2 text-base',
  lg: 'px-6 py-3 text-lg'
};
```

---

### Card (`components/shared/Card.tsx`)

**Base Styling**:
```css
bg-gray-800 rounded-lg border border-gray-700 p-6
```

**Features**:
- Optional title
- Optional actions (top-right)
- Hover effect (optional)
- Loading state overlay

---

### Modal (`components/shared/Modal.tsx`)

**Sizes**:
- sm: max-w-md
- md: max-w-lg
- lg: max-w-2xl
- xl: max-w-4xl

**Features**:
- Backdrop blur
- Click outside to close
- ESC key to close
- Smooth transitions
- Focus trap

---

## API Service Layer

### Base API (`services/api.ts`)

```typescript
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Add auth token if exists
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Handle errors globally
    if (error.response?.status === 401) {
      // Redirect to login
    }
    return Promise.reject(error);
  }
);

export default api;
```

---

### Service Files

Each feature has its own service file:

**phishing.service.ts**:
```typescript
import api from './api';

export const analyzeEmail = (data: EmailData) => 
  api.post('/api/phishing/analyze-email', data);

export const analyzeURL = (url: string) => 
  api.post('/api/phishing/analyze-url', { url });

export const analyzeFile = (file: File) => {
  const formData = new FormData();
  formData.append('file', file);
  return api.post('/api/phishing/analyze-file', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });
};
```

Similar structure for:
- osint.service.ts
- threat.service.ts
- report.service.ts
- chat.service.ts

---

## TypeScript Types (`types/index.ts`)

```typescript
// Common types
export interface ApiResponse<T> {
  success: boolean;
  data: T;
  message?: string;
}

// Phishing types
export interface PhishingAnalysis {
  threat_score: number;
  is_phishing: boolean;
  confidence: number;
  indicators: PhishingIndicator[];
  explanation: string;
  recommendations: string[];
}

// OSINT types
export interface OSINTInvestigation {
  investigation_id: string;
  target: string;
  investigation_type: string;
  summary: string;
  breach_data: BreachData[];
  social_profiles: SocialProfile[];
  risk_score: number;
}

// Threat types
export interface Threat {
  threat_id: string;
  threat_type: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  title: string;
  description: string;
  source: string;
  timestamp: Date;
}

// Report types
export interface IncidentReport {
  report_id: string;
  title: string;
  incident_type: string;
  severity: string;
  description: string;
  affected_systems: string[];
  indicators: string[];
  mitre_techniques: string[];
  timeline: TimelineEvent[];
}

// Chat types
export interface ChatMessage {
  message_id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}
```

---

## Styling Guide

### Color Palette

```css
/* Background */
--bg-primary: #111827;    /* gray-900 */
--bg-secondary: #1F2937;  /* gray-800 */
--bg-tertiary: #374151;   /* gray-700 */

/* Text */
--text-primary: #F9FAFB;  /* gray-50 */
--text-secondary: #D1D5DB; /* gray-300 */
--text-tertiary: #9CA3AF;  /* gray-400 */

/* Accent */
--accent-primary: #3B82F6;  /* blue-600 */
--accent-hover: #2563EB;    /* blue-700 */

/* Status */
--success: #10B981;  /* green-500 */
--warning: #F59E0B;  /* yellow-500 */
--error: #EF4444;    /* red-500 */
--info: #3B82F6;     /* blue-500 */

/* Severity */
--severity-low: #10B981;      /* green-500 */
--severity-medium: #F59E0B;   /* yellow-500 */
--severity-high: #F97316;     /* orange-500 */
--severity-critical: #EF4444; /* red-500 */
```

### Animation Patterns

```typescript
// Fade in
const fadeIn = {
  initial: { opacity: 0 },
  animate: { opacity: 1 },
  exit: { opacity: 0 }
};

// Slide up
const slideUp = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0 },
  exit: { opacity: 0, y: -20 }
};

// Scale
const scale = {
  initial: { scale: 0.9, opacity: 0 },
  animate: { scale: 1, opacity: 1 },
  exit: { scale: 0.9, opacity: 0 }
};
```

---

## Implementation Priority

### Phase 1: Core Setup (Day 1)
1. Initialize React project
2. Setup Tailwind CSS
3. Install dependencies
4. Create folder structure
5. Setup routing
6. Create Layout components

### Phase 2: Shared Components (Day 1-2)
1. Button
2. Card
3. Input
4. Modal
5. Badge
6. Loading

### Phase 3: Dashboard (Day 2-3)
1. Dashboard page
2. StatCard
3. ThreatChart
4. ActivityFeed

### Phase 4: Feature Pages (Day 3-7)
1. Phishing Detector (Day 3-4)
2. OSINT Investigator (Day 4-5)
3. Threat Intelligence (Day 5-6)
4. Report Generator (Day 6-7)
5. Chat Assistant (Day 7)

### Phase 5: Polish & Testing (Day 8-10)
1. Responsive design
2. Error handling
3. Loading states
4. Animations
5. Testing
6. Documentation

---

**End of Component Specifications Document**

For detailed implementation of each component, refer to the individual component files in the `src/components/` directory.