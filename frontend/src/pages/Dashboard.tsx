import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import StatCard from '../components/dashboard/StatCard';
import ThreatChart from '../components/dashboard/ThreatChart';
import ThreatDistribution from '../components/dashboard/ThreatDistribution';
import ActivityFeed from '../components/dashboard/ActivityFeed';
import Button from '../components/shared/Button';
import { dashboardAPI } from '../services/api';
import toast from 'react-hot-toast';

const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [statsData, setStatsData] = useState<any>(null);
  const [activityData, setActivityData] = useState<any[]>([]);

  // Fetch dashboard data on component mount
  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      
      // Fetch overview stats
      const overviewData = await dashboardAPI.getOverview();
      setStatsData(overviewData);
      
      // Fetch recent activity
      const recentActivity = await dashboardAPI.getRecentActivity(10);
      // Handle both array and object responses
      setActivityData(Array.isArray(recentActivity) ? recentActivity : (recentActivity?.activities || []));
      
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
      toast.error('Failed to load dashboard data');
      // Keep using mock data as fallback
    } finally {
      setLoading(false);
    }
  };

  const handleRefreshData = async () => {
    try {
      setLoading(true);
      
      // Fetch fresh data
      const overviewData = await dashboardAPI.getOverview();
      setStatsData(overviewData);
      
      const recentActivity = await dashboardAPI.getRecentActivity(10);
      // Handle both array and object responses
      setActivityData(Array.isArray(recentActivity) ? recentActivity : (recentActivity?.activities || []));
      
      toast.success('Dashboard refreshed successfully');
    } catch (error) {
      console.error('Error refreshing dashboard:', error);
      toast.error('Failed to refresh dashboard');
    } finally {
      setLoading(false);
    }
  };

  // Transform API data into stats array format
  const stats = statsData?.stats ? [
    {
      title: 'Threats Detected',
      value: statsData.stats.threats_detected?.toLocaleString() || '0',
      icon: (
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
      ),
      color: 'red' as const,
      trend: { value: Math.abs(statsData.stats.threats_change || 0), isPositive: (statsData.stats.threats_change || 0) < 0 },
    },
    {
      title: 'Phishing Attempts',
      value: statsData.stats.phishing_attempts?.toLocaleString() || '0',
      icon: (
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
        </svg>
      ),
      color: 'orange' as const,
      trend: { value: Math.abs(statsData.stats.phishing_change || 0), isPositive: (statsData.stats.phishing_change || 0) < 0 },
    },
    {
      title: 'Active Investigations',
      value: statsData.stats.active_investigations?.toLocaleString() || '0',
      icon: (
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
      ),
      color: 'blue' as const,
      trend: { value: Math.abs(statsData.stats.investigations_change || 0), isPositive: (statsData.stats.investigations_change || 0) > 0 },
    },
    {
      title: 'Reports Generated',
      value: statsData.stats.reports_generated?.toLocaleString() || '0',
      icon: (
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
      ),
      color: 'green' as const,
      trend: { value: Math.abs(statsData.stats.reports_change || 0), isPositive: (statsData.stats.reports_change || 0) > 0 },
    },
  ] : [
    {
      title: 'Threats Detected',
      value: '1,234',
      icon: (
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
      ),
      color: 'red' as const,
      trend: { value: 12, isPositive: false },
    },
    {
      title: 'Phishing Attempts',
      value: '567',
      icon: (
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
        </svg>
      ),
      color: 'orange' as const,
      trend: { value: 8, isPositive: false },
    },
    {
      title: 'Active Investigations',
      value: '89',
      icon: (
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
      ),
      color: 'blue' as const,
      trend: { value: 15, isPositive: true },
    },
    {
      title: 'Reports Generated',
      value: '342',
      icon: (
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
      ),
      color: 'green' as const,
      trend: { value: 23, isPositive: true },
    },
  ];

  const chartData = [
    { date: 'Mon', threats: 45, phishing: 20, malware: 15 },
    { date: 'Tue', threats: 52, phishing: 25, malware: 18 },
    { date: 'Wed', threats: 48, phishing: 22, malware: 16 },
    { date: 'Thu', threats: 61, phishing: 30, malware: 21 },
    { date: 'Fri', threats: 55, phishing: 28, malware: 17 },
    { date: 'Sat', threats: 38, phishing: 18, malware: 12 },
    { date: 'Sun', threats: 42, phishing: 20, malware: 14 },
  ];

  const distributionData = [
    { name: 'Phishing', value: 567, color: '#f59e0b' },
    { name: 'Malware', value: 342, color: '#ef4444' },
    { name: 'Ransomware', value: 156, color: '#8b5cf6' },
    { name: 'DDoS', value: 89, color: '#3b82f6' },
    { name: 'Data Breach', value: 80, color: '#10b981' },
  ];

  // Use API data if available, otherwise use mock data
  const activities = activityData.length > 0 ? activityData : [
    {
      id: '1',
      type: 'threat' as const,
      title: 'Critical Threat Detected',
      description: 'Suspicious activity from IP 192.168.1.100',
      timestamp: '5 minutes ago',
      severity: 'critical' as const,
    },
    {
      id: '2',
      type: 'phishing' as const,
      title: 'Phishing Email Blocked',
      description: 'Attempted phishing attack targeting finance@company.com',
      timestamp: '15 minutes ago',
      severity: 'high' as const,
    },
    {
      id: '3',
      type: 'investigation' as const,
      title: 'OSINT Investigation Completed',
      description: 'Username investigation for "suspicious_user_123"',
      timestamp: '1 hour ago',
      severity: 'medium' as const,
    },
    {
      id: '4',
      type: 'report' as const,
      title: 'Incident Report Generated',
      description: 'Security incident report for case #2024-001',
      timestamp: '2 hours ago',
      severity: 'low' as const,
    },
    {
      id: '5',
      type: 'threat' as const,
      title: 'Malware Signature Updated',
      description: 'New malware signatures added to database',
      timestamp: '3 hours ago',
    },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex items-center justify-between"
      >
        <div>
          <h1 className="text-2xl font-bold text-white mb-2">Dashboard</h1>
          <p className="text-gray-400">Overview of your cyber intelligence operations</p>
        </div>
        <Button
          variant="primary"
          onClick={handleRefreshData}
          disabled={loading}
        >
          <svg
            className={`w-5 h-5 mr-2 ${loading ? 'animate-spin' : ''}`}
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          {loading ? 'Refreshing...' : 'Refresh Data'}
        </Button>
      </motion.div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {stats.map((stat: any, index: number) => (
          <StatCard key={index} {...stat} />
        ))}
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <ThreatChart data={chartData} />
        </div>
        <div>
          <ThreatDistribution data={distributionData} />
        </div>
      </div>

      {/* Activity Feed */}
      <ActivityFeed activities={activities} />

      {/* Quick Actions */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        className="bg-gray-800 border border-gray-700 rounded-lg p-6"
      >
        <h3 className="text-lg font-semibold text-white mb-4">Quick Actions</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <Button
            variant="outline"
            className="justify-start"
            onClick={() => navigate('/threats')}
          >
            <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
            Scan for Threats
          </Button>
          <Button
            variant="outline"
            className="justify-start"
            onClick={() => navigate('/osint')}
          >
            <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
            Start Investigation
          </Button>
          <Button
            variant="outline"
            className="justify-start"
            onClick={() => navigate('/reports')}
          >
            <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            Generate Report
          </Button>
          <Button
            variant="outline"
            className="justify-start"
            onClick={() => navigate('/chat')}
          >
            <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
            </svg>
            Ask AI Assistant
          </Button>
        </div>
      </motion.div>
    </div>
  );
};

export default Dashboard;

// Made with Bob
