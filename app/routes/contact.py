"""
Contact form endpoint.
POST /api/contact — validates, rate-limits, stores in Supabase, sends email.
"""
import logging
from fastapi import APIRouter, Request, HTTPException

from app.schemas.contact_schema import ContactRequest, ContactResponse
from app.services.supabase_service import insert_row, fetch_all
from app.services.email_service import send_contact_notification
from app.utils.rate_limit import limiter

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/contact", response_model=ContactResponse)
@limiter.limit("5/minute")
async def submit_contact(request: Request, body: ContactRequest):
    """
    Contact form submission endpoint.
    Rate-limited to 5 requests per minute per IP.
    """
    try:
        previous_submissions = fetch_all(
            "contact_submissions",
            filters={"email": body.email},
        )

        has_messaged_before = len(previous_submissions) > 0
        previous_message_count = len(previous_submissions)

        row = {
            "name": body.name,
            "company": body.company,
            "email": body.email,
            "phone": body.phone,
            "service_interest": body.service_interest,
            "message": body.message,
            "source": "website",
            "status": "new",
        }

        insert_row("contact_submissions", row)
        logger.debug(f"Contact submission saved for {body.email}")

    except Exception as e:
        logger.exception("Failed to save contact submission")
        raise HTTPException(
            status_code=500,
            detail="Failed to save your submission. Please try again.",
        )

    email_sent = await send_contact_notification(
        name=body.name,
        email=body.email,
        company=body.company,
        phone=body.phone,
        service_interest=body.service_interest,
        message=body.message,
        has_messaged_before=has_messaged_before,
        previous_message_count=previous_message_count,
    )

    if not email_sent:
        logger.warning(f"Email notification failed for submission from {body.email}")

    return ContactResponse(
        success=True,
        message="Thank you. Our team will contact you soon.",
    )