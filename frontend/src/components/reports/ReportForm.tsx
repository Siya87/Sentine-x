import React from 'react';
import { motion } from 'framer-motion';
import Input from '../shared/Input';
import Button from '../shared/Button';

interface ReportFormData {
  title: string;
  incident_type: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  description: string;
  detection_time: string;
  affected_systems: string;
  indicators: string;
  attack_vector: string;
}

interface ReportFormProps {
  formData: ReportFormData;
  onChange: (field: keyof ReportFormData, value: string) => void;
  onNext: () => void;
}

const ReportForm: React.FC<ReportFormProps> = ({ formData, onChange, onNext }) => {
  const incidentTypes = [
    'Malware Infection',
    'Phishing Attack',
    'Ransomware',
    'Data Breach',
    'DDoS Attack',
    'Insider Threat',
    'Unauthorized Access',
    'Other',
  ];

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onNext();
  };

  return (
    <motion.form
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      onSubmit={handleSubmit}
      className="space-y-6"
    >
      <div className="bg-gray-800 border border-gray-700 rounded-lg p-6">
        <h3 className="text-lg font-semibold text-white mb-4">Basic Information</h3>
        
        <div className="space-y-4">
          <Input
            label="Report Title"
            value={formData.title}
            onChange={(value) => onChange('title', value)}
            placeholder="e.g., Ransomware Attack on Production Server"
            required
          />

          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Incident Type
            </label>
            <select
              value={formData.incident_type}
              onChange={(e) => onChange('incident_type', e.target.value)}
              className="w-full bg-gray-900 border border-gray-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            >
              <option value="">Select incident type</option>
              {incidentTypes.map((type) => (
                <option key={type} value={type}>
                  {type}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Severity Level
            </label>
            <div className="grid grid-cols-4 gap-2">
              {(['low', 'medium', 'high', 'critical'] as const).map((level) => (
                <button
                  key={level}
                  type="button"
                  onClick={() => onChange('severity', level)}
                  className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                    formData.severity === level
                      ? level === 'critical'
                        ? 'bg-red-500 text-white'
                        : level === 'high'
                        ? 'bg-orange-500 text-white'
                        : level === 'medium'
                        ? 'bg-yellow-500 text-white'
                        : 'bg-green-500 text-white'
                      : 'bg-gray-700 text-gray-400 hover:bg-gray-600'
                  }`}
                >
                  {level.toUpperCase()}
                </button>
              ))}
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Detection Time
            </label>
            <input
              type="datetime-local"
              value={formData.detection_time}
              onChange={(e) => onChange('detection_time', e.target.value)}
              className="w-full bg-gray-900 border border-gray-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>
        </div>
      </div>

      <div className="bg-gray-800 border border-gray-700 rounded-lg p-6">
        <h3 className="text-lg font-semibold text-white mb-4">Incident Details</h3>
        
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Description
            </label>
            <textarea
              value={formData.description}
              onChange={(e) => onChange('description', e.target.value)}
              placeholder="Provide a detailed description of the incident..."
              rows={4}
              className="w-full bg-gray-900 border border-gray-700 rounded-lg px-4 py-2 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>

          <Input
            label="Affected Systems"
            value={formData.affected_systems}
            onChange={(value) => onChange('affected_systems', value)}
            placeholder="e.g., web-server-01, database-prod, user-workstations (comma-separated)"
            required
          />

          <Input
            label="Indicators of Compromise (IOCs)"
            value={formData.indicators}
            onChange={(value) => onChange('indicators', value)}
            placeholder="e.g., malicious IPs, file hashes, domains (comma-separated)"
            required
          />

          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Attack Vector
            </label>
            <textarea
              value={formData.attack_vector}
              onChange={(e) => onChange('attack_vector', e.target.value)}
              placeholder="Describe how the attack was carried out..."
              rows={3}
              className="w-full bg-gray-900 border border-gray-700 rounded-lg px-4 py-2 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>
        </div>
      </div>

      <div className="flex justify-end">
        <Button type="submit" variant="primary">
          Next: Timeline & MITRE ATT&CK
        </Button>
      </div>
    </motion.form>
  );
};

export default ReportForm;

// Made with Bob
