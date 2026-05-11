"""
Industry schemas.
"""
from pydantic import BaseModel
from typing import Any


class IndustryListItem(BaseModel):
    id: str
    slug: str
    title: str
    description: str | None = None


class Industry(IndustryListItem):
    challenges: list[str] | None = None
    solutions: list[str] | None = None
