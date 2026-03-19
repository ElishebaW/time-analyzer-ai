import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-screen bg-slate-950 flex flex-col items-center justify-center px-4 py-16">
      <div className="text-center max-w-2xl">
        {/* Logo and Title */}
        <div className="mb-8">
          <div className="text-6xl mb-4">⏱️</div>
          <h1 className="text-5xl font-bold text-white mb-4">Time Analyzer AI</h1>
          <p className="text-xl text-slate-400 leading-relaxed">
            Analyze and query your time-tracking data effortlessly with AI-powered insights
          </p>
        </div>

        {/* Features */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
            <div className="text-3xl mb-3">🔍</div>
            <h3 className="text-lg font-semibold text-white mb-2">Natural Queries</h3>
            <p className="text-slate-400 text-sm">
              Ask questions in plain English about your time data
            </p>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
            <div className="text-3xl mb-3">📊</div>
            <h3 className="text-lg font-semibold text-white mb-2">Smart Analysis</h3>
            <p className="text-slate-400 text-sm">
              Get AI-powered insights and patterns from your data
            </p>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
            <div className="text-3xl mb-3">⚡</div>
            <h3 className="text-lg font-semibold text-white mb-2">Instant Results</h3>
            <p className="text-slate-400 text-sm">
              Receive immediate answers to your time queries
            </p>
          </div>
        </div>

        {/* CTA Button */}
        <div className="flex flex-col items-center gap-4">
          <Link 
            href="/query" 
            className="px-8 py-4 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-xl transition-all duration-200 text-lg shadow-lg hover:shadow-xl transform hover:scale-105"
          >
            Start Analyzing Your Time
          </Link>
          <p className="text-slate-500 text-sm">
            No setup required • Just ask questions about your data
          </p>
        </div>
      </div>
    </div>
  );
}