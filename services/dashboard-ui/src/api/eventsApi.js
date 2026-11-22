import { fetchApi } from './apiClient';

export async function getEvents(params = {}) {
  const query = new URLSearchParams();
  if (params.limit) query.append('limit', params.limit);
  if (params.offset) query.append('offset', params.offset);
  if (params.event_type) query.append('event_type', params.event_type);
  if (params.source_ip) query.append('source_ip', params.source_ip);
  if (params.severity) query.append('severity', params.severity);

  const qs = query.toString();
  return await fetchApi(`/api/events${qs ? `?${qs}` : ''}`);
}

export async function getEventDetail(id) {
  return await fetchApi(`/api/events/${id}`);
}
