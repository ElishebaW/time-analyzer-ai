import chromadb
import subprocess
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_ollama import ChatOllama
from sentence_transformers import CrossEncoder
from transformers import pipeline


# Initialize FastAPI app
app = FastAPI()

CHROMA_DB_PATH = "./chromadb"

EMBEDDING_MODEL = "sentence-transformers/all-mpnet-base-v2"
embedding_function = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

# Initialize ChromaDB client
chroma_client = Chroma(persist_directory=CHROMA_DB_PATH, embedding_function=embedding_function)

# Initialize the Cross-Encoder model
cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

def expand_query(query):
    generator = pipeline("text2text-generation", model="t5-small")
    expanded_query = generator(f"Expand this query: {query}", max_length=50, num_return_sequences=1)
    return expanded_query[0]["generated_text"]

def rerank_documents_with_cross_encoder(query_text, documents):
    """
    Rerank documents using a Cross-Encoder.
    """

    # Step 1: Ensure each document is a single string
    processed_documents = [
        "\n".join(doc) if isinstance(doc, list) else doc
        for doc in documents
    ]

    # Step 2: Create query-document pairs
    pairs = [[query_text, doc] for doc in processed_documents if isinstance(doc, str) and doc.strip()]

    # Check if pairs are valid
    if not pairs:
        raise ValueError("No valid query-document pairs found for reranking.")

    # Step 3: Predict relevance scores for each pair
    scores = cross_encoder.predict(pairs, batch_size=16)

    # Step 4: Sort documents by their scores in descending order
    ranked_documents = sorted(zip(processed_documents, scores), key=lambda x: x[1], reverse=True)

    # Return only the documents, sorted by relevance
    return [doc for doc, _ in ranked_documents]

# Function to query ChromaDB
def query_chromadb(query_text: str, top_k: int = 5):

    # Step 1: Expand the query
    expanded_query = expand_query(query_text)

    # Retrieve similar documents via Langchain-Chroma
    # Chroma vector store has similarity_search
    docs = chroma_client.similarity_search(expanded_query, k=top_k)
    # Extract text content
    documents = [getattr(doc, 'page_content', str(doc)) for doc in docs]

    # Step 4: Rerank the documents
    return rerank_documents_with_cross_encoder(query_text, documents)

# Function to send the augmented prompt to the local LLM
def send_to_llm(prompt: str):

    if isinstance(prompt, list):
        prompt = json.dumps(prompt)

    try:
        llm = ChatOllama(
            model="codellama",
            temperature=0,
        )
        response = llm.invoke(prompt)
        return response.content
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="ollama is not installed or not in PATH.")

# API Models
class QueryRequest(BaseModel):
    query: str
    top_k: int = 5

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Front-end origin (Next.js dev server)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)
# API Endpoints

@app.get("/")
def read_root():
    return {"message": "Welcome to the RAG API powered by ChromaDB and FastAPI!"}

@app.post("/query")
def query_database(request: QueryRequest):
    """
    Query the ChromaDB database and send the augmented query to the LLM.
    """
    # Step 1: Retrieve relevant documents from ChromaDB
    documents = query_chromadb(request.query, top_k=request.top_k)

    # Step 2: Combine the query and retrieved documents into a prompt
    context = "\n\n".join(documents)
    prompt = f"""
        You are my productivity coach. Below is some context retrieved from my time-tracking database, followed by my query.

        Context:
        {context}

        Query:
        {request.query}

        Your task is to:
        - Use the context to answer the query as accurately as possible.
        - If the context does not contain enough information, respond with "I don't have enough information to answer this query."
        - Your response should be in clean markdown format.
        """

    messages = [
        {
            "role": "system",
            "content": prompt
        },
        {"role": "user", "content": request.query}
    ] 

    # Step 3: Send the prompt to the local LLM
    response = send_to_llm(messages)

    return {"query": request.query, "context": context, "response": response}