
from sentence_transformers import SentenceTransformer, util

# 1. Load the embedding model
print("Loading embedding model...")

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

# 2. Create a small collection of documents
documents = [
    "JWT tokens are used to authenticate requests to protected APIs.",
    "Redis is an in-memory data store often used for caching.",
    "Spring Boot makes it easier to build Java backend applications.",
    "A neural network learns patterns from training data.",
    "SQLite stores structured data in a local database file.",
]

# 3. Convert every document into an embedding
document_embeddings = model.encode(
    documents,
    convert_to_tensor=True,
)

# 4. Ask a question
question = "How can I verify a user's identity when calling an API?"

# 5. Convert the question into an embedding
question_embedding = model.encode(
    question,
    convert_to_tensor=True,
)

# 6. Compare the question with every document
similarities = util.cos_sim(
    question_embedding,
    document_embeddings,
)[0]

# 7. Find the most relevant documents
top_results = similarities.topk(k=3)

print("\nQuestion:", question)
print("\nMost relevant documents:\n")

for score, index in zip(
    top_results.values,
    top_results.indices,
):
    print(f"Similarity: {score.item():.3f}")
    print(f"Document: {documents[index.item()]}")
    print("-" * 60)
