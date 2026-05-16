// Production frontend (phase2) — API URLs. Backend is unchanged.
window.APP_CONFIG = {
  API_URL_LOCAL: "http://localhost:5001/api/recommend",
  API_URL_PRODUCTION: "https://web-production-9d250.up.railway.app/api/recommend",

  getApiUrl() {
    const host = window.location.hostname;
    const isLocal =
      host === "localhost" || host === "127.0.0.1" || host === "";
    return isLocal ? this.API_URL_LOCAL : this.API_URL_PRODUCTION;
  },
};
