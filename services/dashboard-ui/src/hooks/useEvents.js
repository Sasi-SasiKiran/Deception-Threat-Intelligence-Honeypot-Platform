import { useState, useEffect, useCallback } from 'react';
import { getEvents } from '../api/eventsApi';

export function useEvents(filters = {}, refreshInterval = 5000) {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchLatestEvents = useCallback(async () => {
    try {
      const data = await getEvents(filters);
      setEvents(data);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [JSON.stringify(filters)]);

  useEffect(() => {
    fetchLatestEvents();
    if (refreshInterval > 0) {
      const interval = setInterval(fetchLatestEvents, refreshInterval);
      return () => clearInterval(interval);
    }
  }, [fetchLatestEvents, refreshInterval]);

  return { events, loading, error, refetch: fetchLatestEvents };
}
