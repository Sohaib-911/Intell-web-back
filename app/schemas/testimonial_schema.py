"""
Testimonial schemas.
"""
from pydantic import BaseModel
from datetime import datetime


class Testimonial(BaseModel):
    id: str
    client_name: str
    client_role: str | None = None
    company_name: str | None = None
    quote: str
    rating: int | None = None
    image_url: str | None = None
    is_active: bool = True
