from datetime import datetime, timedelta, timezone
from typing import Dict, Union, Optional

from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext

from src.auth.exceptions import IncorrectEmailOrPassword
from src.auth.schemas import UserLogin
from src.auth.constants import REFRESH_TOKEN_MAX_AGE, REFRESH_TOKEN_COOKIE_KEY
from src.config import config
from src.database import database
import secrets

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/signin")


def verify_password(plain_password, hashed_password) -> str:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.secret_key, algorithm=config.algorithm)
    return encoded_jwt


async def get_user(username_or_email: str) -> UserLogin:
    query = {
        "$or": [
            {"username": username_or_email},
            {"email": username_or_email},
            {"userId": username_or_email},
        ]
    }
    user = await database["users"].find_one(query)
    if user:
        return UserLogin(**user)


async def authenticate_user(
    username_or_email: str, password: str = None, provider: str = None
) -> Union[UserLogin, bool]:
    user = await get_user(username_or_email)
    if not user and provider is None:
        raise IncorrectEmailOrPassword()
    elif not user and provider:
        return False
    if password and not verify_password(password, user.password):
        raise IncorrectEmailOrPassword()

    return user


def extract_user_provider(user) -> Dict[str, str]:
    return {
        "profilePicture": user.picture,
        "name": user.display_name,
        "username": user.email,
        "email": user.email,
        "provider": user.provider,
    }


def create_refresh_token(user_id: str) -> str:
    return secrets.token_urlsafe(64)


async def save_refresh_token(user_id: str, refresh_token: str, device: str, ip: str, browser: str):
    data = {
        "userId": user_id,
        "refreshToken": refresh_token,
        "device": device,
        "ip": ip,
        "browser": browser,
        "createdAt": datetime.now(timezone.utc).isoformat(),
        "lastUsedAt": datetime.now(timezone.utc).isoformat(),
    }
    await database["refresh_tokens"].insert_one(data)


async def get_refresh_token(token: str) -> Optional[dict]:
    return await database["refresh_tokens"].find_one({"refreshToken": token})


async def update_refresh_token_last_used(token: str):
    await database["refresh_tokens"].update_one(
        {"refreshToken": token},
        {"$set": {"lastUsedAt": datetime.now(timezone.utc).isoformat()}}
    )


async def delete_refresh_token(token: str):
    await database["refresh_tokens"].delete_one({"refreshToken": token})


async def save_login_history(user_id: str, device: str, ip: str, browser: str, refresh_token: Optional[str] = None, user_agent_raw: Optional[str] = None):
    data = {
        "userId": user_id,
        "device": device,
        "ip": ip,
        "browser": browser,
        "loginAt": datetime.now(timezone.utc).isoformat(),
        "refreshToken": refresh_token,
        "userAgentRaw": user_agent_raw,
    }
    await database["login_history"].insert_one(data)


async def get_last_login_history(user_id: str) -> Optional[dict]:
    return await database["login_history"].find_one({"userId": user_id}, sort=[("loginAt", -1)])


def extract_request_info(request):
    user_agent = request.headers.get("user-agent", "")
    x_forwarded_for = request.headers.get("x-forwarded-for")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0].strip()
    else:
        ip = request.client.host if request.client else "unknown"
    from user_agents import parse as parse_ua
    ua = parse_ua(user_agent)
    device = f"{ua.device.family or 'Unknown'} {ua.os.family or 'Unknown'} {ua.os.version_string or ''}".strip()
    browser = f"{ua.browser.family or 'Unknown'} {ua.browser.version_string or ''}".strip()
    return device, ip, browser, user_agent


async def set_refresh_cookie_and_history(response, user_id, request, config):
    refresh_token = create_refresh_token(user_id)
    device, ip, browser, user_agent = extract_request_info(request)
    await save_refresh_token(user_id, refresh_token, device, ip, browser)
    await save_login_history(user_id, device, ip, browser, refresh_token, user_agent_raw=user_agent)
    response.set_cookie(
        key=REFRESH_TOKEN_COOKIE_KEY,
        value=refresh_token,
        httponly=True,
        max_age=REFRESH_TOKEN_MAX_AGE,
        path="/",
        samesite="lax",
        secure=not config.is_env_dev
    )
    return refresh_token
