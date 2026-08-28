from app.rag.embeddings import embed_text
from app.rag.retrieval import retrieve_similar_chunks
from app.rag.context import build_context
from app.rag.prompt import build_rag_prompt
from app.services.llm import generate_answer
from app.services.database import get_db_connection


def answer_question(question: str, k: int = 3) -> dict:
    query_embedding = embed_text(question)

    db_connection = get_db_connection()

    try:
        with db_connection.cursor() as cursor:
            results = retrieve_similar_chunks(
                cursor,
                query_embedding,
                k
            )

        context = build_context(results)

        prompt = build_rag_prompt(
            question,
            context
        )

        answer = generate_answer(prompt)

        sources = [
            {
                "filename": result[1],
                "page": result[2],
                "chunk_index": result[3],
            }
            for result in results
        ]

        return {
            "answer": answer,
            "sources": sources,
        }

    finally:
        db_connection.close()