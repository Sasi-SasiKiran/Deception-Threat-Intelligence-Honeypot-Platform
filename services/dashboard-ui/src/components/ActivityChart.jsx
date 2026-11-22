import React from 'react';

export default function ActivityChart({ data }) {
  if (!data || data.length === 0) {
    return <div style={{ color: '#9ca3af', padding: '20px', textAlign: 'center' }}>No timeline telemetry yet.</div>;
  }

  const maxCount = Math.max(...data.map(d => d.count), 1);

  return (
    <div style={{ background: '#1f2937', padding: '20px', borderRadius: '8px', border: '1px solid #374151' }}>
      <h3 style={{ fontSize: '1rem', marginBottom: '16px', color: '#f3f4f6' }}>📈 Attack Velocity (Timeline)</h3>
      <div style={{ display: 'flex', alignItems: 'flex-end', gap: '8px', height: '140px', paddingBottom: '20px', borderBottom: '1px solid #374151' }}>
        {data.map((item, idx) => {
          const heightPercent = Math.max((item.count / maxCount) * 100, 10);
          return (
            <div key={idx} style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', height: '100%', justifyContent: 'flex-end' }}>
              <div style={{ fontSize: '0.75rem', color: '#38bdf8', marginBottom: '4px' }}>{item.count}</div>
              <div style={{
                width: '100%',
                height: `${heightPercent}%`,
                background: 'linear-gradient(180deg, #38bdf8 0%, #1e3a8a 100%)',
                borderRadius: '4px 4px 0 0'
              }} />
            </div>
          );
        })}
      </div>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '8px', fontSize: '0.75rem', color: '#9ca3af' }}>
        <span>Earlier</span>
        <span>Latest Activity</span>
      </div>
    </div>
  );
}
