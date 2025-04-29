# 🚀 Time Analyzer AI
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)
![npm Version](https://img.shields.io/badge/npm-8%2B-blue)

## 🔑 Key Features

- **Natural Language Queries**: Ask your data questions like “How many hours on meetings last week?”
- **Local LLM**: Runs CodeLlama via [Ollama](https://ollama.com), no API keys or cloud calls.
- **Vector Search**: ChromaDB for embeddings & top-K similarity retrieval.
- **Modern UI**: Next.js + Tailwind CSS frontend for a responsive, accessible interface.
- **FastAPI Backend**: Lightning-fast API endpoints with uvicorn and CORS support.

## 🛠️ Prerequisites

- Python 3.9+
- Node.js 16+
- npm or yarn
- [Ollama](https://ollama.com/download)
- (Optional) Docker if you prefer containerized setup

## ⚙️ Setup & Run

1. **Clone Repository**
   ```bash
   git clone https://github.com/ElishebaW/Local-LLM-Projects.git
   cd Local-LLM-Projects/time_analyzer_ai
   ```

2. **Backend**
   ```bash
   python -m venv venv            # create venv
   source venv/bin/activate       # activate
   pip install -r requirements.txt
   # ensure Ollama & ChromaDB are running locally
   uvicorn analyzeapi:app --reload --host 0.0.0.0 --port 8000
   ```

3. **Frontend**
   ```bash
   cd analyze-time-front-end
   npm install
   npm run dev                   # starts Next.js on http://localhost:3000
   ```

4. **Use the App**
   - Open http://localhost:3000 in your browser.
   - Navigate to “Query” and enter your natural language question.

## 📋 API Example

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query":"Total design hours last month?","top_k":5}'
```

```json
{
  "response": "You spent 12.5 hours on design tasks last month..."
}
```

## 🧪 Testing

- **Backend**: `pytest` (ensure venv is active)
- **Frontend**: add Jest/React Testing Library as needed

## 📄 License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.