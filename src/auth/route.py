from fastapi import APIRouter, Depends, Request, Response, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_sso.sso.github import GithubSSO
from fastapi_sso.sso.google import GoogleSSO
from datetime import timedelta, datetime, timezone

from src.auth import service
from src.auth.schemas import Token
from src.config import config
from src.users.schemas import ProviderUserCreate
from src.users.service import create_user_provider
from src.auth.constants import Info

router = APIRouter()

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
async def signin_with_email_and_password(
    form_data: OAuth2PasswordRequestForm = Depends(),
    request: Request = None,
    response: Response = None
):
    user = await service.authenticate_user(form_data.username, form_data.password)
    access_token = service.create_access_token(data={"sub": user.userId}, expires_delta=timedelta(minutes=3))
    await service.set_refresh_cookie_and_history(response, user.userId, request, config)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/auth/refresh", response_model=Token)
async def refresh_access_token(request: Request, response: Response):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No refresh token")

    token_data = await service.get_refresh_token(refresh_token)
    if not token_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    device, ip, browser, user_agent = service.extract_request_info(request)
    if token_data["device"] != device or token_data["ip"] != ip or token_data["browser"] != browser:
        await service.delete_refresh_token(refresh_token)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Aktivitas mencurigakan, silakan login ulang.")

    created_at = datetime.fromisoformat(token_data["createdAt"])
    if (datetime.now(timezone.utc) - created_at).days >= 30:
        await service.delete_refresh_token(refresh_token)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token expired, silakan login ulang.")

    await service.update_refresh_token_last_used(refresh_token)
    await service.save_login_history(token_data["userId"], device, ip, browser, refresh_token, user_agent_raw=user_agent)
    access_token = service.create_access_token(data={"sub": token_data["userId"]}, expires_delta=timedelta(minutes=3))
    return {"access_token": access_token, "token_type": "bearer"}


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
    return {"message": Info.LOGOUT_SUCCESS}
