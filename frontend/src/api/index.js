const BASE = "/api";

async function request(url, options = {}) {
  const res = await fetch(`${BASE}${url}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || `HTTP ${res.status}`);
  }
  const text = await res.text();
  return text ? JSON.parse(text) : null;
}

export const api = {
  // Trades
  createTrade(data) {
    return request("/trades", { method: "POST", body: JSON.stringify(data) });
  },
  listTrades(params = {}) {
    const qs = new URLSearchParams();
    Object.entries(params).forEach(([k, v]) => {
      if (v) qs.set(k, v);
    });
    const suffix = qs.toString() ? `?${qs}` : "";
    return request(`/trades${suffix}`);
  },
  getTrade(id) {
    return request(`/trades/${id}`);
  },
  updateTrade(id, data) {
    return request(`/trades/${id}`, {
      method: "PUT",
      body: JSON.stringify(data),
    });
  },
  deleteTrade(id) {
    return request(`/trades/${id}`, { method: "DELETE" });
  },

  // Reviews
  upsertReview(data) {
    return request("/reviews", {
      method: "POST",
      body: JSON.stringify(data),
    });
  },
  listReviews(params = {}) {
    const qs = new URLSearchParams();
    Object.entries(params).forEach(([k, v]) => {
      if (v) qs.set(k, v);
    });
    const suffix = qs.toString() ? `?${qs}` : "";
    return request(`/reviews${suffix}`);
  },
  getReview(dateStr) {
    return request(`/reviews/${dateStr}`);
  },

  // Summary
  getSummary(params) {
    const qs = new URLSearchParams();
    Object.entries(params).forEach(([k, v]) => {
      if (v != null && v !== "") qs.set(k, v);
    });
    return request(`/summary?${qs}`);
  },
};
