import React, { useState } from 'react';
import EventTable from '../components/EventTable';
import FilterBar from '../components/FilterBar';
import EventDetailsModal from '../components/EventDetailsModal';
import LoadingState from '../components/LoadingState';
import { useEvents } from '../hooks/useEvents';

export default function LiveEvents() {
  const [filters, setFilters] = useState({ limit: 50 });
  const { events, loading, error, refetch } = useEvents(filters, 2500);
  const [selectedEvent, setSelectedEvent] = useState(null);

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
        <p style={{ color: '#9ca3af', fontSize: '0.9rem' }}>
          Real-time stream of incoming adversary probes, fake logins, and scanner traffic.
        </p>
        <button
          onClick={refetch}
          style={{
            background: '#374151',
            color: '#f9fafb',
            border: '1px solid #4b5563',
            padding: '6px 14px',
            borderRadius: '4px',
            cursor: 'pointer'
          }}
        >
          🔄 Refresh
        </button>
      </div>

      <FilterBar filters={filters} onChange={setFilters} />

      {loading && events.length === 0 ? (
        <LoadingState message="Polling live telemetry from Ingest database..." />
      ) : (
        <EventTable events={events} onSelectEvent={(evt) => setSelectedEvent(evt)} />
      )}

      <EventDetailsModal event={selectedEvent} onClose={() => setSelectedEvent(null)} />
    </div>
  );
}
