"""
Customers endpoint.
GET /api/customers — list featured customers
"""
from fastapi import APIRouter
from app.schemas.customer_schema import Customer
from app.services.supabase_service import fetch_all

router = APIRouter()


@router.get("/customers", response_model=list[Customer])
def list_customers():
    data = fetch_all("customers", filters={"is_featured": True}, order_by="name")
    return data
