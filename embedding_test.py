from google import genai
from dotenv import load_dotenv
import os
import psycopg

load_dotenv()


gemini_client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


db_connection = psycopg.connect(
    host=os.getenv("DATABASE_HOST"),
    port=os.getenv("DATABASE_PORT"),
    dbname=os.getenv("DATABASE_NAME"),
    user=os.getenv("DATABASE_USER"),
    password=os.getenv("DATABASE_PASSWORD"),
)

texts = [
    "The car is parked outside.",
    "The automobile is parked outside.",
    "Python is a programming language."
]


with db_connection.cursor() as cursor:
    cursor.execute("TRUNCATE TABLE semantic_test")


with db_connection.cursor() as cursor:

    for text in texts:
        response = gemini_client.models.embed_content(
            model="gemini-embedding-2",
            contents=text
        )

        embedding = response.embeddings[0].values

        cursor.execute(
            """
            INSERT INTO semantic_test (text_content, embedding)
            VALUES (%s, %s)
            """,
            (text, embedding)
        )

db_connection.commit()


question = "Where is the vehicle parked?"

response = gemini_client.models.embed_content(
    model="gemini-embedding-2",
    contents=question
)

question_embedding = response.embeddings[0].values


with db_connection.cursor() as cursor:

    cursor.execute(
        """
        SELECT
            text_content,
            embedding <=> %s::vector AS distance
        FROM semantic_test
        ORDER BY distance
        LIMIT 2
        """,
        (question_embedding,)
    )

    results = cursor.fetchall()


print("\nSearch results:")

for text, distance in results:
    print(f"{distance:.6f} → {text}")

db_connection.close()

print("\nEmbeddings stored and search completed successfully.")