import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Button from '../shared/Button';
import { TimelineEvent, MitreTechnique } from '../../types';

interface TimelineFormProps {
  timeline: TimelineEvent[];
  mitreTechniques: MitreTechnique[];
  onTimelineChange: (timeline: TimelineEvent[]) => void;
  onMitreChange: (techniques: MitreTechnique[]) => void;
  onNext: () => void;
  onBack: () => void;
}

const TimelineForm: React.FC<TimelineFormProps> = ({
  timeline,
  mitreTechniques,
  onTimelineChange,
  onMitreChange,
  onNext,
  onBack,
}) => {
  const [newEvent, setNewEvent] = useState({
    timestamp: '',
    event: '',
    description: '',
  });

  const [newTechnique, setNewTechnique] = useState({
    technique_id: '',
    tactic: '',
  });

  const commonTactics = [
    'Initial Access',
    'Execution',
    'Persistence',
    'Privilege Escalation',
    'Defense Evasion',
    'Credential Access',
    'Discovery',
    'Lateral Movement',
    'Collection',
    'Command and Control',
    'Exfiltration',
    'Impact',
  ];

  const addTimelineEvent = () => {
    if (newEvent.timestamp && newEvent.event && newEvent.description) {
      onTimelineChange([...timeline, newEvent]);
      setNewEvent({ timestamp: '', event: '', description: '' });
    }
  };

  const removeTimelineEvent = (index: number) => {
    onTimelineChange(timeline.filter((_, i) => i !== index));
  };

  const addMitreTechnique = () => {
    if (newTechnique.technique_id && newTechnique.tactic) {
      onMitreChange([...mitreTechniques, newTechnique]);
      setNewTechnique({ technique_id: '', tactic: '' });
    }
  };

  const removeMitreTechnique = (index: number) => {
    onMitreChange(mitreTechniques.filter((_, i) => i !== index));
  };

  return (
    <motion.div
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      className="space-y-6"
    >
      {/* Timeline Section */}
      <div className="bg-gray-800 border border-gray-700 rounded-lg p-6">
        <h3 className="text-lg font-semibold text-white mb-4">Incident Timeline</h3>
        
        <div className="space-y-4 mb-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Timestamp
              </label>
              <input
                type="datetime-local"
                value={newEvent.timestamp}
                onChange={(e) => setNewEvent({ ...newEvent, timestamp: e.target.value })}
                className="w-full bg-gray-900 border border-gray-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Event
              </label>
              <input
                type="text"
                value={newEvent.event}
                onChange={(e) => setNewEvent({ ...newEvent, event: e.target.value })}
                placeholder="e.g., Initial Detection"
                className="w-full bg-gray-900 border border-gray-700 rounded-lg px-4 py-2 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Description
              </label>
              <input
                type="text"
                value={newEvent.description}
                onChange={(e) => setNewEvent({ ...newEvent, description: e.target.value })}
                placeholder="Brief description"
                className="w-full bg-gray-900 border border-gray-700 rounded-lg px-4 py-2 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>
          <Button type="button" onClick={addTimelineEvent} variant="secondary">
            Add Timeline Event
          </Button>
        </div>

        <AnimatePresence>
          {timeline.length > 0 && (
            <div className="space-y-2">
              {timeline.map((event, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: 'auto' }}
                  exit={{ opacity: 0, height: 0 }}
                  className="bg-gray-900 border border-gray-700 rounded-lg p-4 flex items-start justify-between"
                >
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <span className="text-sm text-gray-400">
                        {new Date(event.timestamp).toLocaleString()}
                      </span>
                      <span className="px-2 py-1 bg-blue-500/20 text-blue-400 text-xs rounded">
                        {event.event}
                      </span>
                    </div>
                    <p className="text-sm text-gray-300">{event.description}</p>
                  </div>
                  <button
                    onClick={() => removeTimelineEvent(index)}
                    className="text-red-400 hover:text-red-300 ml-4"
                  >
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                </motion.div>
              ))}
            </div>
          )}
        </AnimatePresence>
      </div>

      {/* MITRE ATT&CK Section */}
      <div className="bg-gray-800 border border-gray-700 rounded-lg p-6">
        <h3 className="text-lg font-semibold text-white mb-4">MITRE ATT&CK Techniques</h3>
        
        <div className="space-y-4 mb-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Technique ID
              </label>
              <input
                type="text"
                value={newTechnique.technique_id}
                onChange={(e) => setNewTechnique({ ...newTechnique, technique_id: e.target.value })}
                placeholder="e.g., T1566.001"
                className="w-full bg-gray-900 border border-gray-700 rounded-lg px-4 py-2 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Tactic
              </label>
              <select
                value={newTechnique.tactic}
                onChange={(e) => setNewTechnique({ ...newTechnique, tactic: e.target.value })}
                className="w-full bg-gray-900 border border-gray-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">Select tactic</option>
                {commonTactics.map((tactic) => (
                  <option key={tactic} value={tactic}>
                    {tactic}
                  </option>
                ))}
              </select>
            </div>
          </div>
          <Button type="button" onClick={addMitreTechnique} variant="secondary">
            Add MITRE Technique
          </Button>
        </div>

        <AnimatePresence>
          {mitreTechniques.length > 0 && (
            <div className="flex flex-wrap gap-2">
              {mitreTechniques.map((technique, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, scale: 0.8 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0, scale: 0.8 }}
                  className="bg-gray-900 border border-gray-700 rounded-lg px-3 py-2 flex items-center gap-2"
                >
                  <span className="text-sm font-mono text-blue-400">{technique.technique_id}</span>
                  <span className="text-sm text-gray-400">-</span>
                  <span className="text-sm text-gray-300">{technique.tactic}</span>
                  <button
                    onClick={() => removeMitreTechnique(index)}
                    className="text-red-400 hover:text-red-300 ml-2"
                  >
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                </motion.div>
              ))}
            </div>
          )}
        </AnimatePresence>
      </div>

      <div className="flex justify-between">
        <Button type="button" onClick={onBack} variant="outline">
          Back
        </Button>
        <Button type="button" onClick={onNext} variant="primary">
          Next: Mitigation Steps
        </Button>
      </div>
    </motion.div>
  );
};

export default TimelineForm;

// Made with Bob
