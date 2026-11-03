
import os
from pathlib import Path

import faiss
import numpy as np
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from langchain_openai import ChatOpenAI

# --------------------------------------------------
# 1. Load environment variables
# --------------------------------------------------

load_dotenv()

# --------------------------------------------------
# 2. Initialize Apex LLM
# --------------------------------------------------

llm = ChatOpenAI(
    model="free/glm-5.3-flash",
    base_url="https://api.apinex.bond/v1",
    api_key=os.environ["APEX_API_KEY"],
    temperature=0.2,
    max_tokens=500,
)

# --------------------------------------------------
# 3. Load saved FAISS vector store
# --------------------------------------------------

project_dir = Path(__file__).parent
store_dir = project_dir / "vector_store"

index = faiss.read_index(str(store_dir / "documents.faiss"))

with np.load(
    store_dir / "documents_data.npz",
    allow_pickle=False
) as data:
    chunks = data["chunks"].tolist()
    sources = data["sources"].tolist()
    chunk_numbers = data["chunk_numbers"].tolist()

print(f"Loaded {index.ntotal} vectors from FAISS.")

# --------------------------------------------------
# 4. Load embedding model
# --------------------------------------------------

print("Loading embedding model...")

embedding_model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

# --------------------------------------------------
# 5. Retrieve relevant document chunks
# --------------------------------------------------

def retrieve_documents(question, k=3):

    question_embedding = embedding_model.encode(
        [question],
        convert_to_numpy=True
    ).astype("float32")

    faiss.normalize_L2(question_embedding)

    k = min(k, index.ntotal)

    scores, indices = index.search(question_embedding, k)

    retrieved_context = []

    for score, idx in zip(scores[0], indices[0]):

        if idx < 0:
            continue

        retrieved_context.append(
            f"""
Source: {sources[idx]}
Chunk: {chunk_numbers[idx]}
Similarity: {score:.3f}

Content:
{chunks[idx]}
"""
        )

    return retrieved_context

# --------------------------------------------------
# 6. Generate an answer using retrieved context
# --------------------------------------------------

def ask_question(question):

    retrieved_documents = retrieve_documents(question)

    if not retrieved_documents:
        return "No relevant documents were found."

    context = "\n".join(retrieved_documents)

    prompt = f"""
You are a helpful Java backend programming assistant.

Answer the user's question using ONLY the information
provided in the context below.

If the context does not contain enough information,
clearly say that the answer is not available in the
provided documents.

Do not invent information.

Context:
{context}

User question:
{question}

Answer:
"""

    response = llm.invoke(prompt)

    return response.content

# --------------------------------------------------
# 7. Interactive chatbot
# --------------------------------------------------

print("\n===== Java Backend RAG Assistant =====")
print("Ask questions about your documents.")
print("Type 'exit' to quit.\n")

while True:

    question = input("You: ").strip()

    if question.lower() == "exit":
        print("Goodbye!")
        break

    if not question:
        continue

    try:
        answer = ask_question(question)

        print("\nAI:", answer)
        print("\n" + "-" * 60 + "\n")

    except Exception as error:
        print(f"\nRequest failed: {error}\n")
