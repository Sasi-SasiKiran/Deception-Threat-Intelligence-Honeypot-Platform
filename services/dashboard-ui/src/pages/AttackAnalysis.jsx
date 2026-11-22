import React, { useState, useEffect } from 'react';
import AttackMap from '../components/AttackMap';
import { getTopEndpoints, getEventTypes, getTopSources } from '../api/analyticsApi';

export default function AttackAnalysis() {
  const [endpoints, setEndpoints] = useState([]);
  const [types, setTypes] = useState([]);
  const [sources, setSources] = useState([]);

  useEffect(() => {
    async function loadData() {
      try {
        const [ep, ty, so] = await Promise.all([
          getTopEndpoints(8),
          getEventTypes(),
          getTopSources(10)
        ]);
        setEndpoints(ep);
        setTypes(ty);
        setSources(so);
      } catch (e) {
        console.error(e);
      }
    }
    loadData();
  }, []);

  return (
    <div>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', marginBottom: '24px' }}>
        <div style={{ background: '#1f2937', padding: '20px', borderRadius: '8px', border: '1px solid #374151' }}>
          <h3 style={{ fontSize: '1rem', marginBottom: '16px' }}>🎯 Most Targeted Endpoints</h3>
          {endpoints.map((item, idx) => (
            <div key={idx} style={{ display: 'flex', justifyContent: 'space-between', padding: '8px 0', borderBottom: '1px solid #374151', fontSize: '0.9rem' }}>
              <span style={{ fontFamily: 'monospace', color: '#38bdf8' }}>{item.endpoint}</span>
              <span style={{ fontWeight: 'bold' }}>{item.count} hits</span>
            </div>
          ))}
        </div>

        <div style={{ background: '#1f2937', padding: '20px', borderRadius: '8px', border: '1px solid #374151' }}>
          <h3 style={{ fontSize: '1rem', marginBottom: '16px' }}>📊 Attack Vector Breakdown</h3>
          {types.map((item, idx) => (
            <div key={idx} style={{ display: 'flex', justifyContent: 'space-between', padding: '8px 0', borderBottom: '1px solid #374151', fontSize: '0.9rem' }}>
              <span>{item.event_type}</span>
              <span style={{ color: '#10b981', fontWeight: 'bold' }}>{item.count}</span>
            </div>
          ))}
        </div>
      </div>

      <AttackMap sources={sources} />
    </div>
  );
}
