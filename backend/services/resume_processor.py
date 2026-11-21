
from backend.services.resume_chunker import chunk_resume_text
from backend.services.embedding_service import generate_embeddings


def process_resume(
    resume_text: str,
    job_id: str,
    candidate_id: str
):
    chunks = chunk_resume_text(resume_text)

    texts = [chunk["chunk_text"] for chunk in chunks]

    embeddings = generate_embeddings(texts)

    processed_chunks = []

    for chunk, embedding in zip(chunks, embeddings):
        processed_chunks.append({
            "job_id": job_id,
            "candidate_id": candidate_id,
            "chunk_index": chunk["chunk_index"],
            "chunk_text": chunk["chunk_text"],
            "embedding": embedding.tolist()
        })

    return processed_chunks
