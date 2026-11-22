import React from 'react';

export default function AttackMap({ sources }) {
  return (
    <div style={{ background: '#1f2937', padding: '20px', borderRadius: '8px', border: '1px solid #374151' }}>
      <h3 style={{ fontSize: '1rem', marginBottom: '16px', color: '#f3f4f6' }}>🗺️ Geographic & Network Distribution</h3>
      <div style={{
        height: '180px',
        backgroundColor: '#111827',
        borderRadius: '6px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        flexDirection: 'column',
        color: '#9ca3af',
        border: '1px dashed #374151'
      }}>
        <div style={{ fontSize: '2rem', marginBottom: '8px' }}>🌍</div>
        <div>Active Attack Origin Vectors: <strong style={{ color: '#38bdf8' }}>{sources?.length || 0} unique subnets</strong></div>
        <div style={{ fontSize: '0.8rem', color: '#6b7280', marginTop: '4px' }}>Simulated internal lab / Air-gapped boundary active</div>
      </div>
    </div>
  );
}
