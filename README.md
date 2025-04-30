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
- [Toggl Tracker](https://toggl.com/)
- (Optional) Docker if you prefer containerized setup

## ⚙️ Setup & Run

1. **Clone Repository**
   ```bash
   git clone https://github.com/ElishebaW/Local-LLM-Projects.git
   cd Local-LLM-Projects/time_analyzer_ai
   ```

2. **Backend**
   ```bash
   pip install langchain-community langchain-text-splitters langchain-huggingface langchain-chroma langchain-ollama pydantic json langchain-core sentence-transformers transformers
   # ensure Ollama & ChromaDB are running locally
   uvicorn analyzeapi:app --reload --host 0.0.0.0 --port 8000 or fastapi dev analyzeapi.py
   ```

3. **Frontend**
   ```bash
   cd analyze-time-front-end
   npm install
   npm run dev                   
   ```

4. **Use the App**
   - To start tracking your time you will need to create an account on Toggl and start tracking your time.
   - At the end of your day download a report from Toggl in CSV or ODF format to your Downloads folder, run analyze_time.py to add the embeddings to the ChromaDB and  get a summary of how you can be productive the next day in time_analyze.md.
   - When you are ready to ask questions on your data, open http://localhost:3000 in your browser.
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

## 📄 License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.