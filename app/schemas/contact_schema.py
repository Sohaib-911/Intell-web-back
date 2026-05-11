"""
Contact form request and response schemas.
"""
from pydantic import BaseModel, EmailStr, field_validator
import re


class ContactRequest(BaseModel):
    name: str
    company: str | None = None
    email: EmailStr
    phone: str | None = None
    service_interest: str | None = None
    message: str

    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Name cannot be empty.")
        if len(v) < 2:
            raise ValueError("Name must be at least 2 characters.")
        if len(v) > 100:
            raise ValueError("Name must be under 100 characters.")
        return v

    @field_validator("message")
    @classmethod
    def message_must_not_be_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Message cannot be empty.")
        if len(v) < 10:
            raise ValueError("Message must be at least 10 characters.")
        if len(v) > 5000:
            raise ValueError("Message must be under 5000 characters.")
        return v

    @field_validator("phone")
    @classmethod
    def phone_format(cls, v: str | None) -> str | None:
        if v is None:
            return v
        v = v.strip()
        if v and not re.match(r"^\+?[\d\s\-()]{7,20}$", v):
            raise ValueError("Please enter a valid phone number.")
        return v


class ContactResponse(BaseModel):
    success: bool
    message: str
