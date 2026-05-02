import React from 'react';
import { motion } from 'framer-motion';
import Card from '../shared/Card';
import Badge from '../shared/Badge';
import { OSINTInvestigation } from '../../types';

interface InvestigationResultsProps {
  results: OSINTInvestigation;
}

const InvestigationResults: React.FC<InvestigationResultsProps> = ({ results }) => {
  const getRiskColor = (score: number) => {
    if (score >= 75) return 'critical';
    if (score >= 50) return 'high';
    if (score >= 25) return 'medium';
    return 'low';
  };

  const getRiskLabel = (score: number) => {
    if (score >= 75) return 'Critical Risk';
    if (score >= 50) return 'High Risk';
    if (score >= 25) return 'Medium Risk';
    return 'Low Risk';
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-6"
    >
      {/* Risk Score */}
      <Card>
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-lg font-semibold text-white mb-2">Investigation Summary</h3>
            <p className="text-gray-400 mb-4">{results.summary}</p>
            <div className="flex items-center gap-3">
              <span className="text-sm text-gray-400">Risk Score:</span>
              <Badge severity={getRiskColor(results.risk_score) as any}>
                {getRiskLabel(results.risk_score)}
              </Badge>
              <span className="text-2xl font-bold text-white">{results.risk_score}/100</span>
            </div>
          </div>
          <div className="relative w-32 h-32">
            <svg className="w-32 h-32 transform -rotate-90">
              <circle
                cx="64"
                cy="64"
                r="56"
                stroke="currentColor"
                strokeWidth="8"
                fill="none"
                className="text-gray-700"
              />
              <circle
                cx="64"
                cy="64"
                r="56"
                stroke="currentColor"
                strokeWidth="8"
                fill="none"
                strokeDasharray={`${2 * Math.PI * 56}`}
                strokeDashoffset={`${2 * Math.PI * 56 * (1 - results.risk_score / 100)}`}
                className={`${
                  results.risk_score >= 75 ? 'text-red-500' :
                  results.risk_score >= 50 ? 'text-orange-500' :
                  results.risk_score >= 25 ? 'text-yellow-500' :
                  'text-green-500'
                } transition-all duration-1000`}
                strokeLinecap="round"
              />
            </svg>
          </div>
        </div>
      </Card>

      {/* Breach Data */}
      {results.breach_data && results.breach_data.length > 0 && (
        <Card title={`Data Breaches (${results.breach_data.length})`}>
          <div className="space-y-4">
            {results.breach_data.map((breach, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1 }}
                className="p-4 bg-red-500/10 border border-red-500/50 rounded-lg"
              >
                <div className="flex items-start justify-between mb-2">
                  <h4 className="font-medium text-white">{breach.name}</h4>
                  <Badge severity="critical">BREACH</Badge>
                </div>
                <p className="text-sm text-gray-400 mb-2">{breach.description}</p>
                <div className="flex items-center gap-4 text-xs text-gray-500">
                  <span>Domain: {breach.domain}</span>
                  <span>Date: {new Date(breach.breach_date).toLocaleDateString()}</span>
                </div>
                {breach.data_classes && breach.data_classes.length > 0 && (
                  <div className="mt-3 flex flex-wrap gap-2">
                    {breach.data_classes.map((dataClass, idx) => (
                      <span
                        key={idx}
                        className="px-2 py-1 bg-gray-700 text-gray-300 text-xs rounded"
                      >
                        {dataClass}
                      </span>
                    ))}
                  </div>
                )}
              </motion.div>
            ))}
          </div>
        </Card>
      )}

      {/* Social Profiles */}
      {results.social_profiles && results.social_profiles.length > 0 && (
        <Card title={`Social Media Profiles (${results.social_profiles.length})`}>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {results.social_profiles.map((profile, index) => (
              <motion.a
                key={index}
                href={profile.url}
                target="_blank"
                rel="noopener noreferrer"
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: index * 0.1 }}
                className="p-4 bg-gray-700/50 border border-gray-600 rounded-lg hover:border-blue-500 transition-colors"
              >
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 bg-blue-500/20 rounded-lg flex items-center justify-center">
                    <svg className="w-5 h-5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                    </svg>
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="font-medium text-white truncate">{profile.platform}</p>
                    <p className="text-sm text-gray-400 truncate">@{profile.username}</p>
                    {profile.followers !== undefined && (
                      <p className="text-xs text-gray-500">{profile.followers} followers</p>
                    )}
                  </div>
                  <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                  </svg>
                </div>
              </motion.a>
            ))}
          </div>
        </Card>
      )}

      {/* IP Information */}
      {results.ip_info && (
        <Card title="IP Information">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="p-4 bg-gray-700/50 rounded-lg">
              <p className="text-sm text-gray-400 mb-1">Country</p>
              <p className="text-white font-medium">{results.ip_info.country || 'Unknown'}</p>
            </div>
            <div className="p-4 bg-gray-700/50 rounded-lg">
              <p className="text-sm text-gray-400 mb-1">City</p>
              <p className="text-white font-medium">{results.ip_info.city || 'Unknown'}</p>
            </div>
            <div className="p-4 bg-gray-700/50 rounded-lg">
              <p className="text-sm text-gray-400 mb-1">ISP</p>
              <p className="text-white font-medium">{results.ip_info.isp || 'Unknown'}</p>
            </div>
            <div className="p-4 bg-gray-700/50 rounded-lg">
              <p className="text-sm text-gray-400 mb-1">Organization</p>
              <p className="text-white font-medium">{results.ip_info.org || 'Unknown'}</p>
            </div>
          </div>
        </Card>
      )}

      {/* Investigation Details */}
      <Card title="Investigation Details">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div>
            <p className="text-sm text-gray-400 mb-1">Investigation ID</p>
            <p className="text-white font-mono text-sm">{results.investigation_id}</p>
          </div>
          <div>
            <p className="text-sm text-gray-400 mb-1">Target</p>
            <p className="text-white font-medium">{results.target}</p>
          </div>
          <div>
            <p className="text-sm text-gray-400 mb-1">Type</p>
            <Badge>{results.investigation_type.toUpperCase()}</Badge>
          </div>
          <div>
            <p className="text-sm text-gray-400 mb-1">Created</p>
            <p className="text-white text-sm">{new Date(results.created_at).toLocaleString()}</p>
          </div>
        </div>
      </Card>
    </motion.div>
  );
};

export default InvestigationResults;

// Made with Bob
