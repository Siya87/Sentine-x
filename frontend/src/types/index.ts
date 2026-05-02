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
export interface ThreatIndicator {
  type: string;
  value: string;
  confidence: number;
  first_seen: string;
  last_seen: string;
  tags: string[];
}

export interface Threat {
  threat_id: string;
  threat_type: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  title: string;
  description: string;
  source: string;
  timestamp: string;
  indicators: ThreatIndicator[] | string[]; // Support both formats for backward compatibility
  geo_location?: {
    country: string;
    city?: string;
    latitude?: number;
    longitude?: number;
  };
  confidence?: number;
  mitre_attack?: {
    tactics: string[];
    techniques: string[];
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

// Made with Bob
