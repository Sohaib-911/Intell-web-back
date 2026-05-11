"""
Testimonials endpoint.
GET /api/testimonials — list all active testimonials
"""
from fastapi import APIRouter
from app.schemas.testimonial_schema import Testimonial
from app.services.supabase_service import fetch_all

router = APIRouter()


@router.get("/testimonials", response_model=list[Testimonial])
def list_testimonials():
    data = fetch_all("testimonials", filters={"is_active": True}, order_by="created_at")
    return data
