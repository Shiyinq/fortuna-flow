from fastapi import APIRouter, Depends, Request, Response, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_sso.sso.github import GithubSSO
from fastapi_sso.sso.google import GoogleSSO
from datetime import datetime, timezone
from slowapi import Limiter
from slowapi.util import get_remote_address

from src.auth import service
from src.auth.schemas import (
    Token, EmailVerificationRequest, EmailVerificationResponse,
    VerifyEmailRequest, VerifyEmailResponse, PasswordResetRequest,
    PasswordResetResponse, PasswordResetConfirmRequest, PasswordResetConfirmResponse,SecurityStatus
)
from src.config import config
from src.users.schemas import ProviderUserCreate
from src.users.service import create_user_provider
from src.auth.constants import Info, ErrorCode
from src.auth.exceptions import (
    InvalidRefreshToken, RefreshTokenExpired, SuspiciousActivity,
    VerificationTokenInvalid, PasswordResetTokenInvalid, PasswordsNotMatch, PasswordPolicyViolation
)
from src.logging_config import create_logger

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

logger = create_logger("auth", __name__)

github_sso = GithubSSO(
    client_id=config.github_client_id,
    client_secret=config.github_client_secret,
    redirect_uri=config.github_redirect_uri,
    allow_insecure_http=True,
)

google_sso = GoogleSSO(
    client_id=config.google_client_id,
    client_secret=config.google_client_secret,
    redirect_uri=config.google_redirect_uri,
    allow_insecure_http=True,
)

@router.post("/auth/signin", response_model=Token)
@limiter.limit(f"{config.max_requests_per_minute}/minute")
async def signin_with_email_and_password(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    response: Response = None
):
    logger.info(f"[SIGNIN] Incoming request: {request.method} {request.url} username={form_data.username}")
    try:
        user = await service.authenticate_user(form_data.username, form_data.password)
        access_token = service.create_access_token(data={"sub": user.userId})
        await service.set_refresh_cookie_and_history(response, user.userId, request, config)
        logger.info(f"[SIGNIN] Login success user_id={user.userId}")
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        logger.exception(f"[SIGNIN] Error: {str(e)}")
        raise


@router.post("/auth/refresh", response_model=Token)
async def refresh_access_token(request: Request, response: Response):
    logger.info(f"[REFRESH] Incoming request: {request.method} {request.url}")
    try:
        refresh_token = request.cookies.get("refresh_token")
        if not refresh_token:
            logger.warning("[REFRESH] No refresh_token in cookie")
            raise InvalidRefreshToken()

        token_data = await service.get_refresh_token(refresh_token)
        if not token_data:
            logger.warning("[REFRESH] Token data not found")
            raise InvalidRefreshToken()

        device, ip, browser, user_agent = service.extract_request_info(request)
        if token_data["device"] != device or token_data["ip"] != ip or token_data["browser"] != browser:
            logger.warning(f"[REFRESH] Device/IP/Browser mismatch user_id={token_data.get('userId')}")
            await service.delete_refresh_token(refresh_token)
            raise SuspiciousActivity()

        created_at = datetime.fromisoformat(token_data["createdAt"])
        if (datetime.now(timezone.utc) - created_at).days >= config.refresh_token_max_age_days:
            logger.info(f"[REFRESH] Refresh token expired user_id={token_data.get('userId')}")
            await service.delete_refresh_token(refresh_token)
            raise RefreshTokenExpired()

        await service.update_refresh_token_last_used(refresh_token)
        await service.save_login_history(token_data["userId"], device, ip, browser, refresh_token, user_agent_raw=user_agent)
        access_token = service.create_access_token(data={"sub": token_data["userId"]})
        logger.info(f"[REFRESH] Refresh token success user_id={token_data.get('userId')}")
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        logger.exception(f"[REFRESH] Error: {str(e)}")
        raise


@router.get("/auth/google/signin")
async def signin_with_google():
    try:
        with google_sso:
            return await google_sso.get_login_redirect(
                params={"prompt": "consent", "access_type": "offline"}
            )
    except Exception as e:
        return {"detail": e}


