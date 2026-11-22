import React from 'react';

export default function FilterBar({ filters, onChange }) {
  return (
    <div style={{
      display: 'flex',
      gap: '12px',
      marginBottom: '16px',
      flexWrap: 'wrap',
      background: '#1f2937',
      padding: '12px',
      borderRadius: '6px'
    }}>
      <input
        type="text"
        placeholder="Filter by Source IP..."
        value={filters.source_ip || ''}
        onChange={(e) => onChange({ ...filters, source_ip: e.target.value })}
        style={{
          background: '#111827',
          border: '1px solid #374151',
          color: '#f9fafb',
          padding: '6px 10px',
          borderRadius: '4px',
          fontSize: '0.85rem'
        }}
      />
      <select
        value={filters.event_type || ''}
        onChange={(e) => onChange({ ...filters, event_type: e.target.value })}
        style={{
          background: '#111827',
          border: '1px solid #374151',
          color: '#f9fafb',
          padding: '6px 10px',
          borderRadius: '4px',
          fontSize: '0.85rem'
        }}
      >
        <option value="">All Event Types</option>
        <option value="login_attempt">Fake Login Attempt</option>
        <option value="path_probe">Path Probe</option>
        <option value="page_access">Page Access</option>
        <option value="suspicious_request">Suspicious Request</option>
      </select>

      <select
        value={filters.severity || ''}
        onChange={(e) => onChange({ ...filters, severity: e.target.value })}
        style={{
          background: '#111827',
          border: '1px solid #374151',
          color: '#f9fafb',
          padding: '6px 10px',
          borderRadius: '4px',
          fontSize: '0.85rem'
        }}
      >
        <option value="">All Severities</option>
        <option value="low">Low</option>
        <option value="medium">Medium</option>
        <option value="high">High</option>
        <option value="critical">Critical</option>
      </select>
    </div>
  );
}
