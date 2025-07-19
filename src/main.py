import os
import uuid

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from src.api import router as api_router
from src.config import config
from src.logging_config import request_id_ctx_var

load_dotenv(verbose=True)

# Setup rate limiter
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(title="Fortuna Flow API", openapi_url="/api/openapi.json")

# Add rate limiter to app
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Global rate limiting
# @app.middleware("http")
# async def global_rate_limit(request: Request, call_next):
#     # Apply rate limit to all endpoints
#     await limiter.check_request_limit(request, f"{config.max_requests_per_minute}/minute")
#     response = await call_next(request)
#     return response


@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    request_id_ctx_var.set(request_id)
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response


@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    
    if request.url.path in ["/docs", "/redoc", "/openapi.json"]:
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net blob:; "
            "worker-src 'self' blob:; "
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://fonts.googleapis.com; "
            "img-src 'self' https://fastapi.tiangolo.com https://cdn.jsdelivr.net https://cdn.redoc.ly data:; "
            "font-src 'self' https://cdn.jsdelivr.net https://fonts.gstatic.com; "
            "connect-src 'self'"
        )
    else:
        response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self'"
    
    return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=config.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=[
        "Accept",
        "Accept-Language",
        "Content-Language",
        "Content-Type",
        "Authorization",
        "X-Requested-With",
        "X-Request-ID",
    ],
    expose_headers=["X-Request-ID"],
    max_age=86400,  # Cache preflight requests for 24 hours
)

app.include_router(api_router, prefix="/api")
