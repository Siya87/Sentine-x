import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { KnowledgeBaseEntry } from '../../types';

interface KnowledgeBaseProps {
  entries: KnowledgeBaseEntry[];
  onSelectEntry: (entry: KnowledgeBaseEntry) => void;
}

const KnowledgeBase: React.FC<KnowledgeBaseProps> = ({ entries, onSelectEntry }) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');

  const categories = ['all', ...Array.from(new Set(entries.map((e) => e.category)))];

  const filteredEntries = entries.filter((entry) => {
    const matchesSearch =
      searchQuery === '' ||
      entry.question.toLowerCase().includes(searchQuery.toLowerCase()) ||
      entry.answer.toLowerCase().includes(searchQuery.toLowerCase()) ||
      entry.keywords.some((k) => k.toLowerCase().includes(searchQuery.toLowerCase()));

    const matchesCategory = selectedCategory === 'all' || entry.category === selectedCategory;

    return matchesSearch && matchesCategory;
  });

  return (
    <div className="h-full flex flex-col bg-gray-800 border-l border-gray-700">
      <div className="p-4 border-b border-gray-700">
        <h3 className="text-lg font-semibold text-white mb-4">Knowledge Base</h3>
        
        {/* Search */}
        <div className="relative mb-3">
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search knowledge base..."
            className="w-full bg-gray-900 border border-gray-700 rounded-lg px-4 py-2 pl-10 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
          />
          <svg
            className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-500"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>

        {/* Category Filter */}
        <div className="flex flex-wrap gap-1">
          {categories.map((category) => (
            <button
              key={category}
              onClick={() => setSelectedCategory(category)}
              className={`px-3 py-1 rounded-full text-xs transition-colors ${
                selectedCategory === category
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-700 text-gray-400 hover:bg-gray-600'
              }`}
            >
              {category}
            </button>
          ))}
        </div>
      </div>

      {/* Entries List */}
      <div className="flex-1 overflow-y-auto p-4 space-y-2">
        <AnimatePresence>
          {filteredEntries.length === 0 ? (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="text-center py-8 text-gray-500"
            >
              No entries found
            </motion.div>
          ) : (
            filteredEntries.map((entry, index) => (
              <motion.button
                key={entry.id}
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
                transition={{ delay: index * 0.03 }}
                onClick={() => onSelectEntry(entry)}
                className="w-full text-left bg-gray-900 hover:bg-gray-700 border border-gray-700 hover:border-blue-500 rounded-lg p-3 transition-colors"
              >
                <div className="flex items-start justify-between gap-2 mb-2">
                  <h4 className="text-sm font-medium text-white line-clamp-2">{entry.question}</h4>
                  <span className="flex-shrink-0 px-2 py-0.5 bg-purple-500/20 text-purple-400 text-xs rounded">
                    {entry.category}
                  </span>
                </div>
                <p className="text-xs text-gray-400 line-clamp-2">{entry.answer}</p>
                {entry.keywords.length > 0 && (
                  <div className="flex flex-wrap gap-1 mt-2">
                    {entry.keywords.slice(0, 3).map((keyword, idx) => (
                      <span key={idx} className="px-2 py-0.5 bg-gray-800 text-gray-500 text-xs rounded">
                        {keyword}
                      </span>
                    ))}
                  </div>
                )}
              </motion.button>
            ))
          )}
        </AnimatePresence>
      </div>

      {/* Stats */}
      <div className="p-4 border-t border-gray-700">
        <div className="text-xs text-gray-500 text-center">
          Showing {filteredEntries.length} of {entries.length} entries
        </div>
      </div>
    </div>
  );
};

export default KnowledgeBase;

// Made with Bob
