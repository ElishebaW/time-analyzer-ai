import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from analyze_api import app, query_chromadb, send_to_llm, expand_query, rerank_documents_with_cross_encoder

# Create a TestClient instance
client = TestClient(app)

# Test the root endpoint
def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the RAG API powered by ChromaDB and FastAPI!"}

# Test the query endpoint
def test_query_database():
    with patch('analyze_api.query_chromadb') as mock_query, \
         patch('analyze_api.send_to_llm') as mock_send:
        
        mock_query.return_value = ["test document 1", "test document 2"]
        mock_send.return_value = "test response"
        
        response = client.post("/query", json={"query": "test query", "top_k": 5})
        
        assert response.status_code == 200
        assert "query" in response.json()
        assert "context" in response.json()
        assert "response" in response.json()

# Test query_chromadb function
def test_query_chromadb():
    with patch('analyze_api.expand_query') as mock_expand, \
         patch('analyze_api.rerank_documents_with_cross_encoder') as mock_rerank:
        
        mock_expand.return_value = "expanded query"
        mock_rerank.return_value = ["test document"]
        
        result = query_chromadb("test query", 5)
        
        assert len(result) > 0
        mock_expand.assert_called_once_with("test query")
        mock_rerank.assert_called_once()

# Test expand_query function
def test_expand_query():
    with patch('analyze_api.pipeline') as mock_pipeline:
        mock_generator = MagicMock()
        mock_pipeline.return_value = mock_generator
        mock_generator.return_value = [{"generated_text": "expanded query"}]
        
        result = expand_query("test query")
        assert result == "expanded query"

# Test rerank_documents_with_cross_encoder
def test_rerank_documents_with_cross_encoder():
    query = "test query"
    documents = ["doc1", "doc2"]
    
    with patch('analyze_api.CrossEncoder') as mock_encoder:
        mock_encoder.return_value.predict.return_value = [0.9, 0.8]
        
        result = rerank_documents_with_cross_encoder(query, documents)
        assert len(result) == len(documents)
        assert isinstance(result, list)

# Test send_to_llm
def test_send_to_llm():
    with patch('analyze_api.ChatOllama') as mock_llm:
        mock_llm.return_value.invoke.return_value = MagicMock(content="test response")
        
        result = send_to_llm("test prompt")
        assert result == "test response"

# Test send_to_llm with ollama not installed
def test_send_to_llm_ollama_not_installed():
    with patch('analyze_api.ChatOllama', side_effect=FileNotFoundError):
        with pytest.raises(Exception) as exc_info:
            send_to_llm("test prompt")
        assert "ollama is not installed or not in PATH" in str(exc_info.value)