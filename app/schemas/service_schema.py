"""
Service schemas.
"""
from pydantic import BaseModel
from datetime import datetime


class ServiceListItem(BaseModel):
    id: str
    slug: str
    title: str
    short_description: str
    icon: str | None = None
    sort_order: int = 0


class Service(ServiceListItem):
    full_description: str | None = None
    is_active: bool = True
    created_at: datetime | None = None
