import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import Layout from './components/layout/Layout';
import Dashboard from './pages/Dashboard';
import PhishingDetector from './pages/PhishingDetector';
import OSINTInvestigator from './pages/OSINTInvestigator';
import ThreatIntelligence from './pages/ThreatIntelligence';
import ReportGenerator from './pages/ReportGenerator';
import ChatAssistant from './pages/ChatAssistant';

const App: React.FC = () => {
  return (
    <BrowserRouter>
      <Toaster
        position="top-right"
        toastOptions={{
          duration: 3000,
          style: {
            background: '#1f2937',
            color: '#fff',
          },
        }}
      />
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="phishing" element={<PhishingDetector />} />
          <Route path="osint" element={<OSINTInvestigator />} />
          <Route path="threats" element={<ThreatIntelligence />} />
          <Route path="reports" element={<ReportGenerator />} />
          <Route path="chat" element={<ChatAssistant />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
};

export default App;

// Made with Bob
