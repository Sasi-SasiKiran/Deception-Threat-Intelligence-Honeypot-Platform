import React, { useState, useEffect } from 'react';
import StatCard from '../components/StatCard';
import EventTable from '../components/EventTable';
import ActivityChart from '../components/ActivityChart';
import EventDetailsModal from '../components/EventDetailsModal';
import { useLiveMetrics } from '../hooks/useLiveMetrics';
import { useEvents } from '../hooks/useEvents';
import { getTimeline } from '../api/analyticsApi';

export default function Overview() {
  const { metrics } = useLiveMetrics(3000);
  const { events, loading } = useEvents({ limit: 10 }, 3000);
  const [timelineData, setTimelineData] = useState([]);
  const [selectedEvent, setSelectedEvent] = useState(null);

  useEffect(() => {
    async function loadTimeline() {
      try {
        const data = await getTimeline(24);
        setTimelineData(data);
      } catch (e) {
        console.error(e);
      }
    }
    loadTimeline();
    const interval = setInterval(loadTimeline, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div>
      <div className="grid-kpi">
        <StatCard title="Total Intercepted Events" value={metrics.total_events} icon="🛡️" subtitle="Full capture lifecycle" />
        <StatCard title="Unique Attacker IPs" value={metrics.unique_attackers} icon="🎯" subtitle="Distinct adversary sources" />
        <StatCard title="Probes Today" value={metrics.events_today} icon="⚡" subtitle="Rolling 24-hr activity" />
        <StatCard title="Decoy Health" value={metrics.decoy_status} icon="🟢" subtitle="WordPress Honeytrap" />
      </div>

      <div style={{ marginBottom: '24px' }}>
        <ActivityChart data={timelineData} />
      </div>

      <div style={{ background: '#1f2937', padding: '20px', borderRadius: '8px', border: '1px solid #374151' }}>
        <h3 style={{ fontSize: '1rem', marginBottom: '16px' }}>🚨 Recent Decoy Interceptions</h3>
        <EventTable events={events} onSelectEvent={(evt) => setSelectedEvent(evt)} />
      </div>

      <EventDetailsModal event={selectedEvent} onClose={() => setSelectedEvent(null)} />
    </div>
  );
}
