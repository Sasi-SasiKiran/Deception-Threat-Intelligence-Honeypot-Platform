import React from 'react';

export default function StatCard({ title, value, subtitle, icon }) {
  return (
    <div className="stat-card">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
        <div className="stat-card-title">{title}</div>
        {icon && <span style={{ fontSize: '1.2rem' }}>{icon}</span>}
      </div>
      <div className="stat-card-value">{value}</div>
      {subtitle && <div style={{ fontSize: '0.75rem', color: '#9ca3af', marginTop: '4px' }}>{subtitle}</div>}
    </div>
  );
}
