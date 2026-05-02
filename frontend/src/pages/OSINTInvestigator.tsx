import React, { useState } from 'react';
import { motion } from 'framer-motion';
import Card from '../components/shared/Card';
import Button from '../components/shared/Button';
import InvestigationTypeSelector from '../components/osint/InvestigationTypeSelector';
import InvestigationForm from '../components/osint/InvestigationForm';
import InvestigationResults from '../components/osint/InvestigationResults';
import { OSINTInvestigation } from '../types';
import { osintAPI } from '../services/api';
import toast from 'react-hot-toast';

const OSINTInvestigator: React.FC = () => {
  const [investigationType, setInvestigationType] = useState('email');
  const [isInvestigating, setIsInvestigating] = useState(false);
  const [results, setResults] = useState<OSINTInvestigation | null>(null);

  const handleInvestigate = async (target: string) => {
    try {
      if (!target.trim()) {
        toast.error('Please enter a search query');
        return;
      }

      setIsInvestigating(true);
      setResults(null);

      let response;

      // Call appropriate API based on investigation type
      switch (investigationType) {
        case 'email':
          response = await osintAPI.investigateEmail(target);
          break;
        case 'username':
          response = await osintAPI.investigateUsername(target);
          break;
        case 'phone':
          response = await osintAPI.investigatePhone(target);
          break;
        case 'domain':
          response = await osintAPI.investigateDomain(target);
          break;
        case 'ip':
          response = await osintAPI.investigateIP(target);
          break;
        default:
          throw new Error('Invalid investigation type');
      }

      setResults(response);
      toast.success('Investigation complete');

    } catch (error) {
      console.error('Error during investigation:', error);
      toast.error('Investigation failed. Please try again.');
    } finally {
      setIsInvestigating(false);
    }
  };

  const handleReset = () => {
    setResults(null);
    setInvestigationType('email');
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex items-center justify-between"
      >
        <div>
          <h1 className="text-2xl font-bold text-white mb-2">OSINT Investigator</h1>
          <p className="text-gray-400">Investigate usernames, emails, phone numbers, domains, and IPs</p>
        </div>
        {results && (
          <Button variant="outline" onClick={handleReset}>
            <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
            </svg>
            New Investigation
          </Button>
        )}
      </motion.div>

      {!results ? (
        /* Investigation Form */
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <Card>
            <InvestigationTypeSelector
              selectedType={investigationType}
              onTypeChange={setInvestigationType}
            />
            <InvestigationForm
              investigationType={investigationType}
              onInvestigate={handleInvestigate}
              isLoading={isInvestigating}
            />
          </Card>

          {/* Info Section */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
            <Card>
              <div className="flex items-start gap-3">
                <div className="w-10 h-10 bg-blue-500/20 rounded-lg flex items-center justify-center flex-shrink-0">
                  <svg className="w-5 h-5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                  </svg>
                </div>
                <div>
                  <h3 className="font-medium text-white mb-1">Comprehensive Search</h3>
                  <p className="text-sm text-gray-400">
                    Search across multiple databases and platforms simultaneously
                  </p>
                </div>
              </div>
            </Card>

            <Card>
              <div className="flex items-start gap-3">
                <div className="w-10 h-10 bg-purple-500/20 rounded-lg flex items-center justify-center flex-shrink-0">
                  <svg className="w-5 h-5 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                  </svg>
                </div>
                <div>
                  <h3 className="font-medium text-white mb-1">Breach Detection</h3>
                  <p className="text-sm text-gray-400">
                    Check if target appears in known data breaches
                  </p>
                </div>
              </div>
            </Card>

            <Card>
              <div className="flex items-start gap-3">
                <div className="w-10 h-10 bg-green-500/20 rounded-lg flex items-center justify-center flex-shrink-0">
                  <svg className="w-5 h-5 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                  </svg>
                </div>
                <div>
                  <h3 className="font-medium text-white mb-1">Risk Assessment</h3>
                  <p className="text-sm text-gray-400">
                    Automated risk scoring based on exposure level
                  </p>
                </div>
              </div>
            </Card>
          </div>
        </motion.div>
      ) : (
        /* Investigation Results */
        <InvestigationResults results={results} />
      )}
    </div>
  );
};

export default OSINTInvestigator;

// Made with Bob
