export function getSeverityBadgeClass(severity) {
  const s = (severity || 'low').toLowerCase();
  switch (s) {
    case 'critical':
      return 'badge badge-critical';
    case 'high':
      return 'badge badge-high';
    case 'medium':
      return 'badge badge-medium';
    default:
      return 'badge badge-low';
  }
}
