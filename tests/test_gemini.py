import os

from dotenv import load_dotenv
from google import genai


load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents="""
Answer the question using only the context below.

Context:
DocQuery is an AI document question-answering system.
It retrieves relevant information from uploaded documents
and gives that information to an LLM to generate a grounded answer.

Question:
What does DocQuery do?
"""
)

print(response.text)