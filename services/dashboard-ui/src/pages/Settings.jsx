import React, { useState } from 'react';

export default function Settings() {
  const [refreshRate, setRefreshRate] = useState(3);
  const [theme, setTheme] = useState('dark');

  return (
    <div style={{ background: '#1f2937', padding: '24px', borderRadius: '8px', border: '1px solid #374151', maxWidth: '600px' }}>
      <h3 style={{ fontSize: '1.1rem', marginBottom: '16px' }}>⚙️ SOC Console Settings</h3>
      
      <div style={{ marginBottom: '20px' }}>
        <label style={{ display: 'block', marginBottom: '8px', fontSize: '0.9rem', color: '#9ca3af' }}>
          Real-time Polling Interval (seconds)
        </label>
        <input
          type="number"
          min="1"
          max="60"
          value={refreshRate}
          onChange={(e) => setRefreshRate(Number(e.target.value))}
          style={{
            background: '#111827',
            border: '1px solid #374151',
            color: '#f9fafb',
            padding: '8px',
            borderRadius: '4px',
            width: '100px'
          }}
        />
      </div>

      <div style={{ marginBottom: '20px' }}>
        <label style={{ display: 'block', marginBottom: '8px', fontSize: '0.9rem', color: '#9ca3af' }}>
          Theme Preference
        </label>
        <select
          value={theme}
          onChange={(e) => setTheme(e.target.value)}
          style={{
            background: '#111827',
            border: '1px solid #374151',
            color: '#f9fafb',
            padding: '8px',
            borderRadius: '4px'
          }}
        >
          <option value="dark">Cyber Dark (High Contrast)</option>
          <option value="slate">Slate Night</option>
        </select>
      </div>

      <div style={{ padding: '12px', background: 'rgba(56, 189, 248, 0.1)', borderLeft: '4px solid #38bdf8', fontSize: '0.85rem', color: '#9ca3af' }}>
        <strong>Security Notice:</strong> Database credentials and internal keys are isolated on backend services and never exposed to the frontend console.
      </div>
    </div>
  );
}
