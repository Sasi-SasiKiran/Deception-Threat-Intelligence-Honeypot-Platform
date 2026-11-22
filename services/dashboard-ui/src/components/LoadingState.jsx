import React from 'react';

export default function LoadingState({ message = "Loading telemetry feeds..." }) {
  return (
    <div style={{ padding: '60px', textAlign: 'center', color: '#9ca3af' }}>
      <div style={{ fontSize: '1.5rem', marginBottom: '8px' }}>🔄</div>
      <div>{message}</div>
    </div>
  );
}
