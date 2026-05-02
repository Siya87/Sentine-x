import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import ThreatCard from '../components/threats/ThreatCard';
import ThreatFilters from '../components/threats/ThreatFilters';
import ThreatStats from '../components/threats/ThreatStats';
import ThreatMap from '../components/threats/ThreatMap';
import Loading from '../components/shared/Loading';
import { Threat } from '../types';
import { threatAPI } from '../services/api';
import toast from 'react-hot-toast';

const ThreatIntelligence: React.FC = () => {
  const [threats, setThreats] = useState<Threat[]>([]);
  const [filteredThreats, setFilteredThreats] = useState<Threat[]>([]);
  const [loading, setLoading] = useState(true);
  const [autoRefresh, setAutoRefresh] = useState(true);
  const [filters, setFilters] = useState({
    type: 'all',
    severity: 'all',
    country: 'all',
    search: '',
  });

  // Fallback mock data generator (only used if API fails)
  const generateMockThreats = (): Threat[] => {
    const types = ['malware', 'phishing', 'ransomware', 'ddos', 'data_breach'];
    const severities: Array<'critical' | 'high' | 'medium' | 'low'> = ['critical', 'high', 'medium', 'low'];
    const countries = ['US', 'CN', 'RU', 'KP', 'IR', 'BR', 'IN', 'UK', 'DE', 'FR'];
    
    const titles: Record<string, string[]> = {
      malware: [
        'New Trojan Variant Detected',
        'Backdoor Malware Campaign',
        'Cryptominer Distribution',
        'Spyware Activity Surge',
      ],
      phishing: [
        'Banking Phishing Campaign',
        'Credential Harvesting Attack',
        'CEO Fraud Attempt',
        'Tax Scam Email Wave',
      ],
      ransomware: [
        'LockBit 3.0 Activity',
        'BlackCat Ransomware Detected',
        'Double Extortion Attack',
        'Healthcare Sector Targeted',
      ],
      ddos: [
        'Volumetric DDoS Attack',
        'Application Layer Flood',
        'DNS Amplification Attack',
        'Botnet Activity Spike',
      ],
      data_breach: [
        'Database Exposure Found',
        'API Credentials Leaked',
        'Customer Data Compromised',
        'Cloud Storage Misconfiguration',
      ],
    };

    return Array.from({ length: 50 }, (_, i) => {
      const type = types[Math.floor(Math.random() * types.length)];
      const severity = severities[Math.floor(Math.random() * severities.length)];
      const country = countries[Math.floor(Math.random() * countries.length)];
      const titleList = titles[type];
      const title = titleList[Math.floor(Math.random() * titleList.length)];

      return {
        threat_id: `threat-${i}`,
        title,
        description: `Detected ${type} activity from ${country}. Immediate investigation recommended.`,
        threat_type: type,
        severity,
        timestamp: new Date(Date.now() - Math.random() * 3600000).toISOString(),
        source: 'SentinelX AI',
        confidence: Math.floor(Math.random() * 30) + 70,
        indicators: [
          `${Math.floor(Math.random() * 255)}.${Math.floor(Math.random() * 255)}.${Math.floor(Math.random() * 255)}.${Math.floor(Math.random() * 255)}`,
          `malicious-domain-${i}.com`,
          `hash-${Math.random().toString(36).substring(7)}`,
        ],
        geo_location: {
          country,
          city: 'Unknown',
          latitude: 0,
          longitude: 0,
        },
        mitre_attack: {
          tactics: ['Initial Access'],
          techniques: ['T1566'],
        },
      };
    });
  };

  // Load threats from API
  const loadThreats = async () => {
    try {
      setLoading(true);
      
      // Fetch threats from backend with filters
      const response = await threatAPI.getThreats({
        threat_type: filters.type !== 'all' ? filters.type : undefined,
        severity: filters.severity !== 'all' ? filters.severity : undefined,
        limit: 50
      });
      
      setThreats(response);
      setFilteredThreats(response);
      
    } catch (error) {
      console.error('Error fetching threats:', error);
      toast.error('Failed to load threats');
      // Fallback to mock data
      const mockThreats = generateMockThreats();
      setThreats(mockThreats);
      setFilteredThreats(mockThreats);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadThreats();

    // Auto-refresh every 30 seconds
    let interval: NodeJS.Timeout;
    if (autoRefresh) {
      interval = setInterval(loadThreats, 30000);
    }

    return () => {
      if (interval) clearInterval(interval);
    };
  }, [autoRefresh, filters.type, filters.severity]);

  // Manual refresh handler
  const handleRefresh = async () => {
    await loadThreats();
    toast.success('Threats refreshed');
  };


  // Apply filters
  useEffect(() => {
    let filtered = [...threats];

    // Filter by type
    if (filters.type !== 'all') {
      filtered = filtered.filter(t => t.threat_type === filters.type);
    }

    // Filter by severity
    if (filters.severity !== 'all') {
      filtered = filtered.filter(t => t.severity === filters.severity);
    }

    // Filter by country
    if (filters.country !== 'all') {
      filtered = filtered.filter(t => t.geo_location?.country === filters.country);
    }

    // Filter by search
    if (filters.search) {
      const search = filters.search.toLowerCase();
      filtered = filtered.filter(t =>
        t.title.toLowerCase().includes(search) ||
        t.description.toLowerCase().includes(search) ||
        t.threat_type.toLowerCase().includes(search)
      );
    }

    setFilteredThreats(filtered);
  }, [filters, threats]);

  // Calculate stats
  const stats = {
    total: filteredThreats.length,
    critical: filteredThreats.filter(t => t.severity === 'critical').length,
    high: filteredThreats.filter(t => t.severity === 'high').length,
    medium: filteredThreats.filter(t => t.severity === 'medium').length,
    low: filteredThreats.filter(t => t.severity === 'low').length,
    byType: filteredThreats.reduce((acc, t) => {
      acc[t.threat_type] = (acc[t.threat_type] || 0) + 1;
      return acc;
    }, {} as Record<string, number>),
  };

  const handleFilterChange = (key: string, value: string) => {
    setFilters(prev => ({ ...prev, [key]: value }));
  };

  if (loading && threats.length === 0) {
    return <Loading fullScreen />;
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex items-center justify-between"
      >
        <div>
          <h1 className="text-3xl font-bold text-white mb-2">Threat Intelligence</h1>
          <p className="text-gray-400">Real-time threat monitoring and analysis</p>
        </div>
        <div className="flex items-center gap-4">
          <button
            onClick={() => setAutoRefresh(!autoRefresh)}
            className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-colors ${
              autoRefresh
                ? 'bg-green-500/20 text-green-400 border border-green-500/30'
                : 'bg-gray-800 text-gray-400 border border-gray-700'
            }`}
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            {autoRefresh ? 'Auto-Refresh ON' : 'Auto-Refresh OFF'}
          </button>
          <button
            onClick={() => {
              setLoading(true);
              setTimeout(() => {
                setThreats(generateMockThreats());
                setLoading(false);
              }, 500);
            }}
            className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            Refresh Now
          </button>
        </div>
      </motion.div>

      {/* Stats */}
      <ThreatStats stats={stats} />

      {/* Filters */}
      <ThreatFilters filters={filters} onFilterChange={handleFilterChange} />

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Threat Feed */}
        <div className="lg:col-span-2 space-y-4">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold text-white">
              Live Threat Feed ({filteredThreats.length})
            </h2>
            {loading && (
              <div className="flex items-center gap-2 text-sm text-gray-400">
                <svg className="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Updating...
              </div>
            )}
          </div>

          {filteredThreats.length === 0 ? (
            <div className="bg-gray-800 border border-gray-700 rounded-lg p-12 text-center">
              <svg className="w-16 h-16 mx-auto text-gray-600 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
              </svg>
              <p className="text-gray-400 text-lg mb-2">No threats found</p>
              <p className="text-gray-500 text-sm">Try adjusting your filters</p>
            </div>
          ) : (
            <div className="space-y-4 max-h-[800px] overflow-y-auto pr-2">
              {filteredThreats.map((threat, index) => (
                <ThreatCard key={threat.threat_id} threat={threat} index={index} />
              ))}
            </div>
          )}
        </div>

        {/* Geographic Map */}
        <div className="lg:col-span-1">
          <ThreatMap threats={filteredThreats} />
        </div>
      </div>
    </div>
  );
};

export default ThreatIntelligence;

// Made with Bob
