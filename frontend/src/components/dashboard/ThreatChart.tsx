import React from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import Card from '../shared/Card';

interface ThreatChartProps {
  data: Array<{
    date: string;
    threats: number;
    phishing: number;
    malware: number;
  }>;
}

const ThreatChart: React.FC<ThreatChartProps> = ({ data }) => {
  return (
    <Card title="Threat Trends (Last 7 Days)">
      <ResponsiveContainer width="100%" height={300}>
        <AreaChart data={data}>
          <defs>
            <linearGradient id="colorThreats" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#ef4444" stopOpacity={0.3}/>
              <stop offset="95%" stopColor="#ef4444" stopOpacity={0}/>
            </linearGradient>
            <linearGradient id="colorPhishing" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#f59e0b" stopOpacity={0.3}/>
              <stop offset="95%" stopColor="#f59e0b" stopOpacity={0}/>
            </linearGradient>
            <linearGradient id="colorMalware" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3}/>
              <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
          <XAxis 
            dataKey="date" 
            stroke="#9ca3af"
            style={{ fontSize: '12px' }}
          />
          <YAxis 
            stroke="#9ca3af"
            style={{ fontSize: '12px' }}
          />
          <Tooltip 
            contentStyle={{ 
              backgroundColor: '#1f2937', 
              border: '1px solid #374151',
              borderRadius: '8px',
              color: '#fff'
            }}
          />
          <Legend 
            wrapperStyle={{ color: '#9ca3af' }}
          />
          <Area 
            type="monotone" 
            dataKey="threats" 
            stroke="#ef4444" 
            fillOpacity={1}
            fill="url(#colorThreats)"
            name="Total Threats"
          />
          <Area 
            type="monotone" 
            dataKey="phishing" 
            stroke="#f59e0b" 
            fillOpacity={1}
            fill="url(#colorPhishing)"
            name="Phishing"
          />
          <Area 
            type="monotone" 
            dataKey="malware" 
            stroke="#3b82f6" 
            fillOpacity={1}
            fill="url(#colorMalware)"
            name="Malware"
          />
        </AreaChart>
      </ResponsiveContainer>
    </Card>
  );
};

export default ThreatChart;

// Made with Bob
