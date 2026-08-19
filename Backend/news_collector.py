import requests
from datetime import datetime, timezone

from models import NewsArticle
from news_repository import save_news_article


# CS_KEYWORDS = [
#     "ai",
#     "artificial intelligence",
#     "machine learning",
#     "deep learning",
#     "llm",
#     "large language model",
#     "generative ai",
#     "gpt",
#     "gemini",
#     "claude",
#     "openai",
#     "anthropic",
#     "deepseek",
#     "computer science",
#     "programming",
#     "software",
#     "developer",
#     "github",
#     "python",
#     "javascript",
#     "typescript",
#     "java",
#     "c++",
#     "rust",
#     "golang",
#     "sql",
#     "cloud",
#     "aws",
#     "azure",
#     "docker",
#     "kubernetes",
#     "cybersecurity",
#     "malware",
#     "hacking",
#     "linux",
#     "operating system",
#     "robotics",
# ]


# def is_cs_related(story):
#     title = story.get("title", "").lower()

#     for keyword in CS_KEYWORDS:
#         if keyword in title:
#             return True

#     return False

# Strong signals: these almost always indicate a CS/technology article.
STRONG_CS_KEYWORDS = [
    "artificial intelligence",
    "machine learning",
    "deep learning",
    "large language model",
    "llm",
    "generative ai",
    "computer science",
    "cybersecurity",
    "malware",
    "ransomware",
    "programming language",
    "compiler",
    "operating system",
    "computer architecture",
    "distributed systems",
    "database",
    "databases",
    "open source",
    "software engineering",
    "developer tools",
    "github",
    "api",
    "gpu",
    "neural network",
    "robotics",
    "cryptography",
    "encryption",
]

# Technology/company names are also strong signals.
TECHNOLOGY_KEYWORDS = [
    "openai",
    "anthropic",
    "deepseek",
    "gemini",
    "claude",
    "gpt",
    "hugging face",
    "tensorflow",
    "pytorch",
    "kubernetes",
    "docker",
    "linux",
    "python",
    "javascript",
    "typescript",
    "rust",
    "golang",
    "java",
    "c++",
    "postgresql",
    "mongodb",
    "aws",
    "azure",
    "google cloud",
]

# Weak signals alone should NOT make an article CS-related.
WEAK_CS_KEYWORDS = [
    "data",
    "cloud",
    "software",
    "system",
    "program",
    "android",
    "app",
]


def calculate_cs_score(story):
    title = story.get("title", "").lower()

    score = 0

    # Strong CS concepts
    for keyword in STRONG_CS_KEYWORDS:
        if keyword in title:
            score += 3

    # Technology names
    for keyword in TECHNOLOGY_KEYWORDS:
        if keyword in title:
            score += 2

    # Weak terms
    for keyword in WEAK_CS_KEYWORDS:
        if keyword in title:
            score += 1

    return score


def is_cs_related(story):
    title = story.get("title", "").lower()

    strong_match = any(
        keyword in title
        for keyword in STRONG_CS_KEYWORDS
    )

    technology_match = any(
        keyword in title
        for keyword in TECHNOLOGY_KEYWORDS
    )

    score = calculate_cs_score(story)

    return strong_match or (technology_match and score >= 2)


def get_top_stories(limit = 100):
    url = "https://hacker-news.firebaseio.com/v0/topstories.json"

    response = requests.get(url)

    if response.status_code != 200:
        print("Failed to fetch stories")
        return []

    story_ids = response.json()

    stories = []

    for story_id in story_ids[:limit]:

        story_url = (
            f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
        )

        story_response = requests.get(story_url)

        if story_response.status_code == 200:

            story = story_response.json()

            if story.get("type") == "story":
                stories.append(story)

    return stories


def convert_to_news_article(story, relevance_score):
    published_time = datetime.fromtimestamp(
        story.get("time", 0),
        tz = timezone.utc
    )

    article = NewsArticle(
        title=story.get("title", "Unknown title"),
        url=story.get("url", "No URL"),
        source="Hacker News",
        author=story.get("by", "Unknown"),
        published_at=published_time,
        score=story.get("score", 0),
        category="Uncategorized",
        relevance_score=relevance_score,
    )

    return article


if __name__ == "__main__":

    stories = get_top_stories(100)

    print("\n===== CS INTEL =====\n")

    cs_stories = []

    for story in stories:

        if is_cs_related(story):
            relevance_score = calculate_cs_score(story)
            article = convert_to_news_article(story,relevance_score)
            cs_stories.append(article)

    for index, article in enumerate(cs_stories, start=1):

        print(f"{index}. {article.title}")
        print(f"   Source: {article.source}")
        print(f"   Author: {article.author}")
        print(f"   Score: {article.score}")
        print(f"   Relevance: {article.relevance_score}")
        print(f"   Published: {article.published_at}")
        print(f"   URL: {article.url}")

        save_news_article(article)

        print("   Saved to database!")
        print()