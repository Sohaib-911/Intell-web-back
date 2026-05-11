"""
Email notification service.
Supports both SMTP (via aiosmtplib) and Resend API.
Configure EMAIL_PROVIDER in .env to switch between them.
"""
import html
import logging

from app.config import settings

logger = logging.getLogger(__name__)


async def send_contact_notification(
    name: str,
    email: str,
    company: str | None,
    phone: str | None,
    service_interest: str | None,
    message: str,
    has_messaged_before: bool = False,
    previous_message_count: int = 0,
) -> bool:
    """Send contact form notification email to the Intellisense team."""
    subject_prefix = "Returning Lead" if has_messaged_before else "New Lead"
    subject = f"{subject_prefix} - Contact Form Submission from {name}"

    html_body = _build_email_html(
        name=name,
        email=email,
        company=company,
        phone=phone,
        service_interest=service_interest,
        message=message,
        has_messaged_before=has_messaged_before,
        previous_message_count=previous_message_count,
    )

    plain_body = _build_email_plain(
        name=name,
        email=email,
        company=company,
        phone=phone,
        service_interest=service_interest,
        message=message,
        has_messaged_before=has_messaged_before,
        previous_message_count=previous_message_count,
    )

    try:
        if settings.EMAIL_PROVIDER == "resend":
            return await _send_via_resend(subject, html_body)
        return await _send_via_smtp(subject, html_body, plain_body)
    except Exception:
        logger.exception("Failed to send contact notification email")
        return False


async def _send_via_smtp(subject: str, html_body: str, plain_body: str) -> bool:
    import aiosmtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"{settings.SMTP_FROM_NAME} <{settings.SMTP_FROM_EMAIL}>"
    msg["To"] = settings.CONTACT_RECEIVER_EMAIL
    msg["Reply-To"] = settings.SMTP_FROM_EMAIL

    msg.attach(MIMEText(plain_body, "plain", "utf-8"))
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    await aiosmtplib.send(
        msg,
        hostname=settings.SMTP_HOST,
        port=settings.SMTP_PORT,
        username=settings.SMTP_USERNAME,
        password=settings.SMTP_PASSWORD,
        start_tls=True,
    )

    logger.debug(f"Contact email sent via SMTP to {settings.CONTACT_RECEIVER_EMAIL}")
    return True


async def _send_via_resend(subject: str, html_body: str) -> bool:
    import resend

    resend.api_key = settings.RESEND_API_KEY

    params = resend.Emails.SendParams(
        from_=f"{settings.SMTP_FROM_NAME} <onboarding@resend.dev>",
        to=[settings.CONTACT_RECEIVER_EMAIL],
        subject=subject,
        html=html_body,
    )

    resend.Emails.send(params)

    logger.debug(f"Contact email sent via Resend to {settings.CONTACT_RECEIVER_EMAIL}")
    return True


def _build_email_html(
    name: str,
    email: str,
    company: str | None,
    phone: str | None,
    service_interest: str | None,
    message: str,
    has_messaged_before: bool = False,
    previous_message_count: int = 0,
) -> str:
    safe_name = html.escape(name)
    safe_email = html.escape(email)
    safe_company = html.escape(company or "Not provided")
    safe_phone = html.escape(phone or "Not provided")
    safe_service_interest = html.escape(service_interest or "Not selected")
    safe_message = html.escape(message).replace("\n", "<br />")

    lead_note = (
        f"Returning lead Previous submissions: {previous_message_count}"
        if has_messaged_before
        else "New lead"
    )

    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Intellisense Contact Lead</title>
</head>

<body style="margin:0; padding:32px 16px; background:linear-gradient(135deg, #F3F6FF 0%, #EEF3FF 55%, #F7F3FF 100%); font-family:Arial, Helvetica, sans-serif; color:#151B4A;">

  <table width="100%" cellpadding="0" cellspacing="0" role="presentation" style="border-collapse:collapse;">
    <tr>
      <td align="center">

        <table width="100%" cellpadding="0" cellspacing="0" role="presentation" style="max-width:680px; background:rgba(255, 255, 255, 0.50); border-radius:25px; overflow:hidden; box-shadow:0 20px 60px rgba(61, 78, 170, 0.14); border-collapse:separate;">

          <tr>
            <td style="padding:24px 28px 0px 28px;">
              <div style="color:#283593; font-size:20px; font-weight:600;">
                Intellisense
              </div>

              <h1 style="margin:5px 0 0; font-size:16px; color:#000000; font-weight:500;">
                New Contact Submission
              </h1>
            </td>
          </tr>

          <tr>
            <td style="padding:28px;">

              <div style="margin-bottom:22px; padding:15px 16px; border-radius:12px; background:#E8EAF6; color:#000000; font-size:12px; line-height:1.6;">
                {lead_note}
              </div>

              <h2 style="margin:0 0 14px; font-size:14px; color:#000000;">
                Lead Details
              </h2>

              <table width="100%" cellpadding="0" cellspacing="0" role="presentation" style="border-collapse:separate; border-spacing:0 10px;">
                {_email_row("Full Name", safe_name)}
                {_email_row("Email", f'<a href="mailto:{safe_email}" style="color:#0031E0; text-decoration:none; font-weight:500;">{safe_email}</a>')}
                {_email_row("Company", safe_company)}
                {_email_row("Contact Number", safe_phone)}
                {_email_row("Service", safe_service_interest)}
              </table>

              <h2 style="margin:26px 0 14px; font-size:14px; color:#000000;">
                Message
              </h2>

              <div style="margin-top:12px; padding:18px; border-radius:16px; background:rgba(255, 255, 255, 0.65); color:#303A69; font-size:12px; line-height:1.7;">
                {safe_message}
              </div>

            </td>
          </tr>

        </table>

      </td>
    </tr>
  </table>

</body>
</html>
"""


def _email_row(label: str, value: str) -> str:
    return f"""
    <tr>
      <td style="width:120px; padding:10px 14px; color:#000000; font-size:10px; font-weight:600; vertical-align:middle; background:rgba(255, 255, 255, 0.60); border-top-left-radius:12px; border-bottom-left-radius:12px;">
        {label}
      </td>
      <td style="padding:10px; color:#000000; font-size:12px; line-height:1.5; vertical-align:middle; background:rgba(255, 255, 255, 0.60); border-top-right-radius:12px; border-bottom-right-radius:12px;">
        {value}
      </td>
    </tr>
    """


def _build_email_plain(
    name: str,
    email: str,
    company: str | None,
    phone: str | None,
    service_interest: str | None,
    message: str,
    has_messaged_before: bool = False,
    previous_message_count: int = 0,
) -> str:
    lead_status = "Returning Lead" if has_messaged_before else "New Lead"

    return f"""
New Contact Form Submission — Intellisense

Lead Status: {lead_status}
Previous Submissions: {previous_message_count}

Lead Full Name: {name}
Email: {email}
Company: {company or 'Not provided'}
Contact Number: {phone or 'Not provided'}
Services Interested: {service_interest or 'Not selected'}

Message:
{message}

---
Intellisense Website Notification
"""