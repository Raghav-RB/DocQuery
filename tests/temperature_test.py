import os

from dotenv import load_dotenv
from google import genai


load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

prompt = """
Write one short sentence describing a sunset.
"""


for temperature in [0.1, 0.9]:
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config={
            "temperature": temperature
        }
    )

    print(f"\nTemperature: {temperature}")
    print(response.text)