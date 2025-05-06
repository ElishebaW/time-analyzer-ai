import os
import datetime
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_ollama import ChatOllama
from langchain_core.documents import Document

# Initialize constants
CHROMA_DB_PATH = "./chromadb"
EMBEDDING_MODEL = "sentence-transformers/all-mpnet-base-v2"

# Get today's and yesterday's dates
today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)

# Function to find today's and yesterday's files in the Downloads directory
def find_files_in_downloads():
    download_dir = os.path.expanduser("~/Downloads")  # Path to the Downloads directory

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

# Function to process files using LangChain document loaders
def process_file(file_path):
    if file_path.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
    elif file_path.endswith(".csv"):
        loader = CSVLoader(file_path)
    else:
        raise ValueError("Unsupported file format. Only PDF and CSV files are supported.")

    # Load documents
    raw_documents = loader.load()

    # Convert raw documents to LangChain Document objects with metadata
    documents = [
        Document(
            page_content=doc.page_content,
            metadata={"source": file_path}
        )
        for doc in raw_documents
    ]
    return documents

# Function to split documents into chunks
def split_documents(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", " ", ""]
    )
    split_docs = text_splitter.split_documents(documents)

    # Ensure split documents are properly formatted
    formatted_docs = [
        Document(
            page_content=doc.page_content,
            metadata=doc.metadata
        )
        for doc in split_docs
    ]
    return formatted_docs

# Function to add documents to ChromaDB
def add_to_chromadb(documents, collection_name="time_analysis"):
    # Initialize embeddings and Chroma vector store
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vectorstore = Chroma(persist_directory=CHROMA_DB_PATH, embedding_function=embeddings)

    # Debugging: Print the structure of the documents
    print(f"Adding documents: {documents[:2]}")  # Print the first two documents for debugging

    # Add documents to the vector store
    vectorstore.add_documents(documents)

    print(f"Added {len(documents)} documents to the ChromaDB collection '{collection_name}'.")

# Function to send text and prompt to the local LLM
def send_to_llm(today_text, yesterday_text, output_file="time_analyze.md"):
    global today, yesterday
    
    # Define the prompt
    prompt = f"""[INST]
            You are my productivity coach. You will receive structured time tracking data for {today} and {yesterday} as JSON.

            Your task is to:
            - Compare the time and projects between {today} and {yesterday}.
            - ONLY use the entries listed under each specific date — never infer or carry over tasks between days.
            - Do not assume any project happened on both days unless it appears in both TODAY and YESTERDAY sections.
            - Assign a productivity score for {today}(0–100), based on time usage, task quality, and inclusion of rest or walking breaks.
            - Suggest 3–6 improvements to my time usage. Breaks and walking are considered positive.
            - Your output should be in clean markdown.
            - Make it specific to the data provided, without any generic assumptions or inferences not generic.
            - If you're not sure, say "I'm not sure how you can improve the time.".
            - For Pdf file .pdf type only look at the entries under TIME ENTRY DURATION
            - 4 hours a day is a good base line for productivity, 5-6 hours is considered a high performing days and 2-3 hours is ok if there are meetings and other distractions 

            TODAY - {today}:
            {today_text}

            YESTERDAY - {yesterday}:
            {yesterday_text}
            [/INST]
        """

    # Write the date to the output file
    with open(output_file, "w") as f:
        f.write(f"# {today}\n")

    # Send the prompt and text to the local LLM using `ollama`
    try:
        llm = ChatOllama(
            model="codellama",
            temperature=0,
        )

        response = llm.invoke(prompt)
        # Append the LLM's response to the output file
        with open(output_file, "a") as f:
            f.write(response.content)
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
    today_documents = process_file(today_file)

    # Process yesterday's file
    print(f"Processing yesterday's file: {yesterday_file}")
    yesterday_documents = process_file(yesterday_file)

    # Combine today's and yesterday's documents
    combined_documents = today_documents + yesterday_documents

    # Split documents into chunks
    print("Splitting documents into chunks...")
    split_docs = split_documents(combined_documents)

    # Add documents to ChromaDB
    print("Adding documents to ChromaDB...")
    add_to_chromadb(split_docs, collection_name="time_analysis")


    # Send the extracted text and prompt to the local LLM
    send_to_llm(
        today_text="\n".join([doc.page_content for doc in today_documents]),
        yesterday_text="\n".join([doc.page_content for doc in yesterday_documents])
    )

    print("Analysis complete.")