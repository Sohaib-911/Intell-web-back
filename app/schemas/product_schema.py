"""
Product schemas.
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Any


class ProductListItem(BaseModel):
    id: str
    slug: str
    name: str
    tagline: str | None = None
    description: str | None = None
    features: list[str] | None = None
    image_url: str | None = None
    is_featured: bool = False


class Product(ProductListItem):
    demo_url: str | None = None
    created_at: datetime | None = None
