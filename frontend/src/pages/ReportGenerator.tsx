import React, { useState } from 'react';
import { motion } from 'framer-motion';
import ReportForm from '../components/reports/ReportForm';
import TimelineForm from '../components/reports/TimelineForm';
import MitigationForm from '../components/reports/MitigationForm';
import ReportPreview from '../components/reports/ReportPreview';
import Modal from '../components/shared/Modal';
import { IncidentReport, TimelineEvent, MitreTechnique } from '../types';
import { reportAPI } from '../services/api';
import toast from 'react-hot-toast';

const ReportGenerator: React.FC = () => {
  const [currentStep, setCurrentStep] = useState(1);
  const [generating, setGenerating] = useState(false);
  const [showSuccessModal, setShowSuccessModal] = useState(false);
  const [generatedReport, setGeneratedReport] = useState<IncidentReport | null>(null);

  const [formData, setFormData] = useState({
    title: '',
    incident_type: '',
    severity: 'medium' as 'low' | 'medium' | 'high' | 'critical',
    description: '',
    detection_time: '',
    affected_systems: '',
    indicators: '',
    attack_vector: '',
  });

  const [timeline, setTimeline] = useState<TimelineEvent[]>([]);
  const [mitreTechniques, setMitreTechniques] = useState<MitreTechnique[]>([]);
  const [mitigationSteps, setMitigationSteps] = useState<string[]>([]);

  const handleFormChange = (field: keyof typeof formData, value: string) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
  };

  const handleGenerateReport = async () => {
    try {
      // Validate required fields
      if (!formData.title || !formData.incident_type || !formData.severity) {
        toast.error('Please fill in all required fields');
        return;
      }

      setGenerating(true);

      // Prepare data for API
      const requestData = {
        title: formData.title,
        incident_type: formData.incident_type,
        severity: formData.severity,
        description: formData.description,
        detection_time: formData.detection_time || new Date().toISOString(),
        affected_systems: formData.affected_systems.split(',').map((s) => s.trim()).filter(Boolean),
        indicators: formData.indicators.split(',').map((s) => s.trim()).filter(Boolean),
        attack_vector: formData.attack_vector || '',
        mitre_techniques: mitreTechniques,
        timeline: timeline,
        mitigation_steps: mitigationSteps,
      };

      // Call backend API
      const response = await reportAPI.generateReport(requestData);

      setGeneratedReport(response);
      setShowSuccessModal(true);
      toast.success('Report generated successfully');

    } catch (error) {
      console.error('Error generating report:', error);
      toast.error('Failed to generate report');
    } finally {
      setGenerating(false);
    }
  };

  const handleDownloadPDF = async () => {
    try {
      if (!generatedReport || !generatedReport.report_id) {
        toast.error('No report to export');
        return;
      }

      toast.loading('Generating PDF...');

      // Call backend API to get PDF
      const pdfBlob = await reportAPI.exportReportPDF(generatedReport.report_id);

      // Create download link
      const url = window.URL.createObjectURL(pdfBlob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `${generatedReport.title.replace(/\s+/g, '_')}_report.pdf`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);

      toast.dismiss();
      toast.success('PDF downloaded successfully');

    } catch (error) {
      console.error('Error exporting PDF:', error);
      toast.dismiss();
      toast.error('Failed to export PDF');
    }
  };

  const handleReset = () => {
    setCurrentStep(1);
    setFormData({
      title: '',
      incident_type: '',
      severity: 'medium',
      description: '',
      detection_time: '',
      affected_systems: '',
      indicators: '',
      attack_vector: '',
    });
    setTimeline([]);
    setMitreTechniques([]);
    setMitigationSteps([]);
    setGeneratedReport(null);
    setShowSuccessModal(false);
  };

  const steps = [
    { number: 1, title: 'Basic Info', description: 'Incident details' },
    { number: 2, title: 'Timeline', description: 'Events & MITRE' },
    { number: 3, title: 'Mitigation', description: 'Response steps' },
    { number: 4, title: 'Preview', description: 'Review & generate' },
  ];

  const reportForPreview: Partial<IncidentReport> = {
    title: formData.title,
    incident_type: formData.incident_type,
    severity: formData.severity,
    description: formData.description,
    detection_time: formData.detection_time,
    affected_systems: formData.affected_systems.split(',').map((s) => s.trim()).filter(Boolean),
    indicators: formData.indicators.split(',').map((s) => s.trim()).filter(Boolean),
    attack_vector: formData.attack_vector,
    timeline: timeline,
    mitre_techniques: mitreTechniques,
    mitigation_steps: mitigationSteps,
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <h1 className="text-3xl font-bold text-white mb-2">Incident Report Generator</h1>
        <p className="text-gray-400">Create comprehensive incident reports with AI assistance</p>
      </motion.div>

      {/* Progress Steps */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="bg-gray-800 border border-gray-700 rounded-lg p-6"
      >
        <div className="flex items-center justify-between">
          {steps.map((step, index) => (
            <React.Fragment key={step.number}>
              <div className="flex items-center gap-3">
                <div
                  className={`w-10 h-10 rounded-full flex items-center justify-center font-semibold transition-colors ${
                    currentStep === step.number
                      ? 'bg-blue-600 text-white'
                      : currentStep > step.number
                      ? 'bg-green-600 text-white'
                      : 'bg-gray-700 text-gray-400'
                  }`}
                >
                  {currentStep > step.number ? (
                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                  ) : (
                    step.number
                  )}
                </div>
                <div>
                  <div className="font-medium text-white">{step.title}</div>
                  <div className="text-sm text-gray-400">{step.description}</div>
                </div>
              </div>
              {index < steps.length - 1 && (
                <div className="flex-1 h-0.5 bg-gray-700 mx-4">
                  <div
                    className={`h-full transition-all duration-300 ${
                      currentStep > step.number ? 'bg-green-600' : 'bg-gray-700'
                    }`}
                    style={{ width: currentStep > step.number ? '100%' : '0%' }}
                  />
                </div>
              )}
            </React.Fragment>
          ))}
        </div>
      </motion.div>

      {/* Form Steps */}
      <div className="min-h-[600px]">
        {currentStep === 1 && (
          <ReportForm
            formData={formData}
            onChange={handleFormChange}
            onNext={() => setCurrentStep(2)}
          />
        )}

        {currentStep === 2 && (
          <TimelineForm
            timeline={timeline}
            mitreTechniques={mitreTechniques}
            onTimelineChange={setTimeline}
            onMitreChange={setMitreTechniques}
            onNext={() => setCurrentStep(3)}
            onBack={() => setCurrentStep(1)}
          />
        )}

        {currentStep === 3 && (
          <MitigationForm
            mitigationSteps={mitigationSteps}
            onMitigationChange={setMitigationSteps}
            onNext={() => setCurrentStep(4)}
            onBack={() => setCurrentStep(2)}
          />
        )}

        {currentStep === 4 && (
          <ReportPreview
            report={reportForPreview}
            onBack={() => setCurrentStep(3)}
            onGenerate={handleGenerateReport}
            generating={generating}
          />
        )}
      </div>

      {/* Success Modal */}
      <Modal
        isOpen={showSuccessModal}
        onClose={() => setShowSuccessModal(false)}
        title="Report Generated Successfully"
      >
        <div className="space-y-4">
          <div className="flex items-center justify-center mb-4">
            <div className="w-16 h-16 bg-green-500/20 rounded-full flex items-center justify-center">
              <svg className="w-8 h-8 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
            </div>
          </div>

          <p className="text-center text-gray-300">
            Your incident report has been generated successfully!
          </p>

          {generatedReport && (
            <div className="bg-gray-800 border border-gray-700 rounded-lg p-4">
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-400">Report ID:</span>
                  <span className="text-white font-mono">{generatedReport.report_id}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-400">Title:</span>
                  <span className="text-white">{generatedReport.title}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-400">Created:</span>
                  <span className="text-white">{new Date(generatedReport.created_at).toLocaleString()}</span>
                </div>
              </div>
            </div>
          )}

          <div className="flex gap-3">
            <button
              onClick={handleDownloadPDF}
              className="flex-1 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors flex items-center justify-center gap-2"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              Download PDF
            </button>
            <button
              onClick={handleReset}
              className="flex-1 px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded-lg transition-colors"
            >
              Create New Report
            </button>
          </div>
        </div>
      </Modal>
    </div>
  );
};

export default ReportGenerator;

// Made with Bob
