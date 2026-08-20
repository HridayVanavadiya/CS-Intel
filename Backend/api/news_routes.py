import json

from fastapi import APIRouter, HTTPException, Query
from Backend.database import get_connection


router = APIRouter(
    prefix="/api/news",
    tags=["News"]
)


@router.get("/")
def get_news(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    search: str | None = None,
    category: str | None = None,
    min_importance: int | None = Query(None, ge=1, le=10),
    sort: str = "importance"
):

    connection = get_connection()

    try:
        cursor = connection.cursor()

        query = """
            SELECT
                id,
                title,
                url,
                source,
                author,
                published_at,
                score,
                category,
                relevance_score,
                ai_is_cs_related,
                ai_summary,
                importance_score,
                ai_tags,
                why_it_matters
            FROM news
            WHERE ai_is_cs_related = TRUE
        """

        params = []

        # Search
        if search:
            query += """
                AND (
                    title ILIKE %s
                    OR ai_summary ILIKE %s
                    OR ai_tags ILIKE %s
                )
            """

            search_pattern = f"%{search}%"

            params.extend([
                search_pattern,
                search_pattern,
                search_pattern
            ])

        # Category filter
        if category:
            query += """
                AND category = %s
            """

            params.append(category)

        # Importance filter
        if min_importance is not None:
            query += """
                AND importance_score >= %s
            """

            params.append(min_importance)

        # Sorting
        if sort == "recent":
            query += """
                ORDER BY published_at DESC
            """

        elif sort == "score":
            query += """
                ORDER BY score DESC
            """

        else:
            query += """
                ORDER BY importance_score DESC,
                         published_at DESC
            """

        # Pagination
        query += """
            LIMIT %s
            OFFSET %s;
        """

        params.extend([
            limit,
            offset
        ])

        cursor.execute(query, tuple(params))

        rows = cursor.fetchall()

        articles = []

        for row in rows:

            try:
                tags = json.loads(row[12]) if row[12] else []
            except (json.JSONDecodeError, TypeError):
                tags = []

            articles.append({
                "id": row[0],
                "title": row[1],
                "url": row[2],
                "source": row[3],
                "author": row[4],
                "published_at": row[5],
                "score": row[6],
                "category": row[7],
                "relevance_score": row[8],
                "is_cs_related": row[9],
                "summary": row[10],
                "importance_score": row[11],
                "tags": tags,
                "why_it_matters": row[13]
            })

        return {
            "count": len(articles),
            "limit": limit,
            "offset": offset,
            "articles": articles
        }

    finally:
        cursor.close()
        connection.close()