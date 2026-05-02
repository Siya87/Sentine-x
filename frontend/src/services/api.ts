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

// ============================================
// API Service Functions
// ============================================

// Phishing Detection APIs
export const phishingAPI = {
  analyzeEmail: async (data: { sender: string; subject: string; body: string }) => {
    const response = await api.post('/api/phishing/analyze-email', data);
    return response.data;
  },
  
  analyzeURL: async (url: string) => {
    const response = await api.post('/api/phishing/analyze-url', { url });
    return response.data;
  },
  
  analyzeFile: async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await api.post('/api/phishing/analyze-file', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  },
  
  analyzeSMS: async (data: { sender: string; message: string }) => {
    const response = await api.post('/api/phishing/analyze-sms', data);
    return response.data;
  },
};

// OSINT Investigation APIs
export const osintAPI = {
  investigateEmail: async (email: string) => {
    const response = await api.post('/api/osint/investigate-email', { email });
    return response.data;
  },
  
  investigateUsername: async (username: string) => {
    const response = await api.post('/api/osint/investigate-username', { username });
    return response.data;
  },
  
  investigatePhone: async (phone: string) => {
    const response = await api.post('/api/osint/investigate-phone', { phone });
    return response.data;
  },
  
  investigateDomain: async (domain: string) => {
    const response = await api.post('/api/osint/investigate-domain', { domain });
    return response.data;
  },
  
  investigateIP: async (ip: string) => {
    const response = await api.post('/api/osint/investigate-ip', { ip });
    return response.data;
  },
};

// Threat Intelligence APIs
export const threatAPI = {
  getThreats: async (params?: {
    threat_type?: string;
    severity?: string;
    limit?: number;
    skip?: number;
  }) => {
    const response = await api.get('/api/threat/live', { params });
    return response.data;
  },
  
  getThreatById: async (threatId: string) => {
    const response = await api.get(`/api/threat/${threatId}`);
    return response.data;
  },
  
  getStatistics: async () => {
    const response = await api.get('/api/threat/stats/summary');
    return response.data;
  },
  
  searchThreats: async (query: string) => {
    const response = await api.get('/api/threat/search', { params: { query } });
    return response.data;
  },
};

// Report Generation APIs
export const reportAPI = {
  generateReport: async (data: {
    title: string;
    incident_type: string;
    severity: string;
    description: string;
    detection_time: string;
    affected_systems: string[];
    indicators: string[];
    attack_vector: string;
    mitre_techniques: Array<{ technique_id: string; tactic: string }>;
    timeline: Array<{ timestamp: string; event: string; description: string }>;
    mitigation_steps: string[];
  }) => {
    const response = await api.post('/api/reports/generate', data);
    return response.data;
  },
  
  getReports: async (params?: { limit?: number; skip?: number }) => {
    const response = await api.get('/api/reports', { params });
    return response.data;
  },
  
  getReportById: async (reportId: string) => {
    const response = await api.get(`/api/reports/${reportId}`);
    return response.data;
  },
  
  exportReportPDF: async (reportId: string) => {
    const response = await api.get(`/api/reports/${reportId}/export`, {
      responseType: 'blob',
    });
    return response.data;
  },
};

// Chat Assistant APIs
export const chatAPI = {
  sendMessage: async (data: { message: string; session_id?: string }) => {
    const response = await api.post('/api/chat/message', data);
    return response.data;
  },
  
  getSession: async (sessionId: string) => {
    const response = await api.get(`/api/chat/sessions/${sessionId}`);
    return response.data;
  },
  
  getSessions: async () => {
    const response = await api.get('/api/chat/sessions');
    return response.data;
  },
  
  searchKnowledgeBase: async (query: string) => {
    const response = await api.get('/api/chat/knowledge-base/search', {
      params: { query }
    });
    return response.data;
  },
  
  getKnowledgeBase: async () => {
    const response = await api.get('/api/chat/knowledge-base');
    return response.data;
  },
};

// Dashboard APIs
export const dashboardAPI = {
  getOverview: async () => {
    const response = await api.get('/api/dashboard/overview');
    return response.data;
  },
  
  getRecentActivity: async (limit: number = 10) => {
    const response = await api.get('/api/dashboard/activity', {
      params: { limit }
    });
    return response.data;
  },
  
  getThreatTrends: async (days: number = 7) => {
    const response = await api.get('/api/dashboard/trends', {
      params: { days }
    });
    return response.data;
  },
};

// Health Check
export const healthAPI = {
  check: async () => {
    const response = await api.get('/health');
    return response.data;
  },
};

// Made with Bob
