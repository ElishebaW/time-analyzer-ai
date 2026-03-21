"use client";
import { useState } from "react";
import axios from "axios";

export default function QueryPage() {
  const [query, setQuery] = useState("");
  const [topK, setTopK] = useState(5);
  const [response, setResponse] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [copied, setCopied] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResponse(null);

    try {
      // Send data as JSON in request body
      const res = await axios.post("http://localhost:8000/query", {
        query: query.trim(),
        top_k: topK,
      });
      setResponse(res.data.response);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "An error occurred");
    } finally {
      setLoading(false);
    }
  };

  const handleCopy = async () => {
    if (response) {
      await navigator.clipboard.writeText(response);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const handleClear = () => {
    setQuery("");
    setResponse(null);
    setError(null);
    setTopK(5);
  };

  return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center px-4 py-8">
      <div className="w-full max-w-2xl">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-white mb-2">Time Analyzer AI</h1>
          <p className="text-slate-400">Ask anything about your time data</p>
        </div>

        {/* Query Form */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-8 shadow-2xl">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label htmlFor="query" className="block text-sm font-medium text-slate-300 mb-2">
                What would you like to know about your time?
              </label>
              <textarea
                id="query"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                required
                rows={4}
                className="w-full px-4 py-3 bg-slate-800 text-white rounded-lg border border-slate-700 focus:outline-none focus:ring-2 focus:ring-blue-600 focus:border-transparent resize-none transition-all placeholder-slate-500"
                placeholder="e.g., How many hours did I spend on Project X last week?"
              />
            </div>
            
            <div>
              <label htmlFor="topK" className="block text-sm font-medium text-slate-300 mb-2">
                Number of results
              </label>
              <input
                id="topK"
                type="number"
                value={topK}
                onChange={(e) => setTopK(Number(e.target.value))}
                min={1}
                max={20}
                className="w-full px-4 py-2 bg-slate-800 text-white rounded-lg border border-slate-700 focus:outline-none focus:ring-2 focus:ring-blue-600 focus:border-transparent transition-all"
              />
            </div>
            
            <button
              type="submit"
              disabled={loading || !query.trim()}
              className="w-full py-4 bg-blue-600 hover:bg-blue-700 disabled:bg-slate-700 disabled:cursor-not-allowed text-white font-semibold rounded-lg transition-all duration-200 flex items-center justify-center gap-2"
            >
              {loading ? (
                <>
                  <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                  Processing...
                </>
              ) : (
                "Ask AI"
              )}
            </button>
          </form>

          {/* Error Display */}
          {error && (
            <div className="mt-6 bg-red-900/20 border border-red-800 rounded-lg p-4">
              <p className="text-red-400 text-center">❌ {error}</p>
            </div>
          )}

          {/* Success Display */}
          {response && (
            <div className="mt-6 bg-slate-800 border border-slate-700 rounded-lg p-6">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-lg font-semibold text-white">📊 Analysis Result</h2>
                <div className="flex gap-2">
                  <button
                    onClick={handleCopy}
                    className="px-3 py-1 bg-slate-700 hover:bg-slate-600 text-slate-300 text-sm rounded-md transition-all duration-200 flex items-center gap-1"
                  >
                    {copied ? (
                      <>
                        <span>✓</span>
                        Copied!
                      </>
                    ) : (
                      <>
                        <span>📋</span>
                        Copy
                      </>
                    )}
                  </button>
                  <button
                    onClick={handleClear}
                    className="px-3 py-1 bg-slate-700 hover:bg-slate-600 text-slate-300 text-sm rounded-md transition-all duration-200 flex items-center gap-1"
                  >
                    <span>🗑️</span>
                    Clear
                  </button>
                </div>
              </div>
              <div className="bg-slate-900 rounded-md p-4 border border-slate-600">
                <pre className="whitespace-pre-wrap text-sm text-slate-200 leading-relaxed">{response}</pre>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}