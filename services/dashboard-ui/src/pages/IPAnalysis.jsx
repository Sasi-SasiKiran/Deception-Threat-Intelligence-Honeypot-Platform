import React, { useState, useEffect } from 'react';
import { getTopSources } from '../api/analyticsApi';
import { formatDateTime } from '../utils/formatDate';

export default function IPAnalysis() {
  const [sources, setSources] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadSources() {
      try {
        const data = await getTopSources(20);
        setSources(data);
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    }
    loadSources();
  }, []);

  return (
    <div style={{ background: '#1f2937', padding: '20px', borderRadius: '8px', border: '1px solid #374151' }}>
      <h3 style={{ fontSize: '1rem', marginBottom: '8px' }}>🌐 Attacker IP Profiling & IOC Ledger</h3>
      <p style={{ color: '#9ca3af', fontSize: '0.85rem', marginBottom: '20px' }}>
        Passive analysis of client IP interactions captured across the decoy perimeter.
      </p>

      <div className="table-container">
        <table>
          <thead>
            <tr>
              <th>Adversary Source IP</th>
              <th>Total Attacks / Probes</th>
              <th>Last Interception</th>
              <th>Profile State</th>
            </tr>
          </thead>
          <tbody>
            {sources.map((s, idx) => (
              <tr key={idx}>
                <td style={{ fontFamily: 'monospace', color: '#38bdf8', fontWeight: 'bold' }}>{s.source_ip}</td>
                <td>{s.count}</td>
                <td>{formatDateTime(s.last_seen)}</td>
                <td>
                  <span className="badge badge-high">HOSTILE PROBER</span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
