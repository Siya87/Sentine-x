import React from 'react';
import clsx from 'clsx';

interface InputProps {
  label?: string;
  type?: string;
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
  error?: string;
  required?: boolean;
  disabled?: boolean;
  className?: string;
  icon?: React.ComponentType<{ className?: string }>;
}

const Input: React.FC<InputProps> = ({
  label,
  type = 'text',
  value,
  onChange,
  placeholder,
  error,
  required = false,
  disabled = false,
  className,
  icon: Icon,
}) => {
  return (
    <div className={className}>
      {label && (
        <label className="block text-gray-300 text-sm font-medium mb-2">
          {label}
          {required && <span className="text-red-500 ml-1">*</span>}
        </label>
      )}
      <div className="relative">
        {Icon && (
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <Icon className="h-5 w-5 text-gray-400" />
          </div>
        )}
        <input
          type={type}
          value={value}
          onChange={(e) => onChange(e.target.value)}
          placeholder={placeholder}
          disabled={disabled}
          className={clsx(
            'w-full bg-gray-700 text-white rounded-lg px-4 py-2 border focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors',
            Icon && 'pl-10',
            error ? 'border-red-500' : 'border-gray-600',
            disabled && 'opacity-50 cursor-not-allowed'
          )}
        />
      </div>
      {error && <p className="mt-1 text-sm text-red-500">{error}</p>}
    </div>
  );
};

export default Input;

// Made with Bob
