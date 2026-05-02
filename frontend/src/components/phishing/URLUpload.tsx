import React, { useState } from 'react';
import Input from '../shared/Input';
import Button from '../shared/Button';

interface URLUploadProps {
  onAnalyze: (data: { url: string }) => void;
  isLoading: boolean;
}

const URLUpload: React.FC<URLUploadProps> = ({ onAnalyze, isLoading }) => {
  const [url, setUrl] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onAnalyze({ url });
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <Input
        label="Suspicious URL"
        type="url"
        value={url}
        onChange={setUrl}
        placeholder="https://suspicious-site.com/verify"
        required
      />
      
      <div className="bg-gray-700/50 border border-gray-600 rounded-lg p-4">
        <h4 className="text-sm font-medium text-white mb-2">What we check:</h4>
        <ul className="text-sm text-gray-400 space-y-1">
          <li>• Domain reputation and age</li>
          <li>• SSL certificate validity</li>
          <li>• Known phishing patterns</li>
          <li>• Malicious content detection</li>
          <li>• Redirect chains analysis</li>
        </ul>
      </div>

      <Button
        type="submit"
        variant="primary"
        isLoading={isLoading}
        className="w-full"
      >
        Analyze URL
      </Button>
    </form>
  );
};

export default URLUpload;

// Made with Bob
