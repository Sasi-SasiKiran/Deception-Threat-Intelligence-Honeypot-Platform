import React from 'react';

export default function Sidebar({ currentPage, onNavigate }) {
  const items = [
    { id: 'overview', label: '📊 Overview' },
    { id: 'live-events', label: '🚨 Live Events' },
    { id: 'analysis', label: '🔍 Attack Analysis' },
    { id: 'ip-analysis', label: '🌐 IP Intelligence' },
    { id: 'settings', label: '⚙️ Settings' }
  ];

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <span>🛡️</span> DECEPTION SOC
      </div>
      <ul className="nav-menu">
        {items.map((item) => (
          <li
            key={item.id}
            className={`nav-item ${currentPage === item.id ? 'active' : ''}`}
            onClick={() => onNavigate(item.id)}
          >
            {item.label}
          </li>
        ))}
      </ul>
      <div style={{ padding: '16px', fontSize: '11px', color: '#6b7280', borderTop: '1px solid #374151' }}>
        Ethnotech Honeypot Platform v1.0
      </div>
    </aside>
  );
}
