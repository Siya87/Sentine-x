import React from 'react';
import { motion } from 'framer-motion';

interface ThreatFiltersProps {
  filters: {
    type: string;
    severity: string;
    country: string;
    search: string;
  };
  onFilterChange: (key: string, value: string) => void;
}

const ThreatFilters: React.FC<ThreatFiltersProps> = ({ filters, onFilterChange }) => {
  const threatTypes = ['all', 'malware', 'phishing', 'ransomware', 'ddos', 'data_breach'];
  const severityLevels = ['all', 'critical', 'high', 'medium', 'low'];
  const countries = ['all', 'US', 'CN', 'RU', 'KP', 'IR', 'BR', 'IN', 'UK', 'DE'];

  return (
    <motion.div
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-gray-800 border border-gray-700 rounded-lg p-4 mb-6"
    >
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Search */}
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">
            Search
          </label>
          <div className="relative">
            <input
              type="text"
              value={filters.search}
              onChange={(e) => onFilterChange('search', e.target.value)}
              placeholder="Search threats..."
              className="w-full bg-gray-900 border border-gray-700 rounded-lg px-4 py-2 pl-10 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <svg
              className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-500"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </div>
        </div>

        {/* Threat Type */}
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">
            Threat Type
          </label>
          <select
            value={filters.type}
            onChange={(e) => onFilterChange('type', e.target.value)}
            className="w-full bg-gray-900 border border-gray-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            {threatTypes.map((type) => (
              <option key={type} value={type}>
                {type === 'all' ? 'All Types' : type.replace('_', ' ').toUpperCase()}
              </option>
            ))}
          </select>
        </div>

        {/* Severity */}
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">
            Severity
          </label>
          <select
            value={filters.severity}
            onChange={(e) => onFilterChange('severity', e.target.value)}
            className="w-full bg-gray-900 border border-gray-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            {severityLevels.map((level) => (
              <option key={level} value={level}>
                {level === 'all' ? 'All Severities' : level.toUpperCase()}
              </option>
            ))}
          </select>
        </div>

        {/* Country */}
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">
            Country
          </label>
          <select
            value={filters.country}
            onChange={(e) => onFilterChange('country', e.target.value)}
            className="w-full bg-gray-900 border border-gray-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            {countries.map((country) => (
              <option key={country} value={country}>
                {country === 'all' ? 'All Countries' : country}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Active Filters Summary */}
      {(filters.type !== 'all' || filters.severity !== 'all' || filters.country !== 'all' || filters.search) && (
        <div className="mt-4 pt-4 border-t border-gray-700">
          <div className="flex items-center justify-between">
            <div className="flex flex-wrap gap-2">
              {filters.type !== 'all' && (
                <span className="px-3 py-1 bg-blue-500/20 text-blue-400 text-sm rounded-full flex items-center gap-2">
                  Type: {filters.type}
                  <button
                    onClick={() => onFilterChange('type', 'all')}
                    className="hover:text-blue-300"
                  >
                    ×
                  </button>
                </span>
              )}
              {filters.severity !== 'all' && (
                <span className="px-3 py-1 bg-orange-500/20 text-orange-400 text-sm rounded-full flex items-center gap-2">
                  Severity: {filters.severity}
                  <button
                    onClick={() => onFilterChange('severity', 'all')}
                    className="hover:text-orange-300"
                  >
                    ×
                  </button>
                </span>
              )}
              {filters.country !== 'all' && (
                <span className="px-3 py-1 bg-green-500/20 text-green-400 text-sm rounded-full flex items-center gap-2">
                  Country: {filters.country}
                  <button
                    onClick={() => onFilterChange('country', 'all')}
                    className="hover:text-green-300"
                  >
                    ×
                  </button>
                </span>
              )}
              {filters.search && (
                <span className="px-3 py-1 bg-purple-500/20 text-purple-400 text-sm rounded-full flex items-center gap-2">
                  Search: "{filters.search}"
                  <button
                    onClick={() => onFilterChange('search', '')}
                    className="hover:text-purple-300"
                  >
                    ×
                  </button>
                </span>
              )}
            </div>
            <button
              onClick={() => {
                onFilterChange('type', 'all');
                onFilterChange('severity', 'all');
                onFilterChange('country', 'all');
                onFilterChange('search', '');
              }}
              className="text-sm text-gray-400 hover:text-white transition-colors"
            >
              Clear All
            </button>
          </div>
        </div>
      )}
    </motion.div>
  );
};

export default ThreatFilters;

// Made with Bob