@router.get("/auth/google/callback")
async def google_auth_callback(request: Request, response: Response):
    try:
        with google_sso:
            user = await google_sso.verify_and_process(request)
            check_user = await service.authenticate_user(
                username_or_email=user.email, provider=user.provider
            )
            if not check_user:
                user_provider = service.extract_user_provider(user)
                user_provider = ProviderUserCreate(**user_provider)
                await create_user_provider(user_provider)
            access_token = service.create_access_token(data={"sub": user.email})
            await service.set_refresh_cookie_and_history(response, user.email, request, config)
            redirect_url = (
                f"{config.frontend_url}/auth/callback?access_token={access_token}"
            )
            return RedirectResponse(url=redirect_url)
    except Exception as e:
        return {"detail": e}


@router.get("/auth/github/signin")
async def signin_with_github():
    try:
        with github_sso:
            return await github_sso.get_login_redirect()
    except Exception as e:
        return {"detail": e}


@router.get("/auth/github/callback")
async def github_auth_callback(request: Request, response: Response):
    try:
        with github_sso:
            user = await github_sso.verify_and_process(request)
            check_user = await service.authenticate_user(
                username_or_email=user.email, provider=user.provider
            )
            if not check_user:
                user_provider = service.extract_user_provider(user)
                user_provider = ProviderUserCreate(**user_provider)
                await create_user_provider(user_provider)
            access_token = service.create_access_token(data={"sub": user.email})
            await service.set_refresh_cookie_and_history(response, user.email, request, config)
            redirect_url = (
                f"{config.frontend_url}/auth/callback?access_token={access_token}"
            )
            return RedirectResponse(url=redirect_url)
    except Exception as e:
        return {"detail": e}


@router.post("/auth/logout")
async def logout(request: Request, response: Response):
    logger.info(f"[LOGOUT] Incoming request: {request.method} {request.url}")
    try:
        refresh_token = request.cookies.get("refresh_token")
        if refresh_token:
            await service.delete_refresh_token(refresh_token)
            response.delete_cookie(
                key="refresh_token",
                path="/",
                samesite="lax",
                secure=not config.is_env_dev,
                httponly=True
            )
        logger.info(f"[LOGOUT] Logout success")
        return {"message": Info.LOGOUT_SUCCESS}
    except Exception as e:
        logger.exception(f"[LOGOUT] Error: {str(e)}")
        raise


# Email Verification Endpoints
@router.post("/auth/send-verification", response_model=EmailVerificationResponse)
@limiter.limit(f"{config.max_requests_per_minute}/minute")
async def send_email_verification(request: Request, request_data: EmailVerificationRequest):
    success = await service.resend_verification_email(request_data.email)
    if success:
        return EmailVerificationResponse(message=Info.EMAIL_VERIFICATION_SENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ErrorCode.EMAIL_NOT_FOUND_OR_VERIFIED)


@router.post("/auth/verify-email", response_model=VerifyEmailResponse)
async def verify_email_endpoint(request_data: VerifyEmailRequest):
    success = await service.verify_email(request_data.token)
    if success:
        return VerifyEmailResponse(message=ErrorCode.EMAIL_VERIFIED_SUCCESS)
    else:
        raise VerificationTokenInvalid()


# Password Reset Endpoints
@router.post("/auth/forgot-password", response_model=PasswordResetResponse)
@limiter.limit(f"{config.max_requests_per_minute}/minute")
async def forgot_password(request: Request, request_data: PasswordResetRequest):
    success = await service.send_password_reset(request_data.email)
    return PasswordResetResponse(message=ErrorCode.PASSWORD_RESET_SENT)


@router.post("/auth/reset-password", response_model=PasswordResetConfirmResponse)
async def reset_password_endpoint(request_data: PasswordResetConfirmRequest):
    if request_data.new_password != request_data.confirm_password:
        raise PasswordsNotMatch()
    
    # Validate password strength
    from password_validator import PasswordValidator
    password_rules = PasswordValidator()
    password_rules.min(8).max(128).has().uppercase().has().lowercase().has().digits().has().symbols().no().spaces()
    if not password_rules.validate(request_data.new_password):
        raise PasswordPolicyViolation()
    
    success = await service.reset_password(request_data.token, request_data.new_password)
    if success:
        return PasswordResetConfirmResponse(message=ErrorCode.PASSWORD_RESET_SUCCESS)
    else:
        raise PasswordResetTokenInvalid()
