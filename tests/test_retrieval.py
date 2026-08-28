import os

import psycopg
from dotenv import load_dotenv

from app.rag.embeddings import embed_text
from app.rag.retrieval import retrieve_similar_chunks


load_dotenv()

print("1. Starting database connection...")

db_connection = psycopg.connect(
    host=os.getenv("DATABASE_HOST"),
    port=os.getenv("DATABASE_PORT"),
    dbname=os.getenv("DATABASE_NAME"),
    user=os.getenv("DATABASE_USER"),
    password=os.getenv("DATABASE_PASSWORD"),
)

print("2. Database connected.")

question = "What is a feasibility survey?"

print("3. Creating question embedding...")

query_embedding = embed_text(question)

print("4. Question embedding created.")
print("Embedding dimensions:", len(query_embedding))

with db_connection.cursor() as cursor:

    print("5. Starting retrieval...")

    results = retrieve_similar_chunks(
        cursor,
        query_embedding,
        k=3
    )

    print("6. Retrieval completed.")


for result in results:
    print(result)


db_connection.close()

print("7. Done.")