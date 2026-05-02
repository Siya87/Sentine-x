import React, { useState } from 'react';
import Input from '../shared/Input';
import Button from '../shared/Button';

interface EmailUploadProps {
  onAnalyze: (data: { sender: string; subject: string; body: string }) => void;
  isLoading: boolean;
}

const EmailUpload: React.FC<EmailUploadProps> = ({ onAnalyze, isLoading }) => {
  const [sender, setSender] = useState('');
  const [subject, setSubject] = useState('');
  const [body, setBody] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onAnalyze({ sender, subject, body });
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <Input
        label="Sender Email"
        type="email"
        value={sender}
        onChange={setSender}
        placeholder="suspicious@example.com"
        required
      />
      
      <Input
        label="Email Subject"
        type="text"
        value={subject}
        onChange={setSubject}
        placeholder="Urgent: Verify your account"
        required
      />
      
      <div>
        <label className="block text-sm font-medium text-gray-300 mb-2">
          Email Body
        </label>
        <textarea
          value={body}
          onChange={(e) => setBody(e.target.value)}
          placeholder="Paste the email content here..."
          rows={8}
          required
          className="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
      </div>

      <Button
        type="submit"
        variant="primary"
        isLoading={isLoading}
        className="w-full"
      >
        Analyze Email
      </Button>
    </form>
  );
};

export default EmailUpload;

// Made with Bob
