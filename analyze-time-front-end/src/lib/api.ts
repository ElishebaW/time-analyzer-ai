import axios from "axios";

const API_BASE_URL = "http://localhost:8000";

export type MetricsResponse = {
  queries_processed: number;
  avg_response_time_ms: number;
  system_health: string;
  runtime_seconds: number;
  chroma_collections: number;
  chroma_embeddings: number;
};

export async function queryDatabase(query: string, topK: number = 5) {
  const response = await axios.post(`${API_BASE_URL}/query`, {
    query,
    top_k: topK,
  });
  return response.data as { response: string };
}

export async function getMetrics() {
  const response = await axios.get(`${API_BASE_URL}/metrics`);
  return response.data as MetricsResponse;
}
