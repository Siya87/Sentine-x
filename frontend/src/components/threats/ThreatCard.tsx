import React from 'react';
import { motion } from 'framer-motion';
import Badge from '../shared/Badge';
import { Threat } from '../../types';

interface ThreatCardProps {
  threat: Threat;
  index: number;
}

const ThreatCard: React.FC<ThreatCardProps> = ({ threat, index }) => {
  const getTypeIcon = (type: string) => {
    switch (type.toLowerCase()) {
      case 'malware':
        return (
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
        );
      case 'phishing':
        return (
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
          </svg>
        );
      case 'ransomware':
        return (
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
          </svg>
        );
      case 'ddos':
        return (
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
        );
      default:
        return (
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
          </svg>
        );
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.05 }}
      className="bg-gray-800 border border-gray-700 rounded-lg p-4 hover:border-gray-600 transition-colors"
    >
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-start gap-3 flex-1">
          <div className={`w-10 h-10 rounded-lg flex items-center justify-center flex-shrink-0 ${
            threat.severity === 'critical' ? 'bg-red-500/20 text-red-400' :
            threat.severity === 'high' ? 'bg-orange-500/20 text-orange-400' :
            threat.severity === 'medium' ? 'bg-yellow-500/20 text-yellow-400' :
            'bg-green-500/20 text-green-400'
          }`}>
            {getTypeIcon(threat.threat_type)}
          </div>
          <div className="flex-1 min-w-0">
            <h3 className="font-medium text-white mb-1 truncate">{threat.title}</h3>
            <p className="text-sm text-gray-400 line-clamp-2">{threat.description}</p>
          </div>
        </div>
        <Badge severity={threat.severity}>
          {threat.severity.toUpperCase()}
        </Badge>
      </div>

      <div className="flex items-center justify-between text-xs text-gray-500">
        <div className="flex items-center gap-4">
          <span className="flex items-center gap-1">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
            </svg>
            {threat.threat_type}
          </span>
          <span className="flex items-center gap-1">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
            {threat.geo_location?.country || 'Unknown'}
          </span>
        </div>
        <span>{new Date(threat.timestamp).toLocaleTimeString()}</span>
      </div>

      {threat.indicators && threat.indicators.length > 0 && (
        <div className="mt-3 pt-3 border-t border-gray-700">
          <p className="text-xs text-gray-500 mb-2">Indicators:</p>
          <div className="flex flex-wrap gap-1">
            {threat.indicators.slice(0, 3).map((indicator, idx) => (
              <span
                key={idx}
                className="px-2 py-1 bg-gray-700 text-gray-300 text-xs rounded font-mono"
                title={typeof indicator === 'object' ? `${indicator.type}: ${indicator.value}` : indicator}
              >
                {typeof indicator === 'object' ? indicator.value : indicator}
              </span>
            ))}
            {threat.indicators.length > 3 && (
              <span className="px-2 py-1 bg-gray-700 text-gray-400 text-xs rounded">
                +{threat.indicators.length - 3} more
              </span>
            )}
          </div>
        </div>
      )}
    </motion.div>
  );
};

export default ThreatCard;

// Made with Bob
