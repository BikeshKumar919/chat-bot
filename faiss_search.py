
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# 1. Load the embedding model
print("Loading embedding model...")
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# 2. Create our knowledge base
documents = [
    "JWT tokens are used to authenticate requests to protected APIs.",
    "Redis is an in-memory data store often used for caching.",
    "Spring Boot makes it easier to build Java backend applications.",
    "A neural network learns patterns from training data.",
    "SQLite stores structured data in a local database file.",
]

# 3. Convert documents into embeddings
document_embeddings = model.encode(
    documents,
    convert_to_numpy=True
)

# 4. FAISS expects a two-dimensional NumPy array of float32
document_embeddings = np.asarray(
    document_embeddings,
    dtype="float32"
)

# 5. Normalize vectors so L2 distance gives cosine-similarity ranking
faiss.normalize_L2(document_embeddings)

# 6. Create a FAISS index
embedding_dimension = document_embeddings.shape[1]
index = faiss.IndexFlatIP(embedding_dimension)

# 7. Add the document vectors to the index
index.add(document_embeddings)

print("Number of indexed documents:", index.ntotal)

# 8. Ask a question
question = "How can I verify a user's identity when calling an API?"

# 9. Convert the question into an embedding
question_embedding = model.encode(
    [question],
    convert_to_numpy=True
).astype("float32")

# 10. Normalize the question vector too
faiss.normalize_L2(question_embedding)

# 11. Search for the three most relevant documents
scores, indices = index.search(question_embedding, k=3)

# 12. Display the results
print("\nQuestion:", question)
print("\nMost relevant documents:\n")

for score, idx in zip(scores[0], indices[0]):
    print(f"Similarity: {score:.3f}")
    print(f"Document: {documents[idx]}")
    print("-" * 60)
