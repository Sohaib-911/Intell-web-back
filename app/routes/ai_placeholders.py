"""
Future AI feature placeholder endpoints.
These are stubbed out for future implementation.
"""
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class DemoRequest(BaseModel):
    input: str


@router.post("/emaili-demo")
async def emaili_demo(body: DemoRequest):
    """Placeholder: Emaili AI demo endpoint."""
    return {
        "status": "coming_soon",
        "message": "The Emaili AI demo is coming soon. Contact us to request early access.",
    }


@router.post("/content-generator")
async def content_generator(body: DemoRequest):
    """Placeholder: AI content generator demo."""
    return {
        "status": "coming_soon",
        "message": "AI content generation is coming soon via AutoBiz.",
    }


@router.post("/chatbot-demo")
async def chatbot_demo(body: DemoRequest):
    """Placeholder: AI chatbot demo endpoint."""
    return {
        "status": "coming_soon",
        "message": "The Intellisense AI chatbot is coming soon.",
    }


@router.post("/fleet-health-summary")
async def fleet_health_summary(body: DemoRequest):
    """Placeholder: Fleet health AI summary endpoint."""
    return {
        "status": "coming_soon",
        "message": "Fleet health AI summaries are coming soon via the Fleet Maintenance App.",
    }
