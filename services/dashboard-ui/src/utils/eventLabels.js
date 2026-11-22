export const EVENT_TYPE_LABELS = {
  login_attempt: 'Fake Login Probe',
  path_probe: 'Directory Traversal / Probe',
  page_access: 'Page View',
  invalid_request: 'Malformed Request',
  suspicious_request: 'Sensitive Asset Exfiltration'
};

export function getEventLabel(type) {
  return EVENT_TYPE_LABELS[type] || type || 'Unknown';
}
