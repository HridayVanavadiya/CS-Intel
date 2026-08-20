import os
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    raise ValueError("OPENROUTER_API_KEY was not found in .env")


client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)


response = client.chat.completions.create(
    model="google/gemma-4-31b-it:free",
    messages=[
        {
            "role": "user",
            "content": """
You are testing the AI system for CS Intel.

Analyze this article:

Title:
Rethinking Database Programming

Answer in one short paragraph explaining
whether this is relevant to Computer Science.
"""
        }
    ],
)


print("\n===== OPENROUTER TEST =====\n")

print(response.choices[0].message.content)