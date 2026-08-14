import requests


def get_top_stories(limit=10):
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
            stories.append(story)

    return stories


if __name__ == "__main__":
    stories = get_top_stories(10)

    print("\n===== CS INTEL =====\n")

    for index, story in enumerate(stories, start=1):
        print(f"{index}. {story.get('title')}")
        print(f"   URL: {story.get('url', 'No URL')}")
        print()