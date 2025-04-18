import os
import datetime
import chromadb
import subprocess
from unstructured.partition.pdf import partition_pdf
from unstructured.partition.csv import partition_csv
from langchain.text_splitter import RecursiveCharacterTextSplitter, SentenceTransformersTokenTextSplitter
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

# Initialize ChromaDB client
chroma_client = chromadb.PersistentClient(path="./chromadb")


# Function to split text into chunks
def split_text_into_chunks(text, chunk_size=500, chunk_overlap=50):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )
    return text_splitter.split_text(text)

# Function to process PDF or CSV files and extract text
def process_file(file_path):
    if file_path.endswith(".pdf"):
        elements = partition_pdf(filename=file_path)
    elif file_path.endswith(".csv"):
        elements = partition_csv(filename=file_path)
    else:
        raise ValueError("Unsupported file format. Only PDF and CSV files are supported.")

    # Combine the partitioned elements into a single text
    combined_text = "\n".join([str(element) for element in elements])
    return combined_text

# Function to find today's and yesterday's files in the Downloads directory
def find_files_in_downloads():
    download_dir = os.path.expanduser("~/Downloads")  # Path to the Downloads directory

    # Get today's and yesterday's dates
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)

    # Expected filename patterns
    filename_base_today = f"Toggl_Track_summary_report_{today}_{today}"
    filename_base_yesterday = f"Toggl_Track_summary_report_{yesterday}_{yesterday}"

    # Search for today's file
    today_file = None
    for ext in [".csv", ".pdf"]:
        file_path = os.path.join(download_dir, f"{filename_base_today}{ext}")
        if os.path.exists(file_path):
            today_file = file_path
            break

    # Search for yesterday's file
    yesterday_file = None
    for ext in [".csv", ".pdf"]:
        file_path = os.path.join(download_dir, f"{filename_base_yesterday}{ext}")
        if os.path.exists(file_path):
            yesterday_file = file_path
            break

    if not today_file:
        raise FileNotFoundError(f"No Toggl Track summary report found for today ({today}) in Downloads.")
    if not yesterday_file:
        raise FileNotFoundError(f"No Toggl Track summary report found for yesterday ({yesterday}) in Downloads.")

    return today_file, yesterday_file

# Function to add text and embeddings to ChromaDB
def add_to_chromadb(text, collection_name="time_analysis"):
    # Split text into chunks
    chunks = split_text_into_chunks(text)
    type(chunks)
    len(chunks)
    print(f"chunks: {chunks[0:2]}")  # Print first two chunks for debugging

    token_split_texts = split_text_into_tokens(chunks)

    embedding_function = SentenceTransformerEmbeddingFunction()
    print(embedding_function([token_split_texts[10]]))

    # Create or get a ChromaDB collection
    collection = chroma_client.get_or_create_collection(name=collection_name, embedding_function=embedding_function)

    # Add chunks and embeddings to the collection

    ids = [str(i) for i in range(len(token_split_texts))]
  
    collection.add(documents=token_split_texts,ids=ids)

    print(f"Added {len(token_split_texts)} split texts to the ChromaDB collection '{collection_name}'.")

def split_text_into_tokens(chunks):
    token_splitter = SentenceTransformersTokenTextSplitter(chunk_overlap=0, tokens_per_chunk=256)

    token_split_texts = []
    for text in chunks:
        token_split_texts += token_splitter.split_text(text)
    return token_split_texts

# Function to send text and prompt to the local LLM
def send_to_llm(today_text, yesterday_text, output_file="time_analyze.md"):
    # Define the prompt
    prompt = f"""
You are my productivity coach. You will receive structured time tracking data for TODAY and YESTERDAY as JSON.

Your task is to:
- Compare the time and projects between TODAY and YESTERDAY.
- ONLY use the entries listed under each specific date — never infer or carry over tasks between days.
- Do not assume any project happened on both days unless it appears in both TODAY and YESTERDAY sections.
- Assign a productivity score for TODAY (0–100), based on time usage, task quality, and inclusion of rest or walking breaks.
- Suggest 2–3 improvements to my time usage. Breaks and walking are considered positive.
- Your output should be in clean markdown.
- Make it specific to the data provided, without any assumptions or inferences not generic.
- Important: Do NOT hallucinate or infer data. ONLY use the fields explicitly provided under each date. If you're not sure, say "I'm not sure how you can improve the time.".

TODAY:
{today_text}

YESTERDAY:
{yesterday_text}
"""

    # Write the date to the output file
    today = datetime.date.today()
    with open(output_file, "w") as f:
        f.write(f"# {today}\n")

    # Send the prompt and text to the local LLM using `ollama`
    try:
        result = subprocess.run(
            ["ollama", "run", "llama3.2", prompt],
            capture_output=True,
            text=True
        )
        # Append the LLM's response to the output file
        with open(output_file, "a") as f:
            f.write(result.stdout)
        print(f"Analysis saved to {output_file}")
    except FileNotFoundError:
        raise EnvironmentError("ollama is not installed or not in PATH. Please ensure it is installed.")


# Main function
if __name__ == "__main__":
    # Find files for TODAY and YESTERDAY in the Downloads directory
    print("Searching for files in Downloads...")
    today_file, yesterday_file = find_files_in_downloads()

    # Process today's file
    print(f"Processing today's file: {today_file}")
    today_text = process_file(today_file)

    # Process yesterday's file
    print(f"Processing yesterday's file: {yesterday_file}")
    yesterday_text = process_file(yesterday_file)

    # Combine today's and yesterday's text
    combined_text = f"TODAY:\n{today_text}\n\nYESTERDAY:\n{yesterday_text}"

    # Add combined text to ChromaDB
    add_to_chromadb(combined_text, collection_name="time_analysis")

      # Send the extracted text and prompt to the local LLM
    send_to_llm(today_text, yesterday_text)

    print("Analysis complete.")