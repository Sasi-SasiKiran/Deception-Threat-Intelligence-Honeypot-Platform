import React from 'react';
import { formatDateTime } from '../utils/formatDate';
import { getEventLabel } from '../utils/eventLabels';
import { getSeverityBadgeClass } from '../utils/severity';

export default function EventTable({ events, onSelectEvent }) {
  if (!events || events.length === 0) {
    return (
      <div style={{ padding: '40px', textAlign: 'center', color: '#9ca3af' }}>
        No threat events captured yet.
      </div>
    );
  }

  return (
    <div className="table-container">
      <table>
        <thead>
          <tr>
            <th>Timestamp</th>
            <th>Attacker IP</th>
            <th>Method</th>
            <th>Endpoint</th>
            <th>Classification</th>
            <th>Response</th>
            <th>Severity</th>
          </tr>
        </thead>
        <tbody>
          {events.map((evt) => (
            <tr key={evt.id} onClick={() => onSelectEvent && onSelectEvent(evt)}>
              <td style={{ whiteSpace: 'nowrap' }}>{formatDateTime(evt.timestamp)}</td>
              <td style={{ fontFamily: 'monospace', color: '#38bdf8' }}>{evt.source_ip}</td>
              <td><strong>{evt.method}</strong></td>
              <td style={{ fontFamily: 'monospace' }}>{evt.endpoint}</td>
              <td>{getEventLabel(evt.event_type)}</td>
              <td>
                <span style={{ color: evt.status_code === 401 ? '#f59e0b' : '#9ca3af' }}>
                  {evt.status_code}
                </span>
              </td>
              <td>
                <span className={getSeverityBadgeClass(evt.severity)}>
                  {evt.severity}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
