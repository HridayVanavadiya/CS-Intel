from dataclasses import dataclass
from datetime import datetime


@dataclass
class NewsArticle:
    title: str
    url: str
    source: str
    author: str
    published_at: datetime
    score: int
    category: str
    relevance_score: int