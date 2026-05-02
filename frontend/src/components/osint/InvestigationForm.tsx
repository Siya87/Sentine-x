import React, { useState } from 'react';
import Input from '../shared/Input';
import Button from '../shared/Button';

interface InvestigationFormProps {
  investigationType: string;
  onInvestigate: (target: string) => void;
  isLoading: boolean;
}

const InvestigationForm: React.FC<InvestigationFormProps> = ({
  investigationType,
  onInvestigate,
  isLoading,
}) => {
  const [target, setTarget] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onInvestigate(target);
  };

  const getPlaceholder = () => {
    switch (investigationType) {
      case 'email':
        return 'user@example.com';
      case 'username':
        return 'john_doe_123';
      case 'phone':
        return '+1 (555) 123-4567';
      case 'domain':
        return 'example.com';
      case 'ip':
        return '192.168.1.1';
      default:
        return 'Enter target...';
    }
  };

  const getLabel = () => {
    switch (investigationType) {
      case 'email':
        return 'Email Address';
      case 'username':
        return 'Username';
      case 'phone':
        return 'Phone Number';
      case 'domain':
        return 'Domain Name';
      case 'ip':
        return 'IP Address';
      default:
        return 'Target';
    }
  };

  const getInputType = () => {
    switch (investigationType) {
      case 'email':
        return 'email';
      case 'phone':
        return 'tel';
      default:
        return 'text';
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <Input
        label={getLabel()}
        type={getInputType()}
        value={target}
        onChange={setTarget}
        placeholder={getPlaceholder()}
        required
      />

      <div className="bg-gray-700/50 border border-gray-600 rounded-lg p-4">
        <h4 className="text-sm font-medium text-white mb-2">What we'll search:</h4>
        <ul className="text-sm text-gray-400 space-y-1">
          <li>• Data breach databases</li>
          <li>• Social media profiles</li>
          <li>• Public records</li>
          <li>• Domain/IP information</li>
          <li>• Reputation scores</li>
        </ul>
      </div>

      <Button
        type="submit"
        variant="primary"
        isLoading={isLoading}
        className="w-full"
      >
        Start Investigation
      </Button>
    </form>
  );
};

export default InvestigationForm;

// Made with Bob
