import os

from dotenv import load_dotenv
from google import genai
from google.genai import errors


load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_answer(prompt: str) -> str:
    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
        )

        return response.text

    except errors.APIError as error:
        raise RuntimeError("Gemini API request failed") from error