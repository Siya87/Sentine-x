import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Button from '../shared/Button';

interface MitigationFormProps {
  mitigationSteps: string[];
  onMitigationChange: (steps: string[]) => void;
  onNext: () => void;
  onBack: () => void;
}

const MitigationForm: React.FC<MitigationFormProps> = ({
  mitigationSteps,
  onMitigationChange,
  onNext,
  onBack,
}) => {
  const [newStep, setNewStep] = useState('');

  const addMitigationStep = () => {
    if (newStep.trim()) {
      onMitigationChange([...mitigationSteps, newStep.trim()]);
      setNewStep('');
    }
  };

  const removeMitigationStep = (index: number) => {
    onMitigationChange(mitigationSteps.filter((_, i) => i !== index));
  };

  const suggestedSteps = [
    'Isolate affected systems from the network',
    'Change all compromised credentials',
    'Apply security patches and updates',
    'Review and update firewall rules',
    'Enable multi-factor authentication',
    'Conduct security awareness training',
    'Implement endpoint detection and response (EDR)',
    'Review and update incident response plan',
  ];

  const addSuggestedStep = (step: string) => {
    if (!mitigationSteps.includes(step)) {
      onMitigationChange([...mitigationSteps, step]);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      className="space-y-6"
    >
      <div className="bg-gray-800 border border-gray-700 rounded-lg p-6">
        <h3 className="text-lg font-semibold text-white mb-4">Mitigation Steps</h3>
        
        <div className="space-y-4 mb-6">
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Add Mitigation Step
            </label>
            <div className="flex gap-2">
              <input
                type="text"
                value={newStep}
                onChange={(e) => setNewStep(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && addMitigationStep()}
                placeholder="Describe the mitigation action taken..."
                className="flex-1 bg-gray-900 border border-gray-700 rounded-lg px-4 py-2 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              <Button type="button" onClick={addMitigationStep} variant="secondary">
                Add
              </Button>
            </div>
          </div>

          <AnimatePresence>
            {mitigationSteps.length > 0 && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="space-y-2"
              >
                {mitigationSteps.map((step, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    exit={{ opacity: 0, x: -20 }}
                    className="bg-gray-900 border border-gray-700 rounded-lg p-4 flex items-start gap-3"
                  >
                    <div className="flex-shrink-0 w-6 h-6 bg-blue-500/20 text-blue-400 rounded-full flex items-center justify-center text-sm font-medium">
                      {index + 1}
                    </div>
                    <p className="flex-1 text-sm text-gray-300">{step}</p>
                    <button
                      onClick={() => removeMitigationStep(index)}
                      className="text-red-400 hover:text-red-300"
                    >
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                      </svg>
                    </button>
                  </motion.div>
                ))}
              </motion.div>
            )}
          </AnimatePresence>
        </div>

        <div className="border-t border-gray-700 pt-6">
          <h4 className="text-sm font-medium text-gray-300 mb-3">Suggested Mitigation Steps</h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
            {suggestedSteps.map((step, index) => (
              <button
                key={index}
                onClick={() => addSuggestedStep(step)}
                disabled={mitigationSteps.includes(step)}
                className={`text-left px-3 py-2 rounded-lg text-sm transition-colors ${
                  mitigationSteps.includes(step)
                    ? 'bg-gray-700 text-gray-500 cursor-not-allowed'
                    : 'bg-gray-900 text-gray-300 hover:bg-gray-700 border border-gray-700'
                }`}
              >
                <div className="flex items-center gap-2">
                  {mitigationSteps.includes(step) ? (
                    <svg className="w-4 h-4 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                  ) : (
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                    </svg>
                  )}
                  <span>{step}</span>
                </div>
              </button>
            ))}
          </div>
        </div>
      </div>

      <div className="flex justify-between">
        <Button type="button" onClick={onBack} variant="outline">
          Back
        </Button>
        <Button 
          type="button" 
          onClick={onNext} 
          variant="primary"
          disabled={mitigationSteps.length === 0}
        >
          Preview Report
        </Button>
      </div>
    </motion.div>
  );
};

export default MitigationForm;

// Made with Bob
