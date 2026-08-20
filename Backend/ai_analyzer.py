import os
import json

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel


load_dotenv()


api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    raise ValueError("OPENROUTER_API_KEY was not found in .env")


client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)


class ArticleAnalysis(BaseModel):
    is_cs_related: bool
    category: str
    summary: str
    importance_score: int
    tags: list[str]
    why_it_matters: str


def analyze_article(title, url):

    prompt = f"""
You are the AI analyst for a Computer Science intelligence platform
called CS Intel.

Analyze this article:

TITLE:
{title}

URL:
{url}

Determine whether this article is genuinely relevant to Computer Science.

Relevant areas include:

- Artificial Intelligence
- Machine Learning
- Generative AI
- Software Engineering
- Programming
- Programming Languages
- Cybersecurity
- Cloud Computing
- Databases
- Computer Networks
- Operating Systems
- Distributed Systems
- Computer Architecture
- Hardware
- Robotics
- Developer Tools
- Open Source
- Computer Science Research

Return ONLY valid JSON.

Do NOT use Markdown.
Do NOT use ```json.
Do NOT add explanations before or after the JSON.

The JSON must have exactly these fields:

{{
    "is_cs_related": true,
    "category": "Artificial Intelligence",
    "summary": "A concise 2-3 sentence summary.",
    "importance_score": 7,
    "tags": ["AI", "Machine Learning", "Software Engineering"],
    "why_it_matters": "Explain why this matters to CS students, developers, researchers, or technology professionals."
}}

Rules:

1. is_cs_related:
   - true if genuinely related to Computer Science
   - false if unrelated

2. category:
   - Choose the most appropriate category.

3. summary:
   - Give a concise 2-3 sentence summary.
   - Do not invent information.

4. importance_score:
   - Integer from 1 to 10.
   - 10 = extremely important for CS professionals.
   - 1 = very low importance.

5. tags:
   - Provide 3-5 relevant technical tags.

6. why_it_matters:
   - Briefly explain why the article matters.

Use only information reasonably supported by the title and URL.
"""


    response = client.chat.completions.create(
        model="openai/gpt-oss-20b:free",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        response_format={
            "type": "json_object"
        },
    )

    text = response.choices[0].message.content

    if not text:
        raise ValueError("OpenRouter returned an empty response.")

    text = text.strip()

    # Remove Markdown code fences if the model adds them
    if text.startswith("```json"):
        text = text[7:]

    elif text.startswith("```"):
        text = text[3:]

    if text.endswith("```"):
        text = text[:-3]

    text = text.strip()

    try:

        data = json.loads(text)

        return ArticleAnalysis.model_validate(data)

    except json.JSONDecodeError as error:

        print("\nWARNING: Model did not return valid JSON.")
        print("Raw model response:")
        print(text)

        raise ValueError(
            f"Invalid JSON returned by OpenRouter: {error}"
        )

    except Exception as error:

        print("\nWARNING: AI response failed validation.")
        print("Raw model response:")
        print(text)

        raise


if __name__ == "__main__":

    result = analyze_article(
        "Rethinking Database Programming",
        "https://acadia.engineering/blog/rethinking-database-programming"
    )

    print("\n===== AI ANALYSIS =====\n")

    print(result.model_dump_json(indent=4))