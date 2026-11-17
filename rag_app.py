import re
import os
from pathlib import Path

import faiss
import numpy as np
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_community.chat_message_histories import SQLChatMessageHistory

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

with np.load(store_dir / "documents_data.npz", allow_pickle=False) as data:
    chunks = data["chunks"].tolist()
    sources = data["sources"].tolist()
    chunk_numbers = data["chunk_numbers"].tolist()
    pages = data["pages"].tolist()

print(f"Loaded {index.ntotal} vectors from FAISS.")

# --------------------------------------------------
# 4. Load embedding model
# --------------------------------------------------

print("Loading embedding model...")

embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# --------------------------------------------------
# 5. Initialize conversation memory
# --------------------------------------------------

# --------------------------------------------------
# Initialize persistent SQLite conversation memory
# --------------------------------------------------


def get_session_history(session_id: str):

    return SQLChatMessageHistory(
        session_id=session_id, connection="sqlite:///chat_history.db"
    )


# --------------------------------------------------
# 6. Retrieve relevant document chunks
# --------------------------------------------------


def retrieve_documents(question, k=3):

    question_embedding = embedding_model.encode(
        [question], convert_to_numpy=True
    ).astype("float32")

    faiss.normalize_L2(question_embedding)

    k = min(k, index.ntotal)

    scores, indices = index.search(question_embedding, k)

    retrieved_context = []

    for score, idx in zip(scores[0], indices[0]):

        if idx < 0:
            continue

        source = sources[idx]
        page = pages[idx]

        # Build source information
        if page >= 0:
            location = f"PDF Page: {page + 1}"
        else:
            location = "Text File"

        retrieved_context.append(f"""
Source: {source}
{location}
Chunk: {chunk_numbers[idx]}
Similarity: {score:.3f}

Content:
{chunks[idx]}
""")

    return retrieved_context


# --------------------------------------------------
# 7. Rewrite follow-up questions
# --------------------------------------------------

rewrite_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are a question rewriting assistant.

Your ONLY task is to rewrite questions.

IMPORTANT:
- Never answer the user's question.
- Never explain anything.
- Never provide bullet points.
- Return exactly ONE standalone question.
- If the user's question is already standalone,
  return the exact original question unchanged.
- Resolve references such as it, its, they and them
  using conversation history.
- Preserve the original meaning.

Output only the rewritten question.
""",
        ),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}"),
    ]
)

rewrite_chain = rewrite_prompt | llm


# --------------------------------------------------
# 8. Initialize answer generation chain
# --------------------------------------------------


answer_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are a helpful Java backend programming assistant.

Answer questions using the supplied document context.

Instructions:

1. Prefer information from the retrieved documents.
2. Use conversation history to understand follow-up questions.
3. If the documents do not contain enough information,
   clearly say that the answer is not available in the documents.
4. Never invent document contents.
5. When using information from retrieved passages,
   mention the source filename.
6. For PDF sources, mention the PDF page number.
7. Do not invent page numbers or sources.

Retrieved document context:
{context}
""",
        ),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}"),
    ]
)


answer_chain = answer_prompt | llm


def needs_question_rewriting(question):

    follow_up_patterns = [
        r"\bit\b",
        r"\bits\b",
        r"\bthey\b",
        r"\bthem\b",
        r"\btheir\b",
        r"\bthese\b",
        r"\bthose\b",
        r"\bthat\b",
        r"\bthis\b",
        r"\bformer\b",
        r"\blatter\b",
    ]

    return any(re.search(pattern, question.lower()) for pattern in follow_up_patterns)





# --------------------------------------------------
# 9. Ask question with conversation memory
# --------------------------------------------------



def ask_question(question, session_id):

    # Step 1: Get memory for this session
    chat_history = get_session_history(session_id)
    history = chat_history.messages

    # Step 2: Rewrite only follow-up questions
    if history and needs_question_rewriting(question):

        rewritten_response = rewrite_chain.invoke({
            "history": history,
            "question": question
        })

        standalone_question = rewritten_response.content.strip()

        # Validate the rewrite
        if not standalone_question.endswith("?"):
            print("Invalid rewrite detected. Using original question.")
            standalone_question = question

        print("\nRewritten question:", standalone_question)

    else:
        standalone_question = question
        print("\nStandalone question:", standalone_question)

    # Step 3: Retrieve relevant documents
    context = retrieve_documents(standalone_question)

    # Step 4: Generate answer
    response = answer_chain.invoke({
        "question": question,
        "context": "\n".join(context),
        "history": history
    })

    # Step 5: Save conversation
    chat_history.add_user_message(question)
    chat_history.add_ai_message(response.content)

    return response.content


# --------------------------------------------------
# 10. Interactive chatbot
# --------------------------------------------------

print("\n===== Java Backend RAG Assistant =====")
print("Ask questions about your documents.")
print("Type 'exit' to quit.\n")

while True:

    try:
        question = input("You: ").strip()

    except KeyboardInterrupt:
        print("\n\nChatbot stopped.")
        break

    if question.lower() == "exit":
        print("Goodbye!")
        break

    if not question:
        continue

    try:
        session_id = input("Session ID (user-A/user-B): ").strip()

        answer = ask_question(question, session_id)

        print("\nAI:", answer)
        print("\n" + "-" * 60 + "\n")

    except Exception as error:
        print(f"\nRequest failed: {error}\n")


