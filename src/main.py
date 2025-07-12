import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from src.api import router as api_router
from src.config import config

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

origins = os.getenv("ORIGINS").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")
