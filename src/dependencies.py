from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from src.api_keys.service import validate_api_key
from src.auth.exceptions import InvalidJWTToken
from src.auth.schemas import TokenData, UserCurrent
from src.auth.service import get_user
from src.auth.csrf_service import CSRFService
from src.config import config
from src.logging_config import create_logger

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/signin")
logger = create_logger("dependencies", __name__)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        if token.startswith(config.api_key_prefix):
            user = await validate_api_key(token)
            logger.info(f"[GET_CURRENT_USER] From API Key Success: user={user['userId']}")
            return UserCurrent(**user)

        payload = jwt.decode(token, config.secret_key, algorithms=[config.algorithm])
        username: str = payload.get("sub")
        if username is None:
            logger.warning("[GET_CURRENT_USER] Token does not contain sub/username")
            raise InvalidJWTToken()
        token_data = TokenData(username=username)
    except JWTError as e:
        logger.exception(f"[GET_CURRENT_USER] JWTError: {str(e)}")
        raise InvalidJWTToken()
    user = await get_user(username_or_email=token_data.username)
    if user is None:
        logger.warning(f"[GET_CURRENT_USER] User not found: {token_data.username}")
        raise InvalidJWTToken()
    logger.info(f"[GET_CURRENT_USER] Success: user={token_data.username}")
    return UserCurrent(**user.dict())


def require_csrf_protection(request: Request):
    if request.method == "OPTIONS":
        return True

    if request.headers.get("authorization").startswith(f"Bearer {config.api_key_prefix}"):
        return True

    if config.is_env_dev:
        referer = request.headers.get("referer", "")
        sec_fetch_site = request.headers.get("sec-fetch-site", "")
        if (
            (referer.startswith("http://localhost:8000/docs") or referer.startswith("http://localhost:8000/redoc"))
            and sec_fetch_site == "same-origin"
        ):
            return True

        user_agent = request.headers.get("user-agent", "").lower()
        if "postman" in user_agent:
            return True

    CSRFService.require_csrf_token(request)
    return True
