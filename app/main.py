"""
Intellisense FastAPI Backend
Application entry point with CORS, routing, and middleware.
"""
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.config import settings
from app.utils.rate_limit import limiter
from app.routes import contact, services, products, industries, blogs, testimonials, customers, case_studies, ai_placeholders

# ── Logging configuration ─────────────────────────────────────────────────────
# Suppress noisy INFO/DEBUG output from the console.
# Only WARNING and above will be printed (errors, warnings).
# Uvicorn access logs are kept at WARNING level so routine request logs are silent.
logging.basicConfig(
    level=logging.WARNING,
    format="%(levelname)s | %(name)s | %(message)s",
)
# Silence third-party libraries that are chatty at INFO level
logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
logging.getLogger("uvicorn.error").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("supabase").setLevel(logging.WARNING)
# ─────────────────────────────────────────────────────────────────────────────

app = FastAPI(
    title="Intellisense API",
    description="Backend API for Intellisense company website",
    version="1.0.0",
    docs_url="/docs" if settings.ENVIRONMENT == "development" else None,
    redoc_url="/redoc" if settings.ENVIRONMENT == "development" else None,
)

# Rate limiter state
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS configuration
allowed_origins = [settings.FRONTEND_URL]
if settings.ENVIRONMENT == "development":
    allowed_origins += []

# CORS configuration for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://intellisense.cloud/",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Register routers
app.include_router(contact.router, prefix="/api", tags=["Contact"])
app.include_router(services.router, prefix="/api", tags=["Services"])
app.include_router(products.router, prefix="/api", tags=["Products"])
app.include_router(industries.router, prefix="/api", tags=["Industries"])
app.include_router(blogs.router, prefix="/api", tags=["Blogs"])
app.include_router(testimonials.router, prefix="/api", tags=["Testimonials"])
app.include_router(customers.router, prefix="/api", tags=["Customers"])
app.include_router(case_studies.router, prefix="/api", tags=["Case Studies"])
app.include_router(ai_placeholders.router, prefix="/api/ai", tags=["AI (Future)"])


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok", "service": "intellisense-api", "version": "1.0.0"}


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": "An unexpected error occurred. Please try again later."},
    )
