"""
Customer schemas.
"""
from pydantic import BaseModel


class Customer(BaseModel):
    id: str
    name: str
    logo_url: str | None = None
    website_url: str | None = None
    industry: str | None = None
    is_featured: bool = True
