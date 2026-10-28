
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 1. Locate the documents folder
project_dir = Path(__file__).parent
documents_dir = project_dir / "documents"

# 2. Load the embedding model
print("Loading embedding model...")
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# 3. Configure the text splitter
splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50,
    separators=["\n\n", "\n", ". ", " ", ""],
)

# 4. Load and split all text documents
chunks = []
metadata = []

for file_path in documents_dir.glob("*.txt"):
    text = file_path.read_text(encoding="utf-8")
    file_chunks = splitter.split_text(text)

    for chunk_number, chunk in enumerate(file_chunks, start=1):
        chunks.append(chunk)
        metadata.append({
            "source": file_path.name,
            "chunk": chunk_number,
        })

if not chunks:
    raise ValueError("No text chunks found in the documents folder.")

print(f"Loaded {len(chunks)} chunks.")

# 5. Convert chunks into embeddings
embeddings = model.encode(
    chunks,
    convert_to_numpy=True,
    show_progress_bar=True,
).astype("float32")

# 6. Normalize embeddings for cosine-similarity search
faiss.normalize_L2(embeddings)

# 7. Build the FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatIP(dimension)
index.add(embeddings)

# 8. Save the index and associated text/metadata
store_dir = project_dir / "vector_store"
store_dir.mkdir(exist_ok=True)

faiss.write_index(index, str(store_dir / "documents.faiss"))

np.savez(
    store_dir / "documents_data.npz",
    chunks=np.array(chunks, dtype=str),
    sources=np.array([item["source"] for item in metadata], dtype=str),
    chunk_numbers=np.array([item["chunk"] for item in metadata]),
)

print(f"FAISS index contains {index.ntotal} vectors.")
print(f"Vector store saved to: {store_dir}")
