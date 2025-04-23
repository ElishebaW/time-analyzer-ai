import axios from "axios";

const API_BASE_URL = "http://localhost:8000";

export async function queryDatabase(query: string, topK: number = 5) {
  const response = await axios.post(`${API_BASE_URL}/query`, {
    query,
    top_k: topK,
  });
  return response.data;
}