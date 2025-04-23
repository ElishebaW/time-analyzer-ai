"use client";
import { useState } from "react";
import { queryDatabase } from "../utils/api";
import axios from "axios";

export default function QueryPage() {
  const [query, setQuery] = useState("");
  const [topK, setTopK] = useState(5);
  const [response, setResponse] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResponse(null);

    try {
          // Send the data as JSON in the request body
        const res = await axios.post("http://localhost:8000/query", {
          query: query.trim(),
          top_k: topK,
        });
        setResponse(res.data.response);
    } catch (err: any) {
      setError(err.message || "An error occurred");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "Arial, sans-serif" }}>
      <h1>Query the Database</h1>
      <form onSubmit={handleSubmit} style={{ marginBottom: "2rem" }}>
        <div style={{ marginBottom: "1rem" }}>
          <label htmlFor="query" style={{ display: "block", marginBottom: "0.5rem" }}>
            Enter your query:
          </label>
          <input
            id="query"
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            style={{ width: "100%", padding: "0.5rem", fontSize: "1rem" }}
            required
          />
        </div>
        <div style={{ marginBottom: "1rem" }}>
          <label htmlFor="topK" style={{ display: "block", marginBottom: "0.5rem" }}>
            Number of results (top_k):
          </label>
          <input
            id="topK"
            type="number"
            value={topK}
            onChange={(e) => setTopK(Number(e.target.value))}
            style={{ width: "100%", padding: "0.5rem", fontSize: "1rem" }}
            min={1}
            max={20}
          />
        </div>
        <button
          type="submit"
          style={{
            padding: "0.75rem 1.5rem",
            fontSize: "1rem",
            backgroundColor: "#0070f3",
            color: "#fff",
            border: "none",
            borderRadius: "5px",
            cursor: "pointer",
          }}
          disabled={loading}
        >
          {loading ? "Loading..." : "Submit"}
        </button>
      </form>

      {error && <p style={{ color: "red" }}>Error: {error}</p>}
      {response && (
        <div style={{ marginTop: "2rem" }}>
          <h2>Response:</h2>
          <pre
            style={{
              backgroundColor: "#f4f4f4",
              padding: "1rem",
              borderRadius: "5px",
              whiteSpace: "pre-wrap",
            }}
          >
            {response}
          </pre>
        </div>
      )}
    </div>
  );
}