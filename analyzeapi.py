import os
import datetime
import chromadb
import subprocess
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from chromadb.utils import embedding_functions
from sentence_transformers import CrossEncoder
from transformers import pipeline

# Initialize FastAPI app
app = FastAPI()

# Initialize ChromaDB client
chroma_client = chromadb.PersistentClient(path="./chromadb")

embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction()

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
    # Step 1: Create query-document pairs

    pairs = [[query_text, doc] for doc in documents]


    print("Pairs:", pairs)

    # Step 2: Predict relevance scores for each pair
    scores = cross_encoder.predict(pairs, batch_size=16)

    # Step 3: Sort documents by their scores in descending order
    ranked_documents = sorted(zip(documents, scores), key=lambda x: x[1], reverse=True)

    # Return only the documents, sorted by relevance
    return [doc for doc, _ in ranked_documents]

# Function to query ChromaDB
def query_chromadb(query_text: str, collection_name: str = "time_analysis", top_k: int = 5):

       # Step 1: Expand the query
    expanded_query = expand_query(query_text)

    # Generate embedding for the query
    query_embedding = embedding_function([expanded_query])

    # Get the collection
    collection = chroma_client.get_or_create_collection(name=collection_name)

    # Query the collection
    results = collection.query(
        query_texts=query_text, 
        n_results=top_k, 
        include=['documents', 'embeddings'],
        query_embeddings=query_embedding
    )

    # Extract relevant documents
    documents = results.get("documents", [])

    # Step 4: Rerank the documents
    return rerank_documents_with_cross_encoder(query_text, documents)

# Function to send the augmented prompt to the local LLM
def send_to_llm(prompt: str):
    try:
        result = subprocess.run(
            ["ollama", "run", "llama3.2", prompt],
            capture_output=True,
            text=True
        )
        return result.stdout.strip()
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="ollama is not installed or not in PATH.")

# API Models
class QueryRequest(BaseModel):
    query: str
    top_k: int = 5

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
        - Suggest only short questions without compound sentences. Suggest a variety of questions that cover different aspects of the topic.
        - Make sure they are complete questions, and that they are related to the original question.
        - Output one question per line. Do not number the questions.
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