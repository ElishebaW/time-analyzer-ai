# Time Analyzer AI Frontend

Premium, responsive frontend for querying the Time Analyzer backend.

## Stack

- React + Vite + TypeScript
- Tailwind CSS
- Shadcn-style UI primitives (`Button`, `Input`, `Card`)
- Framer Motion animations

## Run locally

```bash
npm install
npm run dev
```

Vite serves the app on `http://localhost:5173` by default.

## Build

```bash
npm run build
npm run preview
```

## API expectations

The frontend sends POST requests to:

- `http://localhost:8000/query`

Payload:

```json
{
  "query": "your question",
  "top_k": 5
}
```
