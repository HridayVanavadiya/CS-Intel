import requests
from datetime import datetime

from models import NewsArticle


CS_KEYWORDS = [
    "ai",
    "artificial intelligence",
    "machine learning",
    "deep learning",
    "llm",
    "large language model",
    "generative ai",
    "gpt",
    "gemini",
    "claude",
    "openai",
    "anthropic",
    "deepseek",
    "computer science",
    "programming",
    "software",
    "developer",
    "github",
    "python",
    "javascript",
    "typescript",
    "java",
    "c++",
    "rust",
    "golang",
    "sql",
    "cloud",
    "aws",
    "azure",
    "docker",
    "kubernetes",
    "cybersecurity",
    "malware",
    "hacking",
    "linux",
    "operating system",
    "robotics",
]


def is_cs_related(story):
    title = story.get("title", "").lower()

    for keyword in CS_KEYWORDS:
        if keyword in title:
            return True

    return False


def get_top_stories(limit=30):
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


def convert_to_news_article(story):
    published_time = datetime.fromtimestamp(story.get("time", 0))

    article = NewsArticle(
        title=story.get("title", "Unknown title"),
        url=story.get("url", "No URL"),
        source="Hacker News",
        author=story.get("by", "Unknown"),
        published_at=published_time,
        score=story.get("score", 0),
        category="Uncategorized",
    )

    return article


if __name__ == "__main__":

    stories = get_top_stories(30)

    print("\n===== CS INTEL =====\n")

    cs_stories = []

    for story in stories:

        if is_cs_related(story):
            article = convert_to_news_article(story)
            cs_stories.append(article)

    for index, article in enumerate(cs_stories, start=1):

        print(f"{index}. {article.title}")
        print(f"   Source: {article.source}")
        print(f"   Author: {article.author}")
        print(f"   Score: {article.score}")
        print(f"   Published: {article.published_at}")
        print(f"   URL: {article.url}")
        print()