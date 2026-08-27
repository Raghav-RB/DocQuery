from google import genai
from dotenv import load_dotenv
import os


load_dotenv()


gemini_client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def embed_text(text: str) -> list[float]:
    response = gemini_client.models.embed_content(
        model="gemini-embedding-2",
        contents=text
    )

    return response.embeddings[0].values