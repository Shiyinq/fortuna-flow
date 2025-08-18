from fastapi import APIRouter, Depends, Request

from src.config import config
from src.api_keys import service

from src.api_keys.exceptions import APIKeyCreateError, APIKeyDeleteError, APIKeyNotFound
from src.api_keys.schemas import APIKeysResponse
from src.logging_config import create_logger
from src.dependencies import get_current_user, require_csrf_protection
from slowapi import Limiter
from slowapi.util import get_remote_address

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

logger = create_logger("api_keys", __name__)


@router.post("/key", status_code=201, response_model=APIKeysResponse)
@limiter.limit(f"{config.max_requests_per_minute}/minute")
async def create_api_key(request: Request, current_user=Depends(get_current_user), _=Depends(require_csrf_protection)):
    """
    Create a new API key for the current user.

    Returns:
        APIKeysResponse: Newly generated API key and detail message.
    """
    logger.info(f"[CREATE_API_KEY] Incoming request: user_id={current_user.userId}")
    try:
        new_api_key = await service.create_api_key(current_user.userId)
        logger.info(
            f"[CREATE_API_KEY] Success: user_id={current_user.userId}"
        )
        return new_api_key
    except Exception as e:
        logger.exception(f"[CREATE_API_KEY] Error: {str(e)}")
        raise APIKeyCreateError()


@router.delete("/key", status_code=200, response_model=APIKeysResponse)
async def delete_api_key(current_user=Depends(get_current_user), _=Depends(require_csrf_protection)):
    """
    Delete the current user's API key.

    Returns:
        APIKeysResponse: Confirmation message after deleting the API key.

    Raises:
        APIKeyNotFound: If the current user does not have an API key.
    """
    logger.info(f"[DELETE_API_KEY] Incoming request: user_id={current_user.userId}")
    try:
        deleted = await service.delete_api_key(current_user.userId)
        logger.info(
            f"[DELETE_API_KEY] Success: user_id={current_user.userId}"
        )
        return deleted
    except APIKeyNotFound:
        raise
    except Exception as e:
        logger.exception(f"[DELETE_API_KEY] Error: {str(e)}")
        raise APIKeyDeleteError()