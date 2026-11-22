import React from 'react';

export default function LiveIndicator() {
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '0.85rem' }}>
      <div className="pulse-dot"></div>
      <span style={{ color: '#10b981', fontWeight: 600 }}>LIVE INGESTION</span>
    </div>
  );
}
