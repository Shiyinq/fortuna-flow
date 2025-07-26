import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from typing import Dict, Optional, Union

from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext

from src.auth import repository
from src.auth.constants import REFRESH_TOKEN_COOKIE_KEY, REFRESH_TOKEN_MAX_AGE
from src.auth.email_service import EmailService
from src.auth.exceptions import IncorrectEmailOrPassword
from src.auth.schemas import UserLogin
from src.auth.security_service import SecurityService
from src.auth.csrf_service import CSRFService
from src.config import config
from src.database import database
from src.users.exceptions import AccountLocked, EmailNotVerified
from src.utils import hash_token

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
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=config.access_token_expire_minutes
        )
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
    user = await repository.find_user(query)
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

    # Check account lock status
    lock_status = await SecurityService.check_account_lock_status(user.userId)
    if lock_status["is_locked"]:
        raise AccountLocked()

    # Check email verification for non-provider login
    if provider is None and not user.isEmailVerified:
        raise EmailNotVerified()

    if password and not verify_password(password, user.password):
        # Handle failed login
        await SecurityService.handle_failed_login(
            user.userId, user.email, user.username
        )
        raise IncorrectEmailOrPassword()

    # Reset failed attempts if login successful
    await SecurityService.reset_failed_login_attempts(user.userId)
    return user


def extract_user_provider(user) -> Dict[str, str]:
    return {
        "profilePicture": user.picture,
        "name": user.display_name,
        "username": user.email,
        "email": user.email,
        "provider": user.provider,
    }


def create_refresh_token() -> str:
    return secrets.token_urlsafe(64)


async def save_refresh_token(
    user_id: str, refresh_token: str, device: str, ip: str, browser: str
):
    data = {
        "userId": user_id,
        "hashRefreshToken": refresh_token,
        "device": device,
        "ip": ip,
        "browser": browser,
        "createdAt": datetime.now(timezone.utc).isoformat(),
        "lastUsedAt": datetime.now(timezone.utc).isoformat(),
    }
    await repository.insert_refresh_token(data)


async def get_refresh_token(token: str) -> Optional[dict]:
    return await repository.find_refresh_token(token)


async def update_refresh_token_last_used(token: str):
    await repository.update_refresh_token_last_used(token)


async def delete_refresh_token(token: str):
    await repository.delete_refresh_token(token)


async def save_login_history(
    user_id: str,
    device: str,
    ip: str,
    browser: str,
    user_agent_raw: Optional[str] = None,
):
    data = {
        "userId": user_id,
        "device": device,
        "ip": ip,
        "browser": browser,
        "loginAt": datetime.now(timezone.utc).isoformat(),
        "userAgentRaw": user_agent_raw,
    }
    await repository.insert_login_history(data)


async def get_last_login_history(user_id: str) -> Optional[dict]:
    return await repository.find_last_login_history(user_id)


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
    browser = (
        f"{ua.browser.family or 'Unknown'} {ua.browser.version_string or ''}".strip()
    )
    return device, ip, browser, user_agent


async def set_refresh_cookie_and_history(response, user_id, request, config):
    refresh_token = create_refresh_token()
    hash_refresh_token = hash_token(refresh_token)
    device, ip, browser, user_agent = extract_request_info(request)
    await save_refresh_token(user_id, hash_refresh_token, device, ip, browser)
    await save_login_history(
        user_id, device, ip, browser, user_agent_raw=user_agent
    )
    response.set_cookie(
        key=REFRESH_TOKEN_COOKIE_KEY,
        value=refresh_token,
        httponly=True,
        max_age=REFRESH_TOKEN_MAX_AGE,
        path="/",
        samesite="lax",
        secure=not config.is_env_dev,
    )
    
    CSRFService.set_csrf_cookie(response, config.is_env_dev)

    return refresh_token


# Email verification functions
async def send_email_verification(user_id: str, email: str, username: str):
    """Send email verification"""
    token = SecurityService.create_token()
    token_hash = hash_token(token)
    await SecurityService.save_token(
        user_id, token_hash, "email_verification", config.email_verification_expire_hours
    )
    await EmailService.send_email_verification(email, token, username)
    return token


async def verify_email(token: str) -> bool:
    """Verify email with token"""
    token_hash = hash_token(token)
    user_id = await SecurityService.verify_email_token(token_hash)
    return user_id is not None


# Password reset functions
async def send_password_reset(email: str):
    """Send password reset email"""
    user = await get_user(email)
    if not user:
        return False  # Don't reveal if email exists

    token = SecurityService.create_token()
    token_hash = hash_token(token)
    await SecurityService.save_token(
        user.userId, token_hash, "password_reset", config.password_reset_expire_hours
    )
    await EmailService.send_password_reset(email, token, user.username)
    return True


async def reset_password(token: str, new_password: str) -> bool:
    """Reset password with token"""
    token_hash = hash_token(token)
    token_data = await SecurityService.verify_token(token_hash, "password_reset")
    if not token_data:
        return False

    # Update password using userId
    hashed_password = get_password_hash(new_password)
    await database["users"].update_one(
        {"userId": token_data["userId"]}, {"$set": {"password": hashed_password}}
    )

    # Delete token
    await SecurityService.delete_token(token_hash, "password_reset")

    # Reset failed attempts
    user = await database["users"].find_one({"userId": token_data["userId"]})
    if user:
        await SecurityService.reset_failed_login_attempts(user["userId"])
        await SecurityService.unlock_account(user["userId"])

    return True


async def resend_verification_email(email: str):
    """Resend verification email"""
    user = await get_user(email)
    if not user:
        return False

    if user.isEmailVerified:
        return False  # Already verified

    await send_email_verification(user.userId, user.email, user.username)
    return True
