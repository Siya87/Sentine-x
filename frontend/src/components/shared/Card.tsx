import React from 'react';
import { motion } from 'framer-motion';
import clsx from 'clsx';

interface CardProps {
  title?: string;
  children: React.ReactNode;
  className?: string;
  actions?: React.ReactNode;
  hover?: boolean;
}

const Card: React.FC<CardProps> = ({
  title,
  children,
  className,
  actions,
  hover = false,
}) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      whileHover={hover ? { y: -4 } : {}}
      className={clsx(
        'bg-gray-800 rounded-lg border border-gray-700 p-6',
        hover && 'transition-shadow hover:shadow-xl hover:shadow-blue-500/10',
        className
      )}
    >
      {title && (
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-xl font-semibold text-white">{title}</h3>
          {actions && <div className="flex items-center space-x-2">{actions}</div>}
        </div>
      )}
      {children}
    </motion.div>
  );
};

export default Card;

// Made with Bob
