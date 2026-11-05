
from pathlib import Path

from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader
)

DOCUMENTS_DIR = Path("documents")


def load_documents():
    documents = []

    # Load TXT files
    for file_path in DOCUMENTS_DIR.glob("*.txt"):
        loader = TextLoader(
            str(file_path),
            encoding="utf-8"
        )
        documents.extend(loader.load())

    # Load PDF files
    for file_path in DOCUMENTS_DIR.glob("*.pdf"):
        loader = PyPDFLoader(str(file_path))
        documents.extend(loader.load())

    print(f"Total documents/pages loaded: {len(documents)}")

    return documents


if __name__ == "__main__":
    docs = load_documents()

    for doc in docs:
        print("\nSource:", doc.metadata.get("source"))
        print("Page:", doc.metadata.get("page", "N/A"))
        print("Content:", doc.page_content[:200])
