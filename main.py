import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

response = client.interactions.create(
    model="gemini-3.8-flash",
    input="What are the latest major developments in the Indian stock market today?",
    tools=[{"type": "google_search"}]
)

print(response.output_text)