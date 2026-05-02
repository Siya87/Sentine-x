import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Modal from '../shared/Modal';
import Button from '../shared/Button';
import Input from '../shared/Input';

interface SettingsModalProps {
  isOpen: boolean;
  onClose: () => void;
}

type SettingsTab = 'general' | 'api' | 'notifications' | 'security' | 'data';

const SettingsModal: React.FC<SettingsModalProps> = ({ isOpen, onClose }) => {
  const [activeTab, setActiveTab] = useState<SettingsTab>('general');
  const [settings, setSettings] = useState({
    // General Settings
    theme: 'dark',
    language: 'en',
    dashboardRefresh: '30',
    timezone: 'UTC',
    
    // API Keys
    virusTotalKey: '',
    shodanKey: '',
    abuseIPDBKey: '',
    hibpKey: '',
    
    // Notifications
    emailNotifications: true,
    criticalAlerts: true,
    highAlerts: true,
    mediumAlerts: false,
    lowAlerts: false,
    emailAddress: 'admin@sentinelx.ai',
    
    // Security
    sessionTimeout: '30',
    twoFactorAuth: false,
    ipWhitelist: '',
    
    // Data Retention
    logRetention: '90',
    reportRetention: '365',
    autoArchive: true,
  });

  const tabs = [
    { id: 'general' as SettingsTab, name: 'General', icon: '⚙️' },
    { id: 'api' as SettingsTab, name: 'API Keys', icon: '🔑' },
    { id: 'notifications' as SettingsTab, name: 'Notifications', icon: '🔔' },
    { id: 'security' as SettingsTab, name: 'Security', icon: '🔒' },
    { id: 'data' as SettingsTab, name: 'Data', icon: '💾' },
  ];

  const handleSave = () => {
    console.log('Saving settings:', settings);
    // TODO: Implement API call to save settings
    onClose();
  };

  const handleChange = (key: string, value: any) => {
    setSettings(prev => ({ ...prev, [key]: value }));
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Settings" size="xl">
      <div className="flex h-[600px]">
        {/* Sidebar Tabs */}
        <div className="w-48 border-r border-gray-700 pr-4">
          <nav className="space-y-1">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg text-left transition-all ${
                  activeTab === tab.id
                    ? 'bg-blue-500/20 text-blue-400 border border-blue-500/50'
                    : 'text-gray-400 hover:bg-gray-700 hover:text-white'
                }`}
              >
                <span className="text-xl">{tab.icon}</span>
                <span className="font-medium">{tab.name}</span>
              </button>
            ))}
          </nav>
        </div>

        {/* Content Area */}
        <div className="flex-1 pl-6 overflow-y-auto">
          <AnimatePresence mode="wait">
            <motion.div
              key={activeTab}
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              transition={{ duration: 0.2 }}
            >
              {/* General Settings */}
              {activeTab === 'general' && (
                <div className="space-y-6">
                  <div>
                    <h3 className="text-lg font-semibold text-white mb-4">General Settings</h3>
                    
                    <div className="space-y-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-300 mb-2">
                          Theme
                        </label>
                        <select
                          value={settings.theme}
                          onChange={(e) => handleChange('theme', e.target.value)}
                          className="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-blue-500"
                        >
                          <option value="dark">Dark</option>
                          <option value="light">Light</option>
                          <option value="auto">Auto</option>
                        </select>
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-300 mb-2">
                          Language
                        </label>
                        <select
                          value={settings.language}
                          onChange={(e) => handleChange('language', e.target.value)}
                          className="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-blue-500"
                        >
                          <option value="en">English</option>
                          <option value="es">Spanish</option>
                          <option value="fr">French</option>
                          <option value="de">German</option>
                        </select>
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-300 mb-2">
                          Dashboard Auto-Refresh (seconds)
                        </label>
                        <Input
                          type="number"
                          value={settings.dashboardRefresh}
                          onChange={(value) => handleChange('dashboardRefresh', value)}
                          placeholder="30"
                        />
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-300 mb-2">
                          Timezone
                        </label>
                        <select
                          value={settings.timezone}
                          onChange={(e) => handleChange('timezone', e.target.value)}
                          className="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-blue-500"
                        >
                          <option value="UTC">UTC</option>
                          <option value="America/New_York">Eastern Time</option>
                          <option value="America/Los_Angeles">Pacific Time</option>
                          <option value="Europe/London">London</option>
                          <option value="Asia/Tokyo">Tokyo</option>
                        </select>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* API Keys */}
              {activeTab === 'api' && (
                <div className="space-y-6">
                  <div>
                    <h3 className="text-lg font-semibold text-white mb-2">API Configuration</h3>
                    <p className="text-sm text-gray-400 mb-4">
                      Configure your external API keys for threat intelligence services
                    </p>
                    
                    <div className="space-y-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-300 mb-2">
                          VirusTotal API Key
                        </label>
                        <Input
                          type="password"
                          value={settings.virusTotalKey}
                          onChange={(value) => handleChange('virusTotalKey', value)}
                          placeholder="Enter your VirusTotal API key"
                        />
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-300 mb-2">
                          Shodan API Key
                        </label>
                        <Input
                          type="password"
                          value={settings.shodanKey}
                          onChange={(value) => handleChange('shodanKey', value)}
                          placeholder="Enter your Shodan API key"
                        />
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-300 mb-2">
                          AbuseIPDB API Key
                        </label>
                        <Input
                          type="password"
                          value={settings.abuseIPDBKey}
                          onChange={(value) => handleChange('abuseIPDBKey', value)}
                          placeholder="Enter your AbuseIPDB API key"
                        />
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-300 mb-2">
                          Have I Been Pwned API Key
                        </label>
                        <Input
                          type="password"
                          value={settings.hibpKey}
                          onChange={(value) => handleChange('hibpKey', value)}
                          placeholder="Enter your HIBP API key"
                        />
                      </div>

                      <div className="bg-blue-500/10 border border-blue-500/30 rounded-lg p-4 mt-4">
                        <p className="text-sm text-blue-300">
                          <strong>Note:</strong> API keys are encrypted and stored securely. Never share your keys with anyone.
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* Notifications */}
              {activeTab === 'notifications' && (
                <div className="space-y-6">
                  <div>
                    <h3 className="text-lg font-semibold text-white mb-2">Notification Preferences</h3>
                    <p className="text-sm text-gray-400 mb-4">
                      Configure how and when you receive alerts
                    </p>
                    
                    <div className="space-y-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-300 mb-2">
                          Email Address
                        </label>
                        <Input
                          type="email"
                          value={settings.emailAddress}
                          onChange={(value) => handleChange('emailAddress', value)}
                          placeholder="admin@sentinelx.ai"
                        />
                      </div>

                      <div className="space-y-3">
                        <label className="flex items-center gap-3 cursor-pointer">
                          <input
                            type="checkbox"
                            checked={settings.emailNotifications}
                            onChange={(e) => handleChange('emailNotifications', e.target.checked)}
                            className="w-5 h-5 rounded border-gray-600 bg-gray-700 text-blue-500 focus:ring-blue-500"
                          />
                          <span className="text-white">Enable Email Notifications</span>
                        </label>

                        <div className="ml-8 space-y-2">
                          <label className="flex items-center gap-3 cursor-pointer">
                            <input
                              type="checkbox"
                              checked={settings.criticalAlerts}
                              onChange={(e) => handleChange('criticalAlerts', e.target.checked)}
                              className="w-4 h-4 rounded border-gray-600 bg-gray-700 text-red-500 focus:ring-red-500"
                            />
                            <span className="text-gray-300">Critical Alerts</span>
                            <span className="text-xs text-red-400">(Recommended)</span>
                          </label>

                          <label className="flex items-center gap-3 cursor-pointer">
                            <input
                              type="checkbox"
                              checked={settings.highAlerts}
                              onChange={(e) => handleChange('highAlerts', e.target.checked)}
                              className="w-4 h-4 rounded border-gray-600 bg-gray-700 text-orange-500 focus:ring-orange-500"
                            />
                            <span className="text-gray-300">High Severity Alerts</span>
                          </label>

                          <label className="flex items-center gap-3 cursor-pointer">
                            <input
                              type="checkbox"
                              checked={settings.mediumAlerts}
                              onChange={(e) => handleChange('mediumAlerts', e.target.checked)}
                              className="w-4 h-4 rounded border-gray-600 bg-gray-700 text-yellow-500 focus:ring-yellow-500"
                            />
                            <span className="text-gray-300">Medium Severity Alerts</span>
                          </label>

                          <label className="flex items-center gap-3 cursor-pointer">
                            <input
                              type="checkbox"
                              checked={settings.lowAlerts}
                              onChange={(e) => handleChange('lowAlerts', e.target.checked)}
                              className="w-4 h-4 rounded border-gray-600 bg-gray-700 text-green-500 focus:ring-green-500"
                            />
                            <span className="text-gray-300">Low Severity Alerts</span>
                          </label>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* Security */}
              {activeTab === 'security' && (
                <div className="space-y-6">
                  <div>
                    <h3 className="text-lg font-semibold text-white mb-2">Security Settings</h3>
                    <p className="text-sm text-gray-400 mb-4">
                      Manage security and access control settings
                    </p>
                    
                    <div className="space-y-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-300 mb-2">
                          Session Timeout (minutes)
                        </label>
                        <Input
                          type="number"
                          value={settings.sessionTimeout}
                          onChange={(value) => handleChange('sessionTimeout', value)}
                          placeholder="30"
                        />
                        <p className="text-xs text-gray-500 mt-1">
                          Automatically log out after period of inactivity
                        </p>
                      </div>

                      <div>
                        <label className="flex items-center gap-3 cursor-pointer">
                          <input
                            type="checkbox"
                            checked={settings.twoFactorAuth}
                            onChange={(e) => handleChange('twoFactorAuth', e.target.checked)}
                            className="w-5 h-5 rounded border-gray-600 bg-gray-700 text-blue-500 focus:ring-blue-500"
                          />
                          <div>
                            <span className="text-white block">Enable Two-Factor Authentication</span>
                            <span className="text-xs text-gray-400">Add an extra layer of security to your account</span>
                          </div>
                        </label>
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-300 mb-2">
                          IP Whitelist
                        </label>
                        <textarea
                          value={settings.ipWhitelist}
                          onChange={(e) => handleChange('ipWhitelist', e.target.value)}
                          placeholder="Enter IP addresses (one per line)&#10;192.168.1.1&#10;10.0.0.0/24"
                          className="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-blue-500 min-h-[100px]"
                        />
                        <p className="text-xs text-gray-500 mt-1">
                          Only allow access from these IP addresses
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* Data Retention */}
              {activeTab === 'data' && (
                <div className="space-y-6">
                  <div>
                    <h3 className="text-lg font-semibold text-white mb-2">Data Retention</h3>
                    <p className="text-sm text-gray-400 mb-4">
                      Configure how long data is stored in the system
                    </p>
                    
                    <div className="space-y-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-300 mb-2">
                          Log Retention Period (days)
                        </label>
                        <Input
                          type="number"
                          value={settings.logRetention}
                          onChange={(value) => handleChange('logRetention', value)}
                          placeholder="90"
                        />
                        <p className="text-xs text-gray-500 mt-1">
                          Logs older than this will be automatically deleted
                        </p>
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-300 mb-2">
                          Report Retention Period (days)
                        </label>
                        <Input
                          type="number"
                          value={settings.reportRetention}
                          onChange={(value) => handleChange('reportRetention', value)}
                          placeholder="365"
                        />
                        <p className="text-xs text-gray-500 mt-1">
                          Generated reports older than this will be archived
                        </p>
                      </div>

                      <div>
                        <label className="flex items-center gap-3 cursor-pointer">
                          <input
                            type="checkbox"
                            checked={settings.autoArchive}
                            onChange={(e) => handleChange('autoArchive', e.target.checked)}
                            className="w-5 h-5 rounded border-gray-600 bg-gray-700 text-blue-500 focus:ring-blue-500"
                          />
                          <div>
                            <span className="text-white block">Enable Auto-Archive</span>
                            <span className="text-xs text-gray-400">Automatically archive old data instead of deleting</span>
                          </div>
                        </label>
                      </div>

                      <div className="bg-yellow-500/10 border border-yellow-500/30 rounded-lg p-4 mt-4">
                        <p className="text-sm text-yellow-300">
                          <strong>Warning:</strong> Reducing retention periods will permanently delete older data. This action cannot be undone.
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </motion.div>
          </AnimatePresence>
        </div>
      </div>

      {/* Footer Actions */}
      <div className="flex justify-end gap-3 mt-6 pt-4 border-t border-gray-700">
        <Button variant="outline" onClick={onClose}>
          Cancel
        </Button>
        <Button variant="primary" onClick={handleSave}>
          Save Changes
        </Button>
      </div>
    </Modal>
  );
};

export default SettingsModal;

// Made with Bob
