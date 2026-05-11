"""
Blogs endpoints.
GET /api/blogs — list published blog posts
GET /api/blogs/{slug} — get single blog post
"""
from fastapi import APIRouter, HTTPException
from app.schemas.blog_schema import BlogPost, BlogListItem
from app.services.supabase_service import fetch_all, fetch_one
from app.db.supabase_client import get_supabase

router = APIRouter()


@router.get("/blogs", response_model=list[BlogListItem])
def list_blogs():
    sb = get_supabase()
    result = (
        sb.table("blogs")
        .select("id,slug,title,excerpt,cover_image_url,category,tags,author_name,published_at")
        .eq("status", "published")
        .order("published_at", desc=True)
        .execute()
    )
    return result.data or []


@router.get("/blogs/{slug}", response_model=BlogPost)
def get_blog(slug: str):
    data = fetch_one("blogs", "slug", slug)
    if not data or data.get("status") != "published":
        raise HTTPException(status_code=404, detail=f"Blog post '{slug}' not found.")
    return data
