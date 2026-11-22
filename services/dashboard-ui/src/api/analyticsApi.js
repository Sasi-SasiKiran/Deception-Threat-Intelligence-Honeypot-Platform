import { fetchApi } from './apiClient';

export async function getDashboardSummary() {
  return await fetchApi('/api/dashboard/summary');
}

export async function getTimeline(hours = 24) {
  return await fetchApi(`/api/analytics/timeline?hours=${hours}`);
}

export async function getTopEndpoints(limit = 10) {
  return await fetchApi(`/api/analytics/endpoints?limit=${limit}`);
}

export async function getTopSources(limit = 10) {
  return await fetchApi(`/api/analytics/sources?limit=${limit}`);
}

export async function getEventTypes() {
  return await fetchApi('/api/analytics/event-types');
}
