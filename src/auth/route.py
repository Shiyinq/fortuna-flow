from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_sso.sso.github import GithubSSO
from fastapi_sso.sso.google import GoogleSSO
from slowapi import Limiter
from slowapi.util import get_remote_address

from src.auth import service
from src.auth.constants import ErrorCode, Info
from src.auth.csrf_service import CSRFService
from src.auth.exceptions import (
    InvalidRefreshToken,
    PasswordPolicyViolation,
    PasswordResetTokenInvalid,
    PasswordsNotMatch,
    RefreshTokenExpired,
    SuspiciousActivity,
    VerificationTokenInvalid,
)
from src.auth.schemas import (
    EmailVerificationRequest,
    EmailVerificationResponse,
    LogoutResponse,
    PasswordResetConfirmRequest,
    PasswordResetConfirmResponse,
    PasswordResetRequest,
    PasswordResetResponse,
    Token,
    VerifyEmailRequest,
    VerifyEmailResponse,
)
from src.config import config
from src.logging_config import create_logger
from src.users.schemas import ProviderUserCreate
from src.users.service import create_user_provider

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
    response: Response = None,
):
    """
    Sign in using email and password. Returns an access token and sets a refresh token cookie.

    Parameters:
        request (Request): FastAPI request object.
        form_data (OAuth2PasswordRequestForm): Form data containing username and password.
        response (Response): FastAPI response object (used to set cookies).

    Returns:
        Token: Access token and token type.
    """
    logger.info(
        f"[SIGNIN] Incoming request: {request.method} {request.url} username={form_data.username}"
    )
    try:
        user = await service.authenticate_user(form_data.username, form_data.password)
        access_token = service.create_access_token(data={"sub": user.userId})
        await service.set_refresh_cookie_and_history(
            response, user.userId, request, config
        )
        response.set_cookie(
            key="token",
            value=access_token,
            httponly=True,
            max_age=config.access_token_expire_minutes * 60,
            path="/",
            samesite="lax",
            secure=not config.is_env_dev,
        )
        logger.info(f"[SIGNIN] Login success user_id={user.userId}")
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        logger.exception(f"[SIGNIN] Error: {str(e)}")
        raise


@router.post("/auth/refresh", response_model=Token)
async def refresh_access_token(request: Request, response: Response):
    """
    Refresh the access token using a valid refresh token from cookies.

    Parameters:
        request (Request): FastAPI request object (must contain refresh_token cookie).
        response (Response): FastAPI response object.

    Returns:
        Token: New access token and token type.
    """
    logger.info(f"[REFRESH] Incoming request: {request.method} {request.url}")
    try:
        refresh_token = request.cookies.get("refresh_token")
        if not refresh_token:
            logger.warning("[REFRESH] No refresh_token in cookie")
            raise InvalidRefreshToken()

        hash_refresh_token = service.hash_token(refresh_token)
        token_data = await service.get_refresh_token(hash_refresh_token)
        if not token_data:
            logger.warning("[REFRESH] Token data not found")
            raise InvalidRefreshToken()

        device, ip, browser, user_agent = service.extract_request_info(request)
        if (
            token_data["device"] != device
            or token_data["ip"] != ip
            or token_data["browser"] != browser
        ):
            logger.warning(
                f"[REFRESH] Device/IP/Browser mismatch user_id={token_data.get('userId')}"
            )
            await service.delete_refresh_token(hash_refresh_token)
            raise SuspiciousActivity()

        created_at = datetime.fromisoformat(token_data["createdAt"])
        if (
            datetime.now(timezone.utc) - created_at
        ).days >= config.refresh_token_max_age_days:
            logger.info(
                f"[REFRESH] Refresh token expired user_id={token_data.get('userId')}"
            )
            await service.delete_refresh_token(hash_refresh_token)
            raise RefreshTokenExpired()

        await service.update_refresh_token_last_used(hash_refresh_token)
        await service.save_login_history(
            token_data["userId"],
            device,
            ip,
            browser,
            user_agent_raw=user_agent,
        )
        access_token = service.create_access_token(data={"sub": token_data["userId"]})
        logger.info(
            f"[REFRESH] Refresh token success user_id={token_data.get('userId')}"
        )
        response.set_cookie(
            key="token",
            value=access_token,
            httponly=True,
            max_age=config.access_token_expire_minutes * 60,
            path="/",
            samesite="lax",
            secure=not config.is_env_dev,
        )
        
        CSRFService.set_csrf_cookie(response, config.is_env_dev)
        
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        logger.exception(f"[REFRESH] Error: {str(e)}")
        raise


@router.get("/auth/google/signin")
async def signin_with_google():
    """
    Initiate Google OAuth2 sign-in flow. Redirects user to Google login page.

    Returns:
        RedirectResponse: Redirect to Google OAuth2 login.
    """
    try:
        with google_sso:
            return await google_sso.get_login_redirect(
                params={"prompt": "consent", "access_type": "offline"}
            )
    except Exception as e:
        return {"detail": e}


