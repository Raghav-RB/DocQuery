def retrieve_similar_chunks(cursor, query_embedding, k=3):
    cursor.execute(
        """
        SELECT
            text_content,
            embedding <=> %s::vector AS distance
        FROM semantic_test
        ORDER BY distance
        LIMIT %s
        """,
        (query_embedding, k)
    )

    return cursor.fetchall()