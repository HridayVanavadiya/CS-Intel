import os
import json
import time

from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel


load_dotenv()


api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY was not found in .env")


client = genai.Client(api_key=api_key)


class ArticleAnalysis(BaseModel):
    is_cs_related: bool
    category: str
    summary: str
    importance_score: int
    tags: list[str]
    why_it_matters: str


def analyze_article(title, url):

    prompt = f"""
You are the AI analyst for a Computer Science intelligence platform called CS Intel.

Analyze this article:

TITLE:
{title}

URL:
{url}

Determine whether this article is genuinely relevant to Computer Science,
software engineering, AI, cybersecurity, cloud computing, programming,
databases, networking, hardware, or related technology.

Important:
- Do not invent information that is not supported by the title.
- If the title is insufficient to know something, keep the explanation general.
- importance_score must be between 1 and 10.
- Return the requested structured fields.
"""

    max_retries = 3

    for attempt in range(max_retries):

        try:

            response = client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=ArticleAnalysis,
                ),
            )

            break

        except Exception as error:

            if "503" in str(error) or "UNAVAILABLE" in str(error):

                if attempt < max_retries - 1:

                    wait_time = 5 * (2 ** attempt)

                    print(
                        f"Gemini temporarily unavailable. "
                        f"Retrying in {wait_time} seconds..."
                    )

                    time.sleep(wait_time)

                else:
                    raise

            else:
                raise

    if not response.text:
        raise ValueError(
            "Gemini returned an empty response. "
            f"Response object: {response}"
        )

    return ArticleAnalysis.model_validate_json(response.text)


if __name__ == "__main__":

    result = analyze_article(
        "Turbovec - Google's TurboQuant for vector search in Rust",
        "https://github.com/RyanCodrai/turbovec"
    )

    print("\n===== AI ANALYSIS =====\n")

    print(result.model_dump_json(indent=4))