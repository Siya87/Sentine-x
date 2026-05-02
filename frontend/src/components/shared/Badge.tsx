import React from 'react';
import clsx from 'clsx';

interface BadgeProps {
  children: React.ReactNode;
  severity?: 'low' | 'medium' | 'high' | 'critical';
  variant?: 'solid' | 'outline';
  className?: string;
}

const Badge: React.FC<BadgeProps> = ({
  children,
  severity,
  variant = 'solid',
  className,
}) => {
  const severityColors = {
    low: variant === 'solid' 
      ? 'bg-green-500/20 text-green-400 border-green-500/50'
      : 'border-green-500 text-green-400',
    medium: variant === 'solid'
      ? 'bg-yellow-500/20 text-yellow-400 border-yellow-500/50'
      : 'border-yellow-500 text-yellow-400',
    high: variant === 'solid'
      ? 'bg-orange-500/20 text-orange-400 border-orange-500/50'
      : 'border-orange-500 text-orange-400',
    critical: variant === 'solid'
      ? 'bg-red-500/20 text-red-400 border-red-500/50'
      : 'border-red-500 text-red-400',
  };

  return (
    <span
      className={clsx(
        'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border',
        severity ? severityColors[severity] : 'bg-gray-700 text-gray-300 border-gray-600',
        className
      )}
    >
      {children}
    </span>
  );
};

export default Badge;

// Made with Bob
