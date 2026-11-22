const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8002';

export async function fetchApi(endpoint, options = {}) {
  try {
    const res = await fetch(`${API_BASE}${endpoint}`, {
      headers: {
        'Content-Type': 'application/json',
        ...(options.headers || {})
      },
      ...options
    });
    if (!res.ok) {
      throw new Error(`API Request failed with HTTP ${res.status}: ${res.statusText}`);
    }
    return await res.json();
  } catch (err) {
    console.error(`Error in fetchApi [${endpoint}]:`, err);
    throw err;
  }
}
