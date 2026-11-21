
import psycopg2


def get_db_connection():
    connection = psycopg2.connect(
        host="localhost",
        port=5433,
        database="resume_screening",
        user="resume_user",
        password="resume_pass123"
    )

    return connection
