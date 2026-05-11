"""
Blog post schemas.
"""
from pydantic import BaseModel
from datetime import datetime


class BlogListItem(BaseModel):
    id: str
    slug: str
    title: str
    excerpt: str | None = None
    cover_image_url: str | None = None
    category: str | None = None
    tags: list[str] | None = None
    author_name: str = "Intellisense Team"
    published_at: datetime | None = None


class BlogPost(BlogListItem):
    content: str
