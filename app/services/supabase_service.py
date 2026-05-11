"""
Supabase service helpers — thin CRUD wrappers.
All database operations go through here.
"""
from typing import Any
from app.db.supabase_client import get_supabase


def fetch_all(table: str, filters: dict | None = None, order_by: str | None = None) -> list[dict]:
    sb = get_supabase()
    query = sb.table(table).select("*")
    if filters:
        for k, v in filters.items():
            query = query.eq(k, v)
    if order_by:
        query = query.order(order_by)
    result = query.execute()
    return result.data or []


def fetch_one(table: str, slug_field: str, slug_value: str) -> dict | None:
    sb = get_supabase()
    result = sb.table(table).select("*").eq(slug_field, slug_value).limit(1).execute()
    if result.data:
        return result.data[0]
    return None


def insert_row(table: str, data: dict) -> dict:
    sb = get_supabase()
    result = sb.table(table).insert(data).execute()
    return result.data[0] if result.data else {}
