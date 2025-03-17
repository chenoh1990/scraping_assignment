from pydantic import BaseModel
from typing import List


class Article(BaseModel):
    title: str
    url: str
    content: str
    description: str
    tags: List[str]
    article_content: str
