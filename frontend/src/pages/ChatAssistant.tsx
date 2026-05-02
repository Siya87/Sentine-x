import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import ChatMessage from '../components/chat/ChatMessage';
import SuggestionChips from '../components/chat/SuggestionChips';
import KnowledgeBase from '../components/chat/KnowledgeBase';
import Button from '../components/shared/Button';
import { ChatMessage as ChatMessageType, KnowledgeBaseEntry } from '../types';
import { chatAPI } from '../services/api';
import toast from 'react-hot-toast';

const ChatAssistant: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessageType[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [showKnowledgeBase, setShowKnowledgeBase] = useState(true);
  const [showQuickActions, setShowQuickActions] = useState(false);
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [sessionId, setSessionId] = useState<string>('');
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Mock knowledge base entries
  const knowledgeBaseEntries: KnowledgeBaseEntry[] = [
    {
      id: '1',
      question: 'What is phishing?',
      answer: 'Phishing is a cyber attack that uses disguised email as a weapon. The goal is to trick the recipient into believing that the message is something they want or need.',
      category: 'Threats',
      keywords: ['phishing', 'email', 'social engineering'],
    },
    {
      id: '2',
      question: 'How to detect ransomware?',
      answer: 'Ransomware can be detected through unusual file encryption activity, ransom notes appearing on systems, and sudden inability to access files.',
      category: 'Threats',
      keywords: ['ransomware', 'malware', 'encryption'],
    },
    {
      id: '3',
      question: 'What is MITRE ATT&CK?',
      answer: 'MITRE ATT&CK is a globally-accessible knowledge base of adversary tactics and techniques based on real-world observations.',
      category: 'Frameworks',
      keywords: ['MITRE', 'ATT&CK', 'tactics', 'techniques'],
    },
    {
      id: '4',
      question: 'How to respond to a data breach?',
      answer: 'Immediate steps include: contain the breach, assess the damage, notify affected parties, investigate the cause, and implement preventive measures.',
      category: 'Incident Response',
      keywords: ['data breach', 'incident response', 'containment'],
    },
    {
      id: '5',
      question: 'What are indicators of compromise (IOCs)?',
      answer: 'IOCs are pieces of forensic data that identify potentially malicious activity on a system or network, such as IP addresses, file hashes, or URLs.',
      category: 'Detection',
      keywords: ['IOC', 'indicators', 'forensics'],
    },
  ];

  const suggestions = [
    'Explain this threat',
    'How to mitigate this attack?',
    'What is the MITRE technique?',
    'Analyze this file hash',
    'Check IP reputation',
  ];

  const handleSendMessage = async (content: string) => {
    try {
      if (!content.trim()) return;

      const userMessage: ChatMessageType = {
        message_id: `msg-${Date.now()}`,
        role: 'user',
        content: content.trim(),
        timestamp: new Date().toISOString(),
      };

      setMessages((prev) => [...prev, userMessage]);
      setInputValue('');
      setIsTyping(true);

      // Call backend API
      const response = await chatAPI.sendMessage({
        message: content.trim(),
        session_id: sessionId || undefined
      });

      // Add AI response to chat
      const aiResponse: ChatMessageType = {
        message_id: `msg-${Date.now()}-ai`,
        role: 'assistant',
        content: response.response,
        timestamp: new Date().toISOString(),
        category: response.category || detectCategory(content),
      };

      setMessages((prev) => [...prev, aiResponse]);

      // Update session ID if new
      if (response.session_id && !sessionId) {
        setSessionId(response.session_id);
      }

    } catch (error) {
      console.error('Error sending message:', error);
      toast.error('Failed to send message');

      // Add error message
      const errorMessage: ChatMessageType = {
        message_id: `msg-${Date.now()}-error`,
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, errorMessage]);

    } finally {
      setIsTyping(false);
    }
  };

  const generateAIResponse = (query: string): string => {
    const lowerQuery = query.toLowerCase();

    if (lowerQuery.includes('phishing')) {
      return 'Phishing is a social engineering attack where attackers impersonate legitimate entities to steal sensitive information. Key indicators include:\n\n• Suspicious sender addresses\n• Urgent or threatening language\n• Requests for sensitive information\n• Suspicious links or attachments\n\nTo protect against phishing:\n1. Verify sender identity\n2. Check URLs before clicking\n3. Enable multi-factor authentication\n4. Report suspicious emails';
    }

    if (lowerQuery.includes('ransomware')) {
      return 'Ransomware is malware that encrypts files and demands payment for decryption. Response steps:\n\n1. Isolate infected systems immediately\n2. Do NOT pay the ransom\n3. Report to law enforcement\n4. Restore from clean backups\n5. Investigate entry point\n6. Implement preventive measures\n\nPrevention: Regular backups, security awareness training, endpoint protection, and network segmentation.';
    }

    if (lowerQuery.includes('mitre')) {
      return 'MITRE ATT&CK is a comprehensive framework documenting adversary tactics and techniques:\n\n• 14 Tactics (objectives)\n• 100+ Techniques (methods)\n• Sub-techniques (variations)\n\nCommon tactics include:\n- Initial Access\n- Execution\n- Persistence\n- Privilege Escalation\n- Defense Evasion\n\nUse it for threat intelligence, detection engineering, and security assessments.';
    }

    if (lowerQuery.includes('breach') || lowerQuery.includes('incident')) {
      return 'Incident Response Process:\n\n1. **Preparation**: Have IR plan and tools ready\n2. **Identification**: Detect and confirm incident\n3. **Containment**: Limit damage and prevent spread\n4. **Eradication**: Remove threat from environment\n5. **Recovery**: Restore systems to normal operation\n6. **Lessons Learned**: Document and improve\n\nKey: Act quickly but methodically. Document everything.';
    }

    return `I understand you're asking about "${query}". As a cybersecurity AI assistant, I can help with:\n\n• Threat analysis and identification\n• Incident response guidance\n• Security best practices\n• MITRE ATT&CK framework\n• Malware analysis\n• Network security\n\nCould you provide more specific details about what you'd like to know?`;
  };

  const detectCategory = (query: string): string => {
    const lowerQuery = query.toLowerCase();
    if (lowerQuery.includes('phishing') || lowerQuery.includes('malware')) return 'Threats';
    if (lowerQuery.includes('mitre') || lowerQuery.includes('att&ck')) return 'Frameworks';
    if (lowerQuery.includes('incident') || lowerQuery.includes('response')) return 'Incident Response';
    if (lowerQuery.includes('detect') || lowerQuery.includes('ioc')) return 'Detection';
    return 'General';
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage(inputValue);
    }
  };

  const handleKnowledgeBaseSelect = (entry: KnowledgeBaseEntry) => {
    handleSendMessage(entry.question);
  };

  const handleNewChat = () => {
    setMessages([]);
    setInputValue('');
    setUploadedFile(null);
    setSessionId(''); // Reset session for new chat
  };

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      // Validate file size (10MB max)
      if (file.size > 10 * 1024 * 1024) {
        alert('File size must be less than 10MB');
        return;
      }
      setUploadedFile(file);
      handleSendMessage(`[File uploaded: ${file.name}] Please analyze this file.`);
    }
  };

  const handleExportChat = () => {
    const chatText = messages.map(msg =>
      `[${msg.role.toUpperCase()}] ${msg.content}\n`
    ).join('\n');
    
    const blob = new Blob([chatText], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `sentinelx-chat-${new Date().toISOString().split('T')[0]}.txt`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const quickActions = [
    {
      icon: '🔍',
      label: 'Analyze IP',
      prompt: 'Analyze this IP address: ',
      placeholder: '192.168.1.1'
    },
    {
      icon: '🔐',
      label: 'Check Hash',
      prompt: 'Check this file hash: ',
      placeholder: 'a1b2c3d4e5f6...'
    },
    {
      icon: '🌐',
      label: 'Domain Lookup',
      prompt: 'Check domain reputation: ',
      placeholder: 'example.com'
    },
    {
      icon: '📊',
      label: 'MITRE Lookup',
      prompt: 'Explain MITRE technique: ',
      placeholder: 'T1566.001'
    },
    {
      icon: '🔓',
      label: 'Decode Base64',
      prompt: 'Decode this Base64: ',
      placeholder: 'SGVsbG8gV29ybGQ='
    },
    {
      icon: '📝',
      label: 'Generate Report',
      prompt: 'Generate an incident report for: ',
      placeholder: 'phishing attack'
    }
  ];

  const handleQuickAction = (action: typeof quickActions[0]) => {
    const userInput = prompt(`${action.label}\n\n${action.prompt}`, action.placeholder);
    if (userInput) {
      handleSendMessage(action.prompt + userInput);
    }
  };

  return (
    <div className="h-[calc(100vh-8rem)] flex gap-6">
      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col bg-gray-800 border border-gray-700 rounded-lg overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-gray-700">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-purple-600 rounded-full flex items-center justify-center">
              <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
            </div>
            <div>
              <h2 className="text-lg font-semibold text-white">SentinelX AI Assistant</h2>
              <p className="text-sm text-gray-400">Powered by IBM Granite</p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={() => setShowKnowledgeBase(!showKnowledgeBase)}
              className="p-2 hover:bg-gray-700 rounded-lg transition-colors"
              title="Toggle Knowledge Base"
            >
              <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
              </svg>
            </button>
            <Button onClick={handleNewChat} variant="outline" size="sm">
              New Chat
            </Button>
          </div>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-6 space-y-4">
          {messages.length === 0 ? (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="flex flex-col items-center justify-center h-full text-center"
            >
              <div className="w-20 h-20 bg-purple-600/20 rounded-full flex items-center justify-center mb-4">
                <svg className="w-10 h-10 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-white mb-2">How can I help you today?</h3>
              <p className="text-gray-400 mb-6 max-w-md">
                Ask me anything about cybersecurity, threats, incident response, or security best practices.
              </p>
              <SuggestionChips suggestions={suggestions} onSelect={handleSendMessage} />
            </motion.div>
          ) : (
            <>
              {messages.map((message, index) => (
                <ChatMessage key={message.message_id} message={message} index={index} />
              ))}
              {isTyping && (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="flex gap-3"
                >
                  <div className="w-8 h-8 bg-purple-600 rounded-full flex items-center justify-center">
                    <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                    </svg>
                  </div>
                  <div className="bg-gray-800 border border-gray-700 rounded-lg px-4 py-3">
                    <div className="flex gap-1">
                      <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                      <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                      <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                    </div>
                  </div>
                </motion.div>
              )}
              <div ref={messagesEndRef} />
            </>
          )}
        </div>

        {/* Input Area */}
        <div className="p-4 border-t border-gray-700">
          {/* Quick Actions Bar */}
          <AnimatePresence>
            {showQuickActions && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                exit={{ opacity: 0, height: 0 }}
                className="mb-3 overflow-hidden"
              >
                <div className="grid grid-cols-3 gap-2">
                  {quickActions.map((action, index) => (
                    <button
                      key={index}
                      onClick={() => handleQuickAction(action)}
                      className="flex items-center gap-2 px-3 py-2 bg-gray-700 hover:bg-gray-600 rounded-lg transition-colors text-left"
                    >
                      <span className="text-xl">{action.icon}</span>
                      <span className="text-sm text-white">{action.label}</span>
                    </button>
                  ))}
                </div>
              </motion.div>
            )}
          </AnimatePresence>

          {/* File Upload Preview */}
          {uploadedFile && (
            <div className="mb-3 flex items-center gap-2 px-3 py-2 bg-blue-500/20 border border-blue-500/50 rounded-lg">
              <svg className="w-5 h-5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              <span className="text-sm text-blue-300 flex-1">{uploadedFile.name}</span>
              <button
                onClick={() => setUploadedFile(null)}
                className="text-blue-400 hover:text-blue-300"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          )}

          <div className="flex gap-2">
            {/* Quick Actions Toggle */}
            <button
              onClick={() => setShowQuickActions(!showQuickActions)}
              className="p-3 bg-gray-700 hover:bg-gray-600 rounded-lg transition-colors"
              title="Quick Actions"
            >
              <svg className="w-5 h-5 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </button>

            {/* File Upload */}
            <input
              ref={fileInputRef}
              type="file"
              onChange={handleFileUpload}
              className="hidden"
              accept=".txt,.log,.json,.xml,.csv,.pcap"
            />
            <button
              onClick={() => fileInputRef.current?.click()}
              className="p-3 bg-gray-700 hover:bg-gray-600 rounded-lg transition-colors"
              title="Upload File"
            >
              <svg className="w-5 h-5 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13" />
              </svg>
            </button>

            {/* Export Chat */}
            {messages.length > 0 && (
              <button
                onClick={handleExportChat}
                className="p-3 bg-gray-700 hover:bg-gray-600 rounded-lg transition-colors"
                title="Export Chat"
              >
                <svg className="w-5 h-5 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                </svg>
              </button>
            )}

            <textarea
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask me anything about cybersecurity..."
              rows={1}
              className="flex-1 bg-gray-900 border border-gray-700 rounded-lg px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-purple-500 resize-none"
            />
            <Button
              onClick={() => handleSendMessage(inputValue)}
              disabled={!inputValue.trim() || isTyping}
              variant="primary"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
              </svg>
            </Button>
          </div>
        </div>
      </div>

      {/* Knowledge Base Sidebar */}
      {showKnowledgeBase && (
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          exit={{ opacity: 0, x: 20 }}
          className="w-80 flex-shrink-0"
        >
          <KnowledgeBase entries={knowledgeBaseEntries} onSelectEntry={handleKnowledgeBaseSelect} />
        </motion.div>
      )}
    </div>
  );
};

export default ChatAssistant;

// Made with Bob
