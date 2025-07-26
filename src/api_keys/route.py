from fastapi import APIRouter, Depends, Request

from src import dependencies
from src.api_keys import service

from src.logging_config import create_logger
from src.dependencies import get_current_user, require_csrf_protection

router = APIRouter()

logger = create_logger("api_keys", __name__)
