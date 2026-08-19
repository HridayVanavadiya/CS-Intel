import json

from database import get_connection
from ai_analyzer import analyze_article


def get_unanalyzed_articles(limit=5):

    connection = get_connection()

    try:
        cursor = connection.cursor()

        query = """
            SELECT
                id,
                title,
                url
            FROM news
            WHERE ai_summary IS NULL
                OR ai_is_cs_related IS NULL
            ORDER BY relevance_score DESC, created_at DESC
            LIMIT %s;
        """

        cursor.execute(query, (limit,))

        return cursor.fetchall()

    finally:
        cursor.close()
        connection.close()


def update_article_analysis(article_id, analysis):

    connection = get_connection()

    try:
        cursor = connection.cursor()

        query = """
            UPDATE news
            SET
                category = %s,
                ai_summary = %s,
                importance_score = %s,
                ai_tags = %s,
                why_it_matters = %s,
                ai_is_cs_related = %s
            WHERE id = %s;
        """

        cursor.execute(
            query,
            (
                analysis.category,
                analysis.summary,
                analysis.importance_score,
                json.dumps(analysis.tags),
                analysis.why_it_matters,
                analysis.is_cs_related,
                article_id,
            ),
        )

        connection.commit()

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":

    articles = get_unanalyzed_articles(limit=5)

    print(f"\nFound {len(articles)} articles to analyze.\n")

    for article in articles:

        article_id, title, url = article

        print("=" * 60)
        print(f"Analyzing: {title}")

        try:

            analysis = analyze_article(title, url)

            print(f"Category: {analysis.category}")
            print(f"Importance: {analysis.importance_score}/10")
            print(f"Tags: {analysis.tags}")

            update_article_analysis(
                article_id,
                analysis
            )

            print("Saved AI analysis to database!")

        except Exception as error:

            print(f"ERROR: {error}")