
from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_resume_text(
    resume_text: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 150
) -> list:

    if not resume_text or not resume_text.strip():
        return []

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""]
    )

    chunks = splitter.split_text(resume_text)

    result = []

    for index, chunk in enumerate(chunks):
        result.append({
            "chunk_index": index,
            "chunk_text": chunk
        })

    return result
