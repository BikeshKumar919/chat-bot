
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# 1. Locate the saved vector store
project_dir = Path(__file__).parent
store_dir = project_dir / "vector_store"

index_path = store_dir / "documents.faiss"
data_path = store_dir / "documents_data.npz"

# 2. Load the saved FAISS index
index = faiss.read_index(str(index_path))

# 3. Load chunks and metadata
with np.load(data_path, allow_pickle=False) as data:
    chunks = data["chunks"].tolist()
    sources = data["sources"].tolist()
    chunk_numbers = data["chunk_numbers"].tolist()
    pages = data["pages"].tolist()

# 4. Load the same embedding model
model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

# 5. Ask a question
question = input(
    "Ask a question about your documents: "
).strip()

if not question:
    raise ValueError("Please enter a question.")

# 6. Embed the question
query_embedding = model.encode(
    [question],
    convert_to_numpy=True,
).astype("float32")

# 7. Normalize the query vector
faiss.normalize_L2(query_embedding)

# 8. Search FAISS
k = min(3, index.ntotal)
scores, indices = index.search(query_embedding, k)

# 9. Display matching chunks
print("\nRelevant passages:\n")

for score, idx in zip(scores[0], indices[0]):

    if idx < 0:
        continue

    print(f"Similarity: {score:.3f}")
    print(f"Source: {sources[idx]}")
    print(f"Chunk: {chunk_numbers[idx]}")

    if pages[idx] >= 0:
        print(f"PDF Page: {pages[idx] + 1}")
    else:
        print("PDF Page: N/A (Text file)")

    print(f"\nContent:\n{chunks[idx]}")
    print("-" * 60)
