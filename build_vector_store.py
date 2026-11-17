
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter

from load_documents import load_documents


# 1. Locate the project directory
project_dir = Path(__file__).parent


# 2. Load the embedding model
print("Loading embedding model...")

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)


# 3. Configure the text splitter
splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50,
    separators=["\n\n", "\n", ". ", " ", ""],
)


# 4. Load TXT and PDF documents
print("\nLoading documents...")

documents = load_documents()


# 5. Split documents into chunks
print("\nSplitting documents...")

split_documents = splitter.split_documents(documents)

chunks = []
metadata = []

source_chunk_counts = {}

for doc in split_documents:

    source = Path(doc.metadata.get("source", "unknown")).name

    # Keep a separate chunk count for each source file
    source_chunk_counts[source] = (
        source_chunk_counts.get(source, 0) + 1
    )

    chunks.append(doc.page_content)

    metadata.append({
        "source": source,
        "chunk": source_chunk_counts[source],
        "page": doc.metadata.get("page", -1),
    })


if not chunks:
    raise ValueError("No document chunks found.")


print(f"Total chunks created: {len(chunks)}")


# 6. Convert chunks into embeddings
print("\nGenerating embeddings...")

embeddings = model.encode(
    chunks,
    convert_to_numpy=True,
    show_progress_bar=True,
).astype("float32")


# 7. Normalize embeddings for cosine similarity
faiss.normalize_L2(embeddings)


# 8. Build the FAISS index
dimension = embeddings.shape[1]

index = faiss.IndexFlatIP(dimension)

index.add(embeddings)


# 9. Save FAISS index and metadata
store_dir = project_dir / "vector_store"

store_dir.mkdir(exist_ok=True)

faiss.write_index(
    index,
    str(store_dir / "documents.faiss")
)

np.savez(
    store_dir / "documents_data.npz",
    chunks=np.array(chunks, dtype=str),
    sources=np.array(
        [item["source"] for item in metadata],
        dtype=str
    ),
    chunk_numbers=np.array(
        [item["chunk"] for item in metadata]
    ),
    pages=np.array(
        [item["page"] for item in metadata]
    ),
)


print("\n========== VECTOR STORE CREATED ==========")
print(f"FAISS index contains {index.ntotal} vectors.")
print(f"Total chunks: {len(chunks)}")
print(f"Vector store saved to: {store_dir}")

print("\nSource files:")

for source in sorted(source_chunk_counts):
    print(
        f"{source}: {source_chunk_counts[source]} chunks"
    )
