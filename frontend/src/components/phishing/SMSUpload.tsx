import React, { useState } from 'react';
import Input from '../shared/Input';
import Button from '../shared/Button';

interface SMSUploadProps {
  onAnalyze: (data: { phoneNumber: string; message: string }) => void;
  isLoading: boolean;
}

const SMSUpload: React.FC<SMSUploadProps> = ({ onAnalyze, isLoading }) => {
  const [phoneNumber, setPhoneNumber] = useState('');
  const [message, setMessage] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onAnalyze({ phoneNumber, message });
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <Input
        label="Sender Phone Number"
        type="tel"
        value={phoneNumber}
        onChange={setPhoneNumber}
        placeholder="+1 (555) 123-4567"
        required
      />
      
      <div>
        <label className="block text-sm font-medium text-gray-300 mb-2">
          SMS Message <span className="text-red-500">*</span>
        </label>
        <textarea
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Paste the SMS content here..."
          rows={6}
          required
          className="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
      </div>

      <div className="bg-yellow-500/10 border border-yellow-500/50 rounded-lg p-4">
        <div className="flex gap-3">
          <svg className="w-5 h-5 text-yellow-400 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
          <div>
            <h4 className="text-sm font-medium text-yellow-400 mb-1">Common SMS Scam Indicators</h4>
            <ul className="text-xs text-gray-400 space-y-1">
              <li>• Urgent action required messages</li>
              <li>• Requests for personal information</li>
              <li>• Suspicious links or shortened URLs</li>
              <li>• Prize or lottery winnings</li>
              <li>• Threats or intimidation</li>
            </ul>
          </div>
        </div>
      </div>

      <Button
        type="submit"
        variant="primary"
        isLoading={isLoading}
        className="w-full"
      >
        Analyze SMS
      </Button>
    </form>
  );
};

export default SMSUpload;

// Made with Bob
