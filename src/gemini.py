import os
import sys

from google import genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set")

client = genai.Client(api_key=GEMINI_API_KEY)

def generate_content(contents: str, config: dict = {}, model: str = "gemini-2.5-flash-lite") -> str:
    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=config,
    )
    return response.text

if __name__ == "__main__":
    print(generate_content(sys.argv[1]))