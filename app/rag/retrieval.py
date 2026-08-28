def retrieve_similar_chunks(cursor, query_embedding, k=3):
    cursor.execute(
        """
        SELECT
            text_content,
            filename,
            page,
            chunk_index,
            embedding <=> %s::vector AS distance
        FROM document_chunks
        ORDER BY distance
        LIMIT %s
        """,
        (query_embedding, k)
    )

    return cursor.fetchall()