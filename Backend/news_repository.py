from database import get_connection
from models import NewsArticle


def save_news_article(article: NewsArticle):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        query = """
            INSERT INTO news (
                title,
                url,
                source,
                author,
                published_at,
                score,
                category,
                relevance_score
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (url) DO NOTHING;
        """

        cursor.execute(
            query,
            (
                article.title,
                article.url,
                article.source,
                article.author,
                article.published_at,
                article.score,
                article.category,
                article.relevance_score,
            ),
        )

        connection.commit()

    finally:
        cursor.close()
        connection.close()