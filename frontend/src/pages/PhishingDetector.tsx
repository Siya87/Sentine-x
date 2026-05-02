import React, { useState } from 'react';
import { motion } from 'framer-motion';
import Card from '../components/shared/Card';
import Button from '../components/shared/Button';
import UploadTabs from '../components/phishing/UploadTabs';
import EmailUpload from '../components/phishing/EmailUpload';
import URLUpload from '../components/phishing/URLUpload';
import FileUpload from '../components/phishing/FileUpload';
import SMSUpload from '../components/phishing/SMSUpload';
import AnalysisResults from '../components/phishing/AnalysisResults';
import { PhishingAnalysis } from '../types';
import { phishingAPI } from '../services/api';
import toast from 'react-hot-toast';

const PhishingDetector: React.FC = () => {
  const [activeTab, setActiveTab] = useState('email');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [results, setResults] = useState<PhishingAnalysis | null>(null);

  const handleAnalyze = async (data: any) => {
    try {
      setIsAnalyzing(true);
      setResults(null);
      
      let response;
      
      // Call appropriate API based on active tab
      switch (activeTab) {
        case 'email':
          // Validate email data
          if (!data.sender || !data.subject || !data.body) {
            toast.error('Please fill in all email fields');
            return;
          }
          response = await phishingAPI.analyzeEmail({
            sender: data.sender,
            subject: data.subject,
            body: data.body
          });
          break;
          
        case 'url':
          // Validate URL
          if (!data.url) {
            toast.error('Please enter a URL');
            return;
          }
          response = await phishingAPI.analyzeURL(data.url);
          break;
          
        case 'file':
          // Validate file
          if (!data.file) {
            toast.error('Please select a file');
            return;
          }
          response = await phishingAPI.analyzeFile(data.file);
          break;
          
        case 'sms':
          // Validate SMS data
          if (!data.sender || !data.message) {
            toast.error('Please fill in all SMS fields');
            return;
          }
          response = await phishingAPI.analyzeSMS({
            sender: data.sender,
            message: data.message
          });
          break;
          
        default:
          throw new Error('Invalid analysis type');
      }
      
      setResults(response);
      toast.success('Analysis complete');
      
    } catch (error) {
      console.error('Error analyzing:', error);
      toast.error('Analysis failed. Please try again.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleReset = () => {
    setResults(null);
    setActiveTab('email');
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
          <h1 className="text-2xl font-bold text-white mb-2">Phishing Detector</h1>
          <p className="text-gray-400">Analyze emails, URLs, files, and SMS for phishing threats</p>
        </div>
        {results && (
          <Button variant="outline" onClick={handleReset}>
            <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
            </svg>
            New Analysis
          </Button>
        )}
      </motion.div>

      {!results ? (
        /* Upload Form */
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <Card>
            <UploadTabs activeTab={activeTab} onTabChange={setActiveTab} />
            
            <div className="mt-6">
              {activeTab === 'email' && (
                <EmailUpload onAnalyze={handleAnalyze} isLoading={isAnalyzing} />
              )}
              {activeTab === 'url' && (
                <URLUpload onAnalyze={handleAnalyze} isLoading={isAnalyzing} />
              )}
              {activeTab === 'file' && (
                <FileUpload onAnalyze={handleAnalyze} isLoading={isAnalyzing} />
              )}
              {activeTab === 'sms' && (
                <SMSUpload onAnalyze={handleAnalyze} isLoading={isAnalyzing} />
              )}
            </div>
          </Card>

          {/* Info Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
            <Card>
              <div className="flex items-start gap-3">
                <div className="w-10 h-10 bg-blue-500/20 rounded-lg flex items-center justify-center flex-shrink-0">
                  <svg className="w-5 h-5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                  </svg>
                </div>
                <div>
                  <h3 className="font-medium text-white mb-1">AI-Powered Analysis</h3>
                  <p className="text-sm text-gray-400">
                    Advanced machine learning models detect sophisticated phishing attempts
                  </p>
                </div>
              </div>
            </Card>

            <Card>
              <div className="flex items-start gap-3">
                <div className="w-10 h-10 bg-purple-500/20 rounded-lg flex items-center justify-center flex-shrink-0">
                  <svg className="w-5 h-5 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                </div>
                <div>
                  <h3 className="font-medium text-white mb-1">Real-Time Results</h3>
                  <p className="text-sm text-gray-400">
                    Get instant threat analysis and actionable recommendations
                  </p>
                </div>
              </div>
            </Card>

            <Card>
              <div className="flex items-start gap-3">
                <div className="w-10 h-10 bg-green-500/20 rounded-lg flex items-center justify-center flex-shrink-0">
                  <svg className="w-5 h-5 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                  </svg>
                </div>
                <div>
                  <h3 className="font-medium text-white mb-1">Multi-Source Detection</h3>
                  <p className="text-sm text-gray-400">
                    Integrates with VirusTotal and threat intelligence databases
                  </p>
                </div>
              </div>
            </Card>
          </div>
        </motion.div>
      ) : (
        /* Analysis Results */
        <AnalysisResults results={results} />
      )}
    </div>
  );
};

export default PhishingDetector;

// Made with Bob
