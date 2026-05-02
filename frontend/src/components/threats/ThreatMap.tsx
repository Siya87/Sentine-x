import React from 'react';
import { motion } from 'framer-motion';
import { Threat } from '../../types';

interface ThreatMapProps {
  threats: Threat[];
}

const ThreatMap: React.FC<ThreatMapProps> = ({ threats }) => {
  // Count threats by country
  const countryData = threats.reduce((acc, threat) => {
    const country = threat.geo_location?.country || 'Unknown';
    acc[country] = (acc[country] || 0) + 1;
    return acc;
  }, {} as Record<string, number>);

  // Sort by count
  const sortedCountries = Object.entries(countryData)
    .sort(([, a], [, b]) => b - a)
    .slice(0, 10);

  const maxCount = sortedCountries[0]?.[1] || 1;

  const getCountryFlag = (code: string) => {
    const flags: Record<string, string> = {
      US: '🇺🇸',
      CN: '🇨🇳',
      RU: '🇷🇺',
      KP: '🇰🇵',
      IR: '🇮🇷',
      BR: '🇧🇷',
      IN: '🇮🇳',
      UK: '🇬🇧',
      DE: '🇩🇪',
      FR: '🇫🇷',
      JP: '🇯🇵',
      KR: '🇰🇷',
    };
    return flags[code] || '🌍';
  };

  const getSeverityColor = (count: number) => {
    const percentage = (count / maxCount) * 100;
    if (percentage >= 75) return 'bg-red-500';
    if (percentage >= 50) return 'bg-orange-500';
    if (percentage >= 25) return 'bg-yellow-500';
    return 'bg-green-500';
  };

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="bg-gray-800 border border-gray-700 rounded-lg p-6"
    >
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-lg font-semibold text-white">Geographic Distribution</h3>
        <div className="flex items-center gap-2 text-sm text-gray-400">
          <span className="w-3 h-3 bg-red-500 rounded"></span>
          <span>High</span>
          <span className="w-3 h-3 bg-yellow-500 rounded ml-2"></span>
          <span>Medium</span>
          <span className="w-3 h-3 bg-green-500 rounded ml-2"></span>
          <span>Low</span>
        </div>
      </div>

      {/* World Map Placeholder */}
      <div className="relative bg-gray-900 rounded-lg p-8 mb-6 min-h-[300px] flex items-center justify-center">
        <div className="text-center">
          <svg className="w-24 h-24 mx-auto text-gray-700 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <p className="text-gray-500 text-sm">Interactive map visualization</p>
          <p className="text-gray-600 text-xs mt-1">Showing threat distribution across {sortedCountries.length} countries</p>
        </div>

        {/* Animated pulse indicators */}
        {sortedCountries.slice(0, 5).map((_, index) => (
          <motion.div
            key={index}
            className="absolute w-4 h-4 bg-red-500 rounded-full"
            style={{
              left: `${20 + index * 15}%`,
              top: `${30 + (index % 3) * 20}%`,
            }}
            animate={{
              scale: [1, 1.5, 1],
              opacity: [0.7, 1, 0.7],
            }}
            transition={{
              duration: 2,
              repeat: Infinity,
              delay: index * 0.2,
            }}
          />
        ))}
      </div>

      {/* Country List */}
      <div className="space-y-3">
        {sortedCountries.map(([country, count], index) => (
          <motion.div
            key={country}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: index * 0.05 }}
            className="flex items-center gap-3"
          >
            <span className="text-2xl">{getCountryFlag(country)}</span>
            <div className="flex-1">
              <div className="flex items-center justify-between mb-1">
                <span className="text-sm font-medium text-white">{country}</span>
                <span className="text-sm text-gray-400">{count} threats</span>
              </div>
              <div className="w-full bg-gray-700 rounded-full h-2 overflow-hidden">
                <motion.div
                  initial={{ width: 0 }}
                  animate={{ width: `${(count / maxCount) * 100}%` }}
                  transition={{ duration: 0.5, delay: index * 0.05 }}
                  className={`h-full ${getSeverityColor(count)}`}
                />
              </div>
            </div>
          </motion.div>
        ))}
      </div>

      {sortedCountries.length === 0 && (
        <div className="text-center py-8 text-gray-500">
          No geographic data available
        </div>
      )}
    </motion.div>
  );
};

export default ThreatMap;

// Made with Bob
