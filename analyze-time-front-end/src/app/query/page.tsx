"use client";
import { useState } from "react";
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
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-gray-100 flex flex-col items-center py-12 px-4">
      <div className="w-full max-w-lg bg-white dark:bg-gray-800 p-8 rounded-lg shadow-lg">
        <h1 className="text-2xl font-semibold mb-6 text-center">Query Your Time Data</h1>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="query" className="block text-sm font-medium">Enter your query</label>
            <input
              id="query"
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              required
              className="mt-1 block w-full px-3 py-2 bg-gray-100 dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
          <div>
            <label htmlFor="topK" className="block text-sm font-medium">Number of results</label>
            <input
              id="topK"
              type="number"
              value={topK}
              onChange={(e) => setTopK(Number(e.target.value))}
              min={1}
              max={20}
              className="mt-1 block w-full px-3 py-2 bg-gray-100 dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
          <button
            type="submit"
            disabled={loading}
            className="w-full py-2 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-md transition disabled:opacity-50"
          >
            {loading ? "Loading..." : "Submit"}
          </button>
        </form>
        {error && <p className="mt-4 text-red-500 text-center">Error: {error}</p>}
        {response && (
          <div className="mt-6 bg-gray-100 dark:bg-gray-700 p-4 rounded-md">
            <h2 className="text-lg font-medium mb-2">Response:</h2>
            <pre className="whitespace-pre-wrap text-sm text-gray-800 dark:text-gray-200">{response}</pre>
          </div>
        )}
      </div>
    </div>
  );
}