"""
Case Studies endpoints.
GET /api/case-studies
GET /api/case-studies/{slug}
"""
from fastapi import APIRouter, HTTPException
from app.schemas.case_study_schema import CaseStudy, CaseStudyListItem
from app.services.supabase_service import fetch_all, fetch_one
from app.db.supabase_client import get_supabase

router = APIRouter()


@router.get("/case-studies", response_model=list[CaseStudyListItem])
def list_case_studies():
    sb = get_supabase()
    result = (
        sb.table("case_studies")
        .select("id,slug,client_name,industry,challenge,cover_image_url,published_at")
        .eq("status", "published")
        .order("published_at", desc=True)
        .execute()
    )
    return result.data or []


@router.get("/case-studies/{slug}", response_model=CaseStudy)
def get_case_study(slug: str):
    data = fetch_one("case_studies", "slug", slug)
    if not data or data.get("status") != "published":
        raise HTTPException(status_code=404, detail=f"Case study '{slug}' not found.")
    return data
