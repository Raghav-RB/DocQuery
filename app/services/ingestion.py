from app.services.document_loader import extract_text_from_pdf
from app.services.chunker import chunk_text
from app.rag.embeddings import embed_text
from app.services.database import get_db_connection


def ingest_pdf(file_path: str, filename: str):
    db_connection = get_db_connection()

    try:
        pages = extract_text_from_pdf(file_path)

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
                            filename,
                            page["page"],
                            chunk_index
                        )
                    )

        db_connection.commit()

    finally:
        db_connection.close()