@router.get("/auth/google/callback")
async def google_auth_callback(request: Request, response: Response):
    """
    Google OAuth2 callback endpoint. Handles user info from Google and issues access token.

    Parameters:
        request (Request): FastAPI request object.
        response (Response): FastAPI response object (used to set cookies).

    Returns:
        RedirectResponse: Redirect to frontend with access token as query param.
    """
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
            await service.set_refresh_cookie_and_history(
                response, user.email, request, config
            )
            response.set_cookie(
                key="token",
                value=access_token,
                httponly=True,
                max_age=config.access_token_expire_minutes * 60,
                path="/",
                samesite="lax",
                secure=not config.is_env_dev,
            )
            redirect_url = (
                f"{config.frontend_url}/auth/callback?access_token={access_token}"
            )
            return RedirectResponse(url=redirect_url)
    except Exception as e:
        return {"detail": e}


@router.get("/auth/github/signin")
async def signin_with_github():
    """
    Initiate GitHub OAuth2 sign-in flow. Redirects user to GitHub login page.

    Returns:
        RedirectResponse: Redirect to GitHub OAuth2 login.
    """
    try:
        with github_sso:
            return await github_sso.get_login_redirect()
    except Exception as e:
        return {"detail": e}


@router.get("/auth/github/callback")
async def github_auth_callback(request: Request, response: Response):
    """
    GitHub OAuth2 callback endpoint. Handles user info from GitHub and issues access token.

    Parameters:
        request (Request): FastAPI request object.
        response (Response): FastAPI response object (used to set cookies).

    Returns:
        RedirectResponse: Redirect to frontend with access token as query param.
    """
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
            await service.set_refresh_cookie_and_history(
                response, user.email, request, config
            )
            response.set_cookie(
                key="token",
                value=access_token,
                httponly=True,
                max_age=config.access_token_expire_minutes * 60,
                path="/",
                samesite="lax",
                secure=not config.is_env_dev,
            )
            redirect_url = (
                f"{config.frontend_url}/auth/callback?access_token={access_token}"
            )
            return RedirectResponse(url=redirect_url)
    except Exception as e:
        return {"detail": e}


@router.post("/auth/logout", response_model=LogoutResponse)
async def logout(request: Request, response: Response):
    """
    Log out the current user by deleting the refresh token cookie and invalidating the token in the database.

    Returns:
        LogoutResponse: Message indicating logout success.
    """
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
                httponly=True,
            )
        response.delete_cookie(
            key="token",
            path="/",
            samesite="lax",
            secure=not config.is_env_dev,
            httponly=True,
        )
        logger.info(f"[LOGOUT] Logout success")
        return LogoutResponse(message=Info.LOGOUT_SUCCESS)
    except Exception as e:
        logger.exception(f"[LOGOUT] Error: {str(e)}")
        raise


# Email Verification Endpoints
@router.post("/auth/send-verification", response_model=EmailVerificationResponse)
@limiter.limit(f"{config.max_requests_per_minute}/minute")
async def send_email_verification(
    request: Request, request_data: EmailVerificationRequest
):
    """
    Send a verification email to the user for email verification.

    Parameters:
        request (Request): FastAPI request object.
        request_data (EmailVerificationRequest): Email to send verification to.

    Returns:
        EmailVerificationResponse: Message indicating email sent or error.
    """
    success = await service.resend_verification_email(request_data.email)
    if success:
        return EmailVerificationResponse(message=Info.EMAIL_VERIFICATION_SENT)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorCode.EMAIL_NOT_FOUND_OR_VERIFIED,
        )


@router.post("/auth/verify-email", response_model=VerifyEmailResponse)
async def verify_email_endpoint(request_data: VerifyEmailRequest):
    """
    Verify user's email using the provided token.

    Parameters:
        request_data (VerifyEmailRequest): Contains the verification token.

    Returns:
        VerifyEmailResponse: Message indicating verification result.
    """
    success = await service.verify_email(request_data.token)
    if success:
        return VerifyEmailResponse(message=ErrorCode.EMAIL_VERIFIED_SUCCESS)
    else:
        raise VerificationTokenInvalid()


# Password Reset Endpoints
@router.post("/auth/forgot-password", response_model=PasswordResetResponse)
@limiter.limit(f"{config.max_requests_per_minute}/minute")
async def forgot_password(request: Request, request_data: PasswordResetRequest):
    """
    Send a password reset email to the user.

    Parameters:
        request (Request): FastAPI request object.
        request_data (PasswordResetRequest): Email to send password reset link to.

    Returns:
        PasswordResetResponse: Message indicating reset email sent.
    """
    await service.send_password_reset(request_data.email)
    return PasswordResetResponse(message=ErrorCode.PASSWORD_RESET_SENT)


@router.post("/auth/reset-password", response_model=PasswordResetConfirmResponse)
async def reset_password_endpoint(request_data: PasswordResetConfirmRequest):
    """
    Reset the user's password using the provided token and new password.

    Parameters:
        request_data (PasswordResetConfirmRequest): Contains token, new password, and confirmation.

    Returns:
        PasswordResetConfirmResponse: Message indicating password reset result.
    """
    if request_data.new_password != request_data.confirm_password:
        raise PasswordsNotMatch()

    # Validate password strength
    from password_validator import PasswordValidator

    password_rules = PasswordValidator()
    password_rules.min(8).max(
        128
    ).has().uppercase().has().lowercase().has().digits().has().symbols().no().spaces()
    if not password_rules.validate(request_data.new_password):
        raise PasswordPolicyViolation()

    success = await service.reset_password(
        request_data.token, request_data.new_password
    )
    if success:
        return PasswordResetConfirmResponse(message=ErrorCode.PASSWORD_RESET_SUCCESS)
    else:
        raise PasswordResetTokenInvalid()
