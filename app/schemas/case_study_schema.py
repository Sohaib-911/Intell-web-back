"""
Case Study schemas.
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Any


class CaseStudyListItem(BaseModel):
    id: str
    slug: str
    client_name: str
    industry: str | None = None
    challenge: str | None = None
    cover_image_url: str | None = None
    published_at: datetime | None = None


class CaseStudy(CaseStudyListItem):
    solution: str | None = None
    results: dict[str, Any] | None = None
    testimonial_id: str | None = None
    status: str = "draft"
