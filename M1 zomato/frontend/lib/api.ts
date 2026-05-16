const API_URL_LOCAL = "http://localhost:5001/api/recommend";
const API_URL_PRODUCTION =
  "https://web-production-9d250.up.railway.app/api/recommend";

/** Same contract as phase2/config.js — optional Next.js dev UI. */
export function getRecommendApiUrl(): string {
  if (process.env.NEXT_PUBLIC_API_URL) {
    return process.env.NEXT_PUBLIC_API_URL;
  }
  if (typeof window !== "undefined") {
    const host = window.location.hostname;
    const isLocal =
      host === "localhost" || host === "127.0.0.1";
    return isLocal ? API_URL_LOCAL : API_URL_PRODUCTION;
  }
  return API_URL_LOCAL;
}
