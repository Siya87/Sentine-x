import React from 'react';
import { motion } from 'framer-motion';
import Card from '../shared/Card';
import Badge from '../shared/Badge';
import { PhishingAnalysis } from '../../types';

interface AnalysisResultsProps {
  results: PhishingAnalysis;
}

const AnalysisResults: React.FC<AnalysisResultsProps> = ({ results }) => {
  const getThreatColor = (score: number) => {
    if (score >= 80) return 'critical';
    if (score >= 60) return 'high';
    if (score >= 40) return 'medium';
    return 'low';
  };

  const getThreatLabel = (score: number) => {
    if (score >= 80) return 'Critical Threat';
    if (score >= 60) return 'High Risk';
    if (score >= 40) return 'Medium Risk';
    return 'Low Risk';
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-6"
    >
      {/* Threat Score */}
      <Card>
        <div className="text-center py-8">
          <div className="relative inline-flex items-center justify-center w-32 h-32 mb-4">
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
                strokeDashoffset={`${2 * Math.PI * 56 * (1 - results.threat_score / 100)}`}
                className={`${
                  results.threat_score >= 80 ? 'text-red-500' :
                  results.threat_score >= 60 ? 'text-orange-500' :
                  results.threat_score >= 40 ? 'text-yellow-500' :
                  'text-green-500'
                } transition-all duration-1000`}
                strokeLinecap="round"
              />
            </svg>
            <div className="absolute inset-0 flex flex-col items-center justify-center">
              <span className="text-4xl font-bold text-white">{results.threat_score}</span>
              <span className="text-sm text-gray-400">/ 100</span>
            </div>
          </div>
          <h3 className="text-xl font-semibold text-white mb-2">
            {getThreatLabel(results.threat_score)}
          </h3>
          <Badge severity={getThreatColor(results.threat_score) as any}>
            {results.is_phishing ? 'PHISHING DETECTED' : 'SAFE'}
          </Badge>
        </div>
      </Card>

      {/* Analysis Details */}
      <Card title="Analysis Details">
        <div className="space-y-4">
          <div>
            <h4 className="text-sm font-medium text-gray-400 mb-2">Summary</h4>
            <p className="text-white">{results.explanation}</p>
          </div>
          
          {results.indicators && results.indicators.length > 0 && (
            <div>
              <h4 className="text-sm font-medium text-gray-400 mb-2">Threat Indicators</h4>
              <ul className="space-y-2">
                {results.indicators.map((indicator, index) => (
                  <li key={index} className="flex items-start gap-2 text-sm">
                    <svg className="w-5 h-5 text-red-400 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                    </svg>
                    <span className="text-gray-300">{indicator.description}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </Card>

      {/* Recommendations */}
      {results.recommendations && results.recommendations.length > 0 && (
        <Card title="Recommended Actions">
          <ul className="space-y-3">
            {results.recommendations.map((recommendation, index) => (
              <li key={index} className="flex items-start gap-3">
                <div className="w-6 h-6 rounded-full bg-blue-500/20 flex items-center justify-center flex-shrink-0 mt-0.5">
                  <span className="text-xs font-bold text-blue-400">{index + 1}</span>
                </div>
                <span className="text-gray-300">{recommendation}</span>
              </li>
            ))}
          </ul>
        </Card>
      )}

    </motion.div>
  );
};

export default AnalysisResults;

// Made with Bob
