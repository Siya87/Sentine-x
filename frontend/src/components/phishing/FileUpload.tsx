import React, { useState, useRef } from 'react';
import Button from '../shared/Button';

interface FileUploadProps {
  onAnalyze: (data: { file: File }) => void;
  isLoading: boolean;
}

const FileUpload: React.FC<FileUploadProps> = ({ onAnalyze, isLoading }) => {
  const [file, setFile] = useState<File | null>(null);
  const [dragActive, setDragActive] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setFile(e.dataTransfer.files[0]);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (file) {
      onAnalyze({ file });
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
          dragActive
            ? 'border-blue-500 bg-blue-500/10'
            : 'border-gray-600 hover:border-gray-500'
        }`}
      >
        <input
          ref={fileInputRef}
          type="file"
          onChange={handleChange}
          className="hidden"
          accept=".eml,.msg,.txt,.pdf,.doc,.docx"
        />
        
        {file ? (
          <div className="space-y-4">
            <div className="w-16 h-16 mx-auto bg-green-500/20 rounded-lg flex items-center justify-center">
              <svg className="w-8 h-8 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div>
              <p className="text-white font-medium">{file.name}</p>
              <p className="text-sm text-gray-400">{(file.size / 1024).toFixed(2)} KB</p>
            </div>
            <Button
              type="button"
              variant="outline"
              onClick={() => setFile(null)}
            >
              Remove File
            </Button>
          </div>
        ) : (
          <div className="space-y-4">
            <div className="w-16 h-16 mx-auto bg-gray-700 rounded-lg flex items-center justify-center">
              <svg className="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
              </svg>
            </div>
            <div>
              <p className="text-white mb-2">Drag and drop your file here</p>
              <p className="text-sm text-gray-400 mb-4">or</p>
              <Button
                type="button"
                variant="outline"
                onClick={() => fileInputRef.current?.click()}
              >
                Browse Files
              </Button>
            </div>
            <p className="text-xs text-gray-500">
              Supported: .eml, .msg, .txt, .pdf, .doc, .docx (Max 10MB)
            </p>
          </div>
        )}
      </div>

      <Button
        type="submit"
        variant="primary"
        isLoading={isLoading}
        disabled={!file}
        className="w-full"
      >
        Analyze File
      </Button>
    </form>
  );
};

export default FileUpload;

// Made with Bob
