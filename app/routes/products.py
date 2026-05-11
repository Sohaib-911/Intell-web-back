"""
Products endpoints.
GET /api/products — list all products
GET /api/products/{slug} — get single product by slug
"""
from fastapi import APIRouter, HTTPException
from app.schemas.product_schema import Product, ProductListItem
from app.services.supabase_service import fetch_all, fetch_one

router = APIRouter()


@router.get("/products", response_model=list[ProductListItem])
def list_products():
    data = fetch_all("products")
    return data


@router.get("/products/{slug}", response_model=Product)
def get_product(slug: str):
    data = fetch_one("products", "slug", slug)
    if not data:
        raise HTTPException(status_code=404, detail=f"Product '{slug}' not found.")
    return data
