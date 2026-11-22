import React from 'react';
import LiveIndicator from './LiveIndicator';

export default function Navbar({ title }) {
  return (
    <header className="navbar">
      <div style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
        <h2 style={{ fontSize: '1.2rem', fontWeight: 600 }}>{title}</h2>
      </div>
      <div style={{ display: 'flex', alignItems: 'center', gap: '20px' }}>
        <LiveIndicator />
        <span style={{ fontSize: '0.85rem', color: '#9ca3af' }}>
          Network: <span style={{ color: '#10b981', fontWeight: 'bold' }}>SEGMENTED</span>
        </span>
      </div>
    </header>
  );
}
