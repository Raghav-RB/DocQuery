import os

import psycopg
from dotenv import load_dotenv

from app.services.document_loader import extract_text_from_pdf
from app.services.chunker import chunk_text
from app.rag.embeddings import embed_text


load_dotenv()


db_connection = psycopg.connect(
    host=os.getenv("DATABASE_HOST"),
    port=os.getenv("DATABASE_PORT"),
    dbname=os.getenv("DATABASE_NAME"),
    user=os.getenv("DATABASE_USER"),
    password=os.getenv("DATABASE_PASSWORD"),
)


pages = extract_text_from_pdf("sample.pdf")


with db_connection.cursor() as cursor:

    for page in pages:

        chunks = chunk_text(
            page["text"],
            chunk_size=1000,
            overlap_sentences=1
        )

        for chunk_index, chunk in enumerate(chunks):

            embedding = embed_text(chunk)

            cursor.execute(
                """
                INSERT INTO document_chunks
                    (text_content, embedding, filename, page, chunk_index)
                VALUES
                    (%s, %s, %s, %s, %s)
                """,
                (
                    chunk,
                    embedding,
                    "sample.pdf",
                    page["page"],
                    chunk_index
                )
            )


db_connection.commit()
db_connection.close()


print("Document ingestion completed successfully.")