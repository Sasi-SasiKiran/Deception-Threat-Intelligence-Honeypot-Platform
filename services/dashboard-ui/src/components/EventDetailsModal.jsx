import React from 'react';
import { formatDateTime } from '../utils/formatDate';
import { getSeverityBadgeClass } from '../utils/severity';

export default function EventDetailsModal({ event, onClose }) {
  if (!event) return null;

  return (
    <div style={{
      position: 'fixed',
      top: 0, left: 0, right: 0, bottom: 0,
      backgroundColor: 'rgba(0,0,0,0.7)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 1000
    }}>
      <div style={{
        backgroundColor: '#1f2937',
        border: '1px solid #374151',
        borderRadius: '8px',
        width: '650px',
        maxWidth: '90%',
        padding: '24px',
        color: '#f9fafb'
      }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
          <h3 style={{ margin: 0, fontSize: '1.2rem' }}>🔍 Event Forensic Details</h3>
          <button onClick={onClose} style={{ background: 'none', border: 'none', color: '#9ca3af', fontSize: '1.4rem', cursor: 'pointer' }}>&times;</button>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px', fontSize: '0.9rem', marginBottom: '16px' }}>
          <div><strong>Event ID:</strong> <span style={{ color: '#9ca3af', fontSize: '0.8rem' }}>{event.id}</span></div>
          <div><strong>Timestamp:</strong> {formatDateTime(event.timestamp)}</div>
          <div><strong>Source IP:</strong> <span style={{ color: '#38bdf8' }}>{event.source_ip}</span></div>
          <div><strong>Classification:</strong> {event.event_type}</div>
          <div><strong>HTTP Request:</strong> {event.method} {event.endpoint}</div>
          <div><strong>Response Code:</strong> {event.status_code}</div>
          <div><strong>Severity:</strong> <span className={getSeverityBadgeClass(event.severity)}>{event.severity}</span></div>
          <div><strong>Fingerprint:</strong> <span style={{ fontFamily: 'monospace' }}>{event.fingerprint || 'N/A'}</span></div>
        </div>

        <div style={{ marginBottom: '16px' }}>
          <strong>User Agent:</strong>
          <div style={{ background: '#111827', padding: '8px', borderRadius: '4px', fontSize: '0.8rem', fontFamily: 'monospace', marginTop: '4px', wordBreak: 'break-all' }}>
            {event.user_agent || 'Unknown'}
          </div>
        </div>

        <div>
          <strong>Captured & Sanitized Payload Summary:</strong>
          <pre style={{ background: '#111827', padding: '12px', borderRadius: '4px', fontSize: '0.8rem', marginTop: '4px', overflowX: 'auto' }}>
            {JSON.stringify(event.payload_summary, null, 2)}
          </pre>
        </div>

        <div style={{ marginTop: '20px', textAlign: 'right' }}>
          <button onClick={onClose} style={{
            background: '#38bdf8',
            color: '#0b0f19',
            border: 'none',
            padding: '8px 16px',
            borderRadius: '4px',
            fontWeight: 'bold',
            cursor: 'pointer'
          }}>
            Close
          </button>
        </div>
      </div>
    </div>
  );
}
