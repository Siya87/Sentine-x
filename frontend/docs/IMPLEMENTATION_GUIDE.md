# SentinelX AI - Frontend Implementation Guide

## Step-by-Step Implementation Instructions

This guide provides detailed, actionable steps to implement the complete React frontend for SentinelX AI.

---

## Table of Contents
1. [Project Initialization](#project-initialization)
2. [Core Setup](#core-setup)
3. [Shared Components Implementation](#shared-components-implementation)
4. [Layout Components](#layout-components)
5. [Feature Implementation](#feature-implementation)
6. [API Integration](#api-integration)
7. [Testing & Deployment](#testing--deployment)

---

## Project Initialization

### Step 1: Create React App

```bash
# Navigate to project root
cd d:/Bob_ibm

# Create frontend directory
mkdir frontend
cd frontend

# Initialize React app with TypeScript
npx create-react-app . --template typescript

# Install dependencies
npm install react-router-dom axios framer-motion
npm install @headlessui/react @heroicons/react
npm install recharts react-markdown date-fns react-hot-toast clsx
npm install -D tailwindcss postcss autoprefixer
npm install -D @types/node

# Initialize Tailwind CSS
npx tailwindcss init -p
```

### Step 2: Configure Tailwind CSS

**File: `tailwind.config.js`**
```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        gray: {
          850: '#1a202e',
        }
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      }
    },
  },
  plugins: [],
}
```

**File: `src/index.css`**
```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  body {
    @apply bg-gray-900 text-gray-100;
  }
}

@layer components {
  .btn-primary {
    @apply px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors;
  }
  
  .card {
    @apply bg-gray-800 rounded-lg border border-gray-700 p-6;
  }
  
  .input-field {
    @apply w-full bg-gray-700 text-white rounded-lg px-4 py-2 border border-gray-600 focus:border-blue-500 focus:outline-none;
  }
}

/* Custom scrollbar */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: #1F2937;
}

::-webkit-scrollbar-thumb {
  background: #4B5563;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #6B7280;
}
```

### Step 3: Setup Environment Variables

**File: `.env`**
```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_NAME=SentinelX AI
REACT_APP_VERSION=1.0.0
```

---

## Core Setup

### Step 4: Create Type Definitions

**File: `src/types/index.ts`**
```typescript
// Common types
export interface ApiResponse<T> {
  success: boolean;
  data: T;
  message?: string;
  error?: string;
}

// Phishing types
export interface PhishingIndicator {
  type: string;
  description: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
}

export interface PhishingAnalysis {
  threat_score: number;
  is_phishing: boolean;
  confidence: number;
  indicators: PhishingIndicator[];
  explanation: string;
  recommendations: string[];
  analysis_time: string;
}

// OSINT types
export interface BreachData {
  name: string;
  domain: string;
  breach_date: string;
  data_classes: string[];
  description: string;
}

export interface SocialProfile {
  platform: string;
  username: string;
  url: string;
  followers?: number;
}

export interface OSINTInvestigation {
  investigation_id: string;
  target: string;
  investigation_type: 'email' | 'username' | 'phone' | 'domain' | 'ip';
  summary: string;
  breach_data: BreachData[];
  social_profiles: SocialProfile[];
  ip_info?: any;
  risk_score: number;
  created_at: string;
}

// Threat types
export interface Threat {
  threat_id: string;
  threat_type: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  title: string;
  description: string;
  source: string;
  timestamp: string;
  indicators: string[];
  geo_location?: {
    country: string;
    city?: string;
    latitude?: number;
    longitude?: number;
  };
}

export interface ThreatStatistics {
  total_threats: number;
  by_severity: Record<string, number>;
  by_type: Record<string, number>;
  by_country: Record<string, number>;
}

// Report types
export interface TimelineEvent {
  timestamp: string;
  event: string;
  description: string;
}

export interface MitreTechnique {
  technique_id: string;
  tactic: string;
}

export interface IncidentReport {
  report_id: string;
  title: string;
  incident_type: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  description: string;
  detection_time: string;
  affected_systems: string[];
  indicators: string[];
  attack_vector: string;
  mitre_techniques: MitreTechnique[];
  timeline: TimelineEvent[];
  mitigation_steps: string[];
  executive_summary: string;
  created_at: string;
}

// Chat types
export interface ChatMessage {
  message_id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
  category?: string;
}

export interface ChatSession {
  session_id: string;
  messages: ChatMessage[];
  created_at: string;
}

export interface KnowledgeBaseEntry {
  id: string;
  question: string;
  answer: string;
  category: string;
  keywords: string[];
}
```

### Step 5: Setup API Service

**File: `src/services/api.ts`**
```typescript
import axios, { AxiosError } from 'axios';
import toast from 'react-hot-toast';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000,
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('auth_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    if (error.response) {
      const status = error.response.status;
      const message = (error.response.data as any)?.detail || 'An error occurred';
      
      switch (status) {
        case 400:
          toast.error(`Bad Request: ${message}`);
          break;
        case 401:
          toast.error('Unauthorized. Please login again.');
          localStorage.removeItem('auth_token');
          window.location.href = '/login';
          break;
        case 403:
          toast.error('Access forbidden');
          break;
        case 404:
          toast.error('Resource not found');
          break;
        case 500:
          toast.error('Server error. Please try again later.');
          break;
        default:
          toast.error(message);
      }
    } else if (error.request) {
      toast.error('Network error. Please check your connection.');
    } else {
      toast.error('An unexpected error occurred');
    }
    
    return Promise.reject(error);
  }
);

export default api;
```

### Step 6: Create Feature Services

**File: `src/services/phishing.service.ts`**
```typescript
import api from './api';
import { PhishingAnalysis } from '../types';

export const phishingService = {
  analyzeEmail: async (data: { content: string; sender?: string; subject?: string }) => {
    const response = await api.post<PhishingAnalysis>('/api/phishing/analyze-email', data);
    return response.data;
  },

  analyzeURL: async (url: string) => {
    const response = await api.post<PhishingAnalysis>('/api/phishing/analyze-url', { url });
    return response.data;
  },

  analyzeFile: async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await api.post<PhishingAnalysis>('/api/phishing/analyze-file', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  },

  analyzeSMS: async (data: { message: string; sender?: string }) => {
    const response = await api.post<PhishingAnalysis>('/api/phishing/analyze-sms', data);
    return response.data;
  },
};
```

**File: `src/services/osint.service.ts`**
```typescript
import api from './api';
import { OSINTInvestigation } from '../types';

export const osintService = {
  investigate: async (target: string, investigationType: string) => {
    const response = await api.post<OSINTInvestigation>('/api/osint/investigate', {
      target,
      investigation_type: investigationType,
    });
    return response.data;
  },

  getInvestigation: async (investigationId: string) => {
    const response = await api.get<OSINTInvestigation>(`/api/osint/investigations/${investigationId}`);
    return response.data;
  },

  searchInvestigations: async (query: string) => {
    const response = await api.get<OSINTInvestigation[]>('/api/osint/search', {
      params: { query },
    });
    return response.data;
  },

  deleteInvestigation: async (investigationId: string) => {
    await api.delete(`/api/osint/investigations/${investigationId}`);
  },
};
```

**File: `src/services/threat.service.ts`**
```typescript
import api from './api';
import { Threat, ThreatStatistics } from '../types';

export const threatService = {
  getLiveThreats: async (limit: number = 50) => {
    const response = await api.get<Threat[]>('/api/threat/live', {
      params: { limit },
    });
    return response.data;
  },

  searchThreats: async (query: string) => {
    const response = await api.get<Threat[]>('/api/threat/search', {
      params: { query },
    });
    return response.data;
  },

  getStatistics: async () => {
    const response = await api.get<ThreatStatistics>('/api/threat/statistics');
    return response.data;
  },

  getHostInfo: async (ip: string) => {
    const response = await api.get(`/api/threat/host/${ip}`);
    return response.data;
  },

  getCountryThreats: async (country: string) => {
    const response = await api.get<Threat[]>('/api/threat/country', {
      params: { country },
    });
    return response.data;
  },
};
```

**File: `src/services/report.service.ts`**
```typescript
import api from './api';
import { IncidentReport } from '../types';

export const reportService = {
  generateReport: async (data: Partial<IncidentReport>) => {
    const response = await api.post<IncidentReport>('/api/report/generate', data);
    return response.data;
  },

  getReport: async (reportId: string) => {
    const response = await api.get<IncidentReport>(`/api/report/${reportId}`);
    return response.data;
  },

  listReports: async (limit: number = 50) => {
    const response = await api.get<IncidentReport[]>('/api/report/list', {
      params: { limit },
    });
    return response.data;
  },

  updateReport: async (reportId: string, data: Partial<IncidentReport>) => {
    const response = await api.put<IncidentReport>(`/api/report/${reportId}`, data);
    return response.data;
  },

  deleteReport: async (reportId: string) => {
    await api.delete(`/api/report/${reportId}`);
  },

  exportPDF: async (reportId: string) => {
    const response = await api.get(`/api/report/${reportId}/export`, {
      responseType: 'blob',
    });
    return response.data;
  },

  getStatistics: async () => {
    const response = await api.get('/api/report/statistics');
    return response.data;
  },
};
```

**File: `src/services/chat.service.ts`**
```typescript
import api from './api';
import { ChatMessage, ChatSession, KnowledgeBaseEntry } from '../types';

export const chatService = {
  sendMessage: async (sessionId: string | null, message: string) => {
    const response = await api.post<ChatMessage>('/api/chat/message', {
      session_id: sessionId,
      message,
    });
    return response.data;
  },

  getSessionHistory: async (sessionId: string) => {
    const response = await api.get<ChatSession>(`/api/chat/sessions/${sessionId}`);
    return response.data;
  },

  listSessions: async () => {
    const response = await api.get<ChatSession[]>('/api/chat/sessions');
    return response.data;
  },

  deleteSession: async (sessionId: string) => {
    await api.delete(`/api/chat/sessions/${sessionId}`);
  },

  getKnowledgeBase: async () => {
    const response = await api.get<KnowledgeBaseEntry[]>('/api/chat/knowledge-base');
    return response.data;
  },
};
```

---

## Shared Components Implementation

### Step 7: Create Button Component

**File: `src/components/shared/Button.tsx`**
```typescript
import React from 'react';
import { motion } from 'framer-motion';
import clsx from 'clsx';

interface ButtonProps {
  children: React.ReactNode;
  onClick?: () => void;
  variant?: 'primary' | 'secondary' | 'outline' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
  disabled?: boolean;
  className?: string;
  type?: 'button' | 'submit' | 'reset';
}

const Button: React.FC<ButtonProps> = ({
  children,
  onClick,
  variant = 'primary',
  size = 'md',
  isLoading = false,
  disabled = false,
  className,
  type = 'button',
}) => {
  const variants = {
    primary: 'bg-blue-600 hover:bg-blue-700 text-white',
    secondary: 'bg-gray-600 hover:bg-gray-700 text-white',
    outline: 'border-2 border-blue-600 text-blue-600 hover:bg-blue-600 hover:text-white',
    danger: 'bg-red-600 hover:bg-red-700 text-white',
  };

  const sizes = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg',
  };

  return (
    <motion.button
      whileHover={{ scale: disabled || isLoading ? 1 : 1.02 }}
      whileTap={{ scale: disabled || isLoading ? 1 : 0.98 }}
      type={type}
      disabled={disabled || isLoading}
      onClick={onClick}
      className={clsx(
        'rounded-lg font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 focus:ring-offset-gray-900',
        variants[variant],
        sizes[size],
        (disabled || isLoading) && 'opacity-50 cursor-not-allowed',
        className
      )}
    >
      {isLoading ? (
        <div className="flex items-center justify-center space-x-2">
          <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
            <circle
              className="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              strokeWidth="4"
              fill="none"
            />
            <path
              className="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            />
          </svg>
          <span>Loading...</span>
        </div>
      ) : (
        children
      )}
    </motion.button>
  );
};

export default Button;
```

### Step 8: Create Card Component

**File: `src/components/shared/Card.tsx`**
```typescript
import React from 'react';
import { motion } from 'framer-motion';
import clsx from 'clsx';

interface CardProps {
  title?: string;
  children: React.ReactNode;
  className?: string;
  actions?: React.ReactNode;
  hover?: boolean;
}

const Card: React.FC<CardProps> = ({
  title,
  children,
  className,
  actions,
  hover = false,
}) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      whileHover={hover ? { y: -4 } : {}}
      className={clsx(
        'bg-gray-800 rounded-lg border border-gray-700 p-6',
        hover && 'transition-shadow hover:shadow-xl hover:shadow-blue-500/10',
        className
      )}
    >
      {title && (
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-xl font-semibold text-white">{title}</h3>
          {actions && <div className="flex items-center space-x-2">{actions}</div>}
        </div>
      )}
      {children}
    </motion.div>
  );
};

export default Card;
```

### Step 9: Create Input Component

**File: `src/components/shared/Input.tsx`**
```typescript
import React from 'react';
import clsx from 'clsx';

interface InputProps {
  label?: string;
  type?: string;
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
  error?: string;
  required?: boolean;
  disabled?: boolean;
  className?: string;
  icon?: React.ComponentType<{ className?: string }>;
}

const Input: React.FC<InputProps> = ({
  label,
  type = 'text',
  value,
  onChange,
  placeholder,
  error,
  required = false,
  disabled = false,
  className,
  icon: Icon,
}) => {
  return (
    <div className={className}>
      {label && (
        <label className="block text-gray-300 text-sm font-medium mb-2">
          {label}
          {required && <span className="text-red-500 ml-1">*</span>}
        </label>
      )}
      <div className="relative">
        {Icon && (
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <Icon className="h-5 w-5 text-gray-400" />
          </div>
        )}
        <input
          type={type}
          value={value}
          onChange={(e) => onChange(e.target.value)}
          placeholder={placeholder}
          disabled={disabled}
          className={clsx(
            'w-full bg-gray-700 text-white rounded-lg px-4 py-2 border focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors',
            Icon && 'pl-10',
            error ? 'border-red-500' : 'border-gray-600',
            disabled && 'opacity-50 cursor-not-allowed'
          )}
        />
      </div>
      {error && <p className="mt-1 text-sm text-red-500">{error}</p>}
    </div>
  );
};

export default Input;
```

### Step 10: Create Badge Component

**File: `src/components/shared/Badge.tsx`**
```typescript
import React from 'react';
import clsx from 'clsx';

interface BadgeProps {
  children: React.ReactNode;
  severity?: 'low' | 'medium' | 'high' | 'critical';
  variant?: 'solid' | 'outline';
  className?: string;
}

const Badge: React.FC<BadgeProps> = ({
  children,
  severity,
  variant = 'solid',
  className,
}) => {
  const severityColors = {
    low: variant === 'solid' 
      ? 'bg-green-500/20 text-green-400 border-green-500/50'
      : 'border-green-500 text-green-400',
    medium: variant === 'solid'
      ? 'bg-yellow-500/20 text-yellow-400 border-yellow-500/50'
      : 'border-yellow-500 text-yellow-400',
    high: variant === 'solid'
      ? 'bg-orange-500/20 text-orange-400 border-orange-500/50'
      : 'border-orange-500 text-orange-400',
    critical: variant === 'solid'
      ? 'bg-red-500/20 text-red-400 border-red-500/50'
      : 'border-red-500 text-red-400',
  };

  return (
    <span
      className={clsx(
        'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border',
        severity ? severityColors[severity] : 'bg-gray-700 text-gray-300 border-gray-600',
        className
      )}
    >
      {children}
    </span>
  );
};

export default Badge;
```

### Step 11: Create Loading Component

**File: `src/components/shared/Loading.tsx`**
```typescript
import React from 'react';
import { motion } from 'framer-motion';

interface LoadingProps {
  size?: 'sm' | 'md' | 'lg';
  text?: string;
}

const Loading: React.FC<LoadingProps> = ({ size = 'md', text }) => {
  const sizes = {
    sm: 'h-8 w-8',
    md: 'h-12 w-12',
    lg: 'h-16 w-16',
  };

  return (
    <div className="flex flex-col items-center justify-center space-y-4">
      <motion.div
        animate={{ rotate: 360 }}
        transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
        className={sizes[size]}
      >
        <svg viewBox="0 0 24 24" className="text-blue-500">
          <circle
            className="opacity-25"
            cx="12"
            cy="12"
            r="10"
            stroke="currentColor"
            strokeWidth="4"
            fill="none"
          />
          <path
            className="opacity-75"
            fill="currentColor"
            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
          />
        </svg>
      </motion.div>
      {text && <p className="text-gray-400 text-sm">{text}</p>}
    </div>
  );
};

export default Loading;
```

---

## Layout Components

### Step 12: Create Sidebar Component

**File: `src/components/layout/Sidebar.tsx`**
```typescript
import React from 'react';
import { NavLink } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
  HomeIcon,
  ShieldExclamationIcon,
  MagnifyingGlassIcon,
  ExclamationTriangleIcon,
  DocumentTextIcon,
  ChatBubbleLeftRightIcon,
} from '@heroicons/react/24/outline';

interface SidebarProps {
  isOpen: boolean;
  onToggle: () => void;
}

const navItems = [
  { name: 'Dashboard', icon: HomeIcon, path: '/dashboard' },
  { name: 'Phishing Detector', icon: ShieldExclamationIcon, path: '/phishing' },
  { name: 'OSINT Investigator', icon: MagnifyingGlassIcon, path: '/osint' },
  { name: 'Threat Intelligence', icon: ExclamationTriangleIcon, path: '/threat' },
  { name: 'Report Generator', icon: DocumentTextIcon, path: '/report' },
  { name: 'Chat Assistant', icon: ChatBubbleLeftRightIcon, path: '/chat' },
];

const Sidebar: React.FC<SidebarProps> = ({ isOpen, onToggle }) => {
  return (
    <motion.aside
      initial={false}
      animate={{ width: isOpen ? 256 : 64 }}
      className="bg-gray-800 border-r border-gray-700 flex flex-col"
    >
      <div className="p-4 border-b border-gray-700">
        <motion.div
          initial={false}
          animate={{ opacity: isOpen ? 1 : 0 }}
          className="flex items-center space-x-3"
        >
          <div className="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center">
            <span className="text-white font-bold text-xl">S</span>
          </div>
          {isOpen && (
            <div>
              <h2 className="text-white font-bold">SentinelX</h2>
              <p className="text-gray-400 text-xs">AI Security</p>
            </div>
          )}
        </motion.div>
      </div>

      <nav className="flex-1 p-4 space-y-2">
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              `flex items-center space-x-3 px-3 py-2 rounded-lg transition-colors ${
                isActive
                  ? 'bg-blue-600 text-white'
                  : 'text-gray-400 hover:bg-gray-700 hover:text-white'
              }`
            }
          >
            <item.icon className="w-6 h-6 flex-shrink-0" />
            {isOpen && <span className="font-medium">{item.name}</span>}
          </NavLink>
        ))}
      </nav>
    </motion.aside>
  );
};

export default Sidebar;
```

### Step 13: Create Header Component

**File: `src/components/layout/Header.tsx`**
```typescript
import React from 'react';
import { Bars3Icon, BellIcon } from '@heroicons/react/24/outline';

interface HeaderProps {
  onMenuClick: () => void;
}

const Header: React.FC<HeaderProps> = ({ onMenuClick }) => {
  return (
    <header className="bg-gray-800 border-b border-gray-700 px-6 py-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <button
            onClick={onMenuClick}
            className="lg:hidden text-gray-400 hover:text-white"
          >
            <Bars3Icon className="w-6 h-6" />
          </button>
          <h1 className="text-2xl font-bold text-white">
            {process.env.REACT_APP_NAME || 'SentinelX AI'}
          </h1>
        </div>

        <div className="flex items-center space-x-4">
          <button className="relative text-gray-400 hover:text-white">
            <BellIcon className="w-6 h-6" />
            <span className="absolute -top-1 -right-1 w-4 h-4 bg-red-500 rounded-full text-xs flex items-center justify-center text-white">
              3
            </span>
          </button>
          
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
              <span className="text-white text-sm font-bold">U</span>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
```

### Step 14: Create Layout Component

**File: `src/components/layout/Layout.tsx`**
```typescript
import React, { useState } from 'react';
import Sidebar from './Sidebar';
import Header from './Header';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const [sidebarOpen, setSidebarOpen] = useState(true);

  return (
    <div className="flex h-screen bg-gray-900">
      <Sidebar isOpen={sidebarOpen} onToggle={() => setSidebarOpen(!sidebarOpen)} />
      <div className="flex-1 flex flex-col overflow-hidden">
        <Header onMenuClick={() => setSidebarOpen(!sidebarOpen)} />
        <main className="flex-1 overflow-y-auto p-6">
          {children}
        </main>
      </div>
    </div>
  );
};

export default Layout;
```

---

## Routing Setup

### Step 15: Create App Component with Routing

**File: `src/App.tsx`**
```typescript
import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import Layout from './components/layout/Layout';
import Dashboard from './pages/Dashboard';
import PhishingDetector from './pages/PhishingDetector';
import OSINTInvestigator from './pages/OSINTInvestigator';
import ThreatIntelligence from './pages/ThreatIntelligence';
import ReportGenerator from './pages/ReportGenerator';
import ChatAssistant from './pages/ChatAssistant';

function App() {
  return (
    <BrowserRouter>
      <Toaster
        position="top-right"
        toastOptions={{
          duration: 4000,
          style: {
            background: '#1F2937',
            color: '#F9FAFB',
            border: '1px solid #374151',
          },
        }}
      />
      <Layout>
        <Routes>
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/phishing" element={<PhishingDetector />} />
          <Route path="/osint" element={<OSINTInvestigator />} />
          <Route path="/threat" element={<ThreatIntelligence />} />
          <Route path="/report" element={<ReportGenerator />} />
          <Route path="/chat" element={<ChatAssistant />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
}

export default App;
```

---

## Next Steps

This implementation guide provides the foundation for the SentinelX AI frontend. The next document will contain:

1. Complete page implementations for all 6 features
2. Feature-specific components
3. Advanced interactions and animations
4. Testing strategies
5. Deployment instructions

**Files Created So Far:**
- Project configuration (tailwind.config.js, .env)
- Type definitions (types/index.ts)
- API services (5 service files)
- Shared components (6 components)
- Layout components (3 components)
- App routing (App.tsx)

**Estimated Progress: 40% Complete**

Continue to Part 2 for page implementations and feature-specific components.