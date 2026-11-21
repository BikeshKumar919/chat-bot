
from backend.config.database import get_db_connection
from backend.services.embedding_service import generate_embeddings

from pgvector.psycopg2 import register_vector


def search_resume_chunks(
    query: str,
    job_id: str,
    limit: int | None = None
):
    # Step 1: Generate embedding for search query
    query_embedding = generate_embeddings([query])[0]

    # Step 2: Connect to PostgreSQL
    connection = get_db_connection()

    try:
        register_vector(connection)

        cursor = connection.cursor()

        # Step 3: Search similar resume chunks
        sql = """
            SELECT
                candidate_id,
                chunk_index,
                chunk_text,
                embedding <=> %s AS distance
            FROM resume_chunks
            WHERE job_id = %s
            ORDER BY embedding <=> %s
            LIMIT %s;
        """

        cursor.execute(
            sql,
            (
                query_embedding,
                job_id,
                query_embedding,
                limit
            )
        )

        results = cursor.fetchall()

        # Step 4: Convert results into dictionaries
        matches = []

        for row in results:
            matches.append({
                "candidate_id": row[0],
                "chunk_index": row[1],
                "chunk_text": row[2],
                "distance": float(row[3])
            })

        return matches

    finally:
        cursor.close()
        connection.close()
