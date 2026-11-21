
from backend.config.database import get_db_connection
from pgvector.psycopg2 import register_vector


def save_resume_chunks(chunks: list):
    connection = get_db_connection()

    try:
        register_vector(connection)

        cursor = connection.cursor()

        query = """
            INSERT INTO resume_chunks (
                job_id,
                candidate_id,
                chunk_index,
                chunk_text,
                embedding
            )
            VALUES (%s, %s, %s, %s, %s)
        """

        for chunk in chunks:
            cursor.execute(
                query,
                (
                    chunk["job_id"],
                    chunk["candidate_id"],
                    chunk["chunk_index"],
                    chunk["chunk_text"],
                    chunk["embedding"]
                )
            )

        connection.commit()

        return len(chunks)

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()
