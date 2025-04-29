// filepath: /nextjs-frontend/src/pages/index.tsx
import Link from "next/link";

export default function Home() {
  return (
    <div className="container mx-auto px-8 py-16 font-sans text-gray-900 dark:text-gray-100">
      <h1 className="text-5xl font-bold mb-4 text-center">Time Analyzer AI</h1>
      <p className="text-lg mb-8 text-center">Analyze and query your time-tracking data effortlessly.</p>
      <div className="flex justify-center">
        <Link href="/query" className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-md font-medium transition">

            Go to Query Page
       
        </Link>
      </div>
    </div>
  );
}