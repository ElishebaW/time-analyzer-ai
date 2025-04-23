// filepath: /nextjs-frontend/src/pages/index.tsx
import Link from "next/link";

export default function Home() {
  return (
    <div style={{ padding: "2rem", fontFamily: "Arial, sans-serif" }}>
      <h1>Welcome to the Time Analyzer AI App</h1>
      <p>
        Go to the query page to ask questions of your time!
      </p>
      <Link href="/query">
        <button
          style={{
            padding: "0.75rem 1.5rem",
            fontSize: "1rem",
            backgroundColor: "#0070f3",
            color: "#fff",
            border: "none",
            borderRadius: "5px",
            cursor: "pointer",
          }}
        >
          Go to Query Page
        </button>
      </Link>
    </div>
  );
}