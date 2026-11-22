import { useState, useEffect } from 'react';
import { getDashboardSummary } from '../api/analyticsApi';

export function useLiveMetrics(pollingInterval = 4000) {
  const [metrics, setMetrics] = useState({
    total_events: 0,
    unique_attackers: 0,
    events_today: 0,
    decoy_status: 'ONLINE'
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let isMounted = true;
    async function loadMetrics() {
      try {
        const data = await getDashboardSummary();
        if (isMounted) {
          setMetrics(data);
          setLoading(false);
        }
      } catch (err) {
        console.warn('Metrics polling error:', err);
      }
    }
    loadMetrics();
    const timer = setInterval(loadMetrics, pollingInterval);
    return () => {
      isMounted = false;
      clearInterval(timer);
    };
  }, [pollingInterval]);

  return { metrics, loading };
}
