"""
Industries endpoints.
GET /api/industries — list all industries
GET /api/industries/{slug} — get single industry
"""
from fastapi import APIRouter, HTTPException
from app.schemas.industry_schema import Industry, IndustryListItem
from app.services.supabase_service import fetch_all, fetch_one

router = APIRouter()


@router.get("/industries", response_model=list[IndustryListItem])
def list_industries():
    data = fetch_all("industries")
    return data


@router.get("/industries/{slug}", response_model=Industry)
def get_industry(slug: str):
    data = fetch_one("industries", "slug", slug)
    if not data:
        raise HTTPException(status_code=404, detail=f"Industry '{slug}' not found.")
    return data
