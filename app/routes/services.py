"""
Services endpoints.
GET /api/services — list all active services
GET /api/services/{slug} — get single service by slug
"""
from fastapi import APIRouter, HTTPException
from app.schemas.service_schema import Service, ServiceListItem
from app.services.supabase_service import fetch_all, fetch_one

router = APIRouter()


@router.get("/services", response_model=list[ServiceListItem])
def list_services():
    data = fetch_all("services", filters={"is_active": True}, order_by="sort_order")
    return data


@router.get("/services/{slug}", response_model=Service)
def get_service(slug: str):
    data = fetch_one("services", "slug", slug)
    if not data:
        raise HTTPException(status_code=404, detail=f"Service '{slug}' not found.")
    return data
