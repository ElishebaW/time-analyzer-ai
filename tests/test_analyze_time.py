from unittest.mock import MagicMock, patch
from analyze_time import (
    find_files_in_downloads,
    process_file,
    split_documents,
    add_to_chromadb,
    send_to_llm
)

# Test find_files_in_downloads
def test_find_files_in_downloads():
    with patch('os.path.exists') as mock_exists:
        mock_exists.return_value = True
        today_file, yesterday_file = find_files_in_downloads()
        
        assert today_file.endswith('.pdf') or today_file.endswith('.csv')
        assert yesterday_file.endswith('.pdf') or yesterday_file.endswith('.csv')

# Test process_file
def test_process_file_pdf():
    mock_loader = MagicMock()
    mock_loader.load.return_value = [MagicMock(page_content="test content")]
    
    with patch('analyze_time.PyPDFLoader', return_value=mock_loader):
        documents = process_file("test.pdf")
        assert len(documents) == 1
        assert documents[0].page_content == "test content"

def test_process_file_csv():
    mock_loader = MagicMock()
    mock_loader.load.return_value = [MagicMock(page_content="test content")]
    
    with patch('analyze_time.CSVLoader', return_value=mock_loader):
        documents = process_file("test.csv")
        assert len(documents) == 1
        assert documents[0].page_content == "test content"

# Test split_documents
def test_split_documents():
    mock_docs = [MagicMock(page_content="test content", metadata={"source": "test"})]
    split_docs = split_documents(mock_docs)
    assert len(split_docs) > 0

# Test add_to_chromadb
def test_add_to_chromadb():
    mock_docs = [MagicMock(page_content="test content")]
    with patch('analyze_time.HuggingFaceEmbeddings') as mock_embeddings, \
         patch('analyze_time.Chroma') as mock_chroma:
        
        add_to_chromadb(mock_docs)
        mock_chroma.return_value.add_documents.assert_called_once_with(mock_docs)

# Test send_to_llm
def test_send_to_llm():
    with patch('analyze_time.ChatOllama') as mock_llm, \
         patch('builtins.open', create=True) as mock_open:
        
        mock_llm.return_value.invoke.return_value = MagicMock(content="test analysis")
        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file
        
        send_to_llm("test today text", "test yesterday text")
        
        mock_llm.return_value.invoke.assert_called_once()
        mock_file.write.assert_called()