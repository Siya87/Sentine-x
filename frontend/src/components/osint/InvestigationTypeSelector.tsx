import React from 'react';
import { motion } from 'framer-motion';
import clsx from 'clsx';

interface InvestigationType {
  id: string;
  label: string;
  icon: React.ReactNode;
  description: string;
}

interface InvestigationTypeSelectorProps {
  selectedType: string;
  onTypeChange: (type: string) => void;
}

const InvestigationTypeSelector: React.FC<InvestigationTypeSelectorProps> = ({
  selectedType,
  onTypeChange,
}) => {
  const types: InvestigationType[] = [
    {
      id: 'email',
      label: 'Email',
      description: 'Investigate email addresses',
      icon: (
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
        </svg>
      ),
    },
    {
      id: 'username',
      label: 'Username',
      description: 'Search across platforms',
      icon: (
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
        </svg>
      ),
    },
    {
      id: 'phone',
      label: 'Phone',
      description: 'Lookup phone numbers',
      icon: (
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
        </svg>
      ),
    },
    {
      id: 'domain',
      label: 'Domain',
      description: 'Analyze domain info',
      icon: (
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" />
        </svg>
      ),
    },
    {
      id: 'ip',
      label: 'IP Address',
      description: 'Geolocate and analyze',
      icon: (
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z" />
        </svg>
      ),
    },
  ];

  return (
    <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-6">
      {types.map((type) => (
        <motion.button
          key={type.id}
          onClick={() => onTypeChange(type.id)}
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          className={clsx(
            'p-4 rounded-lg border-2 transition-all text-left',
            selectedType === type.id
              ? 'border-blue-500 bg-blue-500/10'
              : 'border-gray-700 bg-gray-800 hover:border-gray-600'
          )}
        >
          <div className={clsx(
            'w-12 h-12 rounded-lg flex items-center justify-center mb-3',
            selectedType === type.id ? 'bg-blue-500/20 text-blue-400' : 'bg-gray-700 text-gray-400'
          )}>
            {type.icon}
          </div>
          <h3 className={clsx(
            'font-medium mb-1',
            selectedType === type.id ? 'text-blue-400' : 'text-white'
          )}>
            {type.label}
          </h3>
          <p className="text-xs text-gray-400">{type.description}</p>
        </motion.button>
      ))}
    </div>
  );
};

export default InvestigationTypeSelector;

// Made with Bob
