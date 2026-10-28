
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Locate the documents folder
documents_dir = Path(__file__).parent / "documents"

# Configure the text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50,
    separators=["\n\n", "\n", ". ", " ", ""],
)

# Load and split every text file
for file_path in documents_dir.glob("*.txt"):
    text = file_path.read_text(encoding="utf-8")

    chunks = text_splitter.split_text(text)

    print(f"\nFile: {file_path.name}")
    print(f"Total chunks: {len(chunks)}\n")

    for i, chunk in enumerate(chunks, start=1):
        print(f"--- Chunk {i} ---")
        print(chunk)
        print()
