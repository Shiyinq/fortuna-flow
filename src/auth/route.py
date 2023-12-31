from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_sso.sso.github import GithubSSO
from fastapi_sso.sso.google import GoogleSSO

from src.auth import service
from src.auth.schemas import Token
from src.config import config
from src.user.schemas import ProviderUserCreate
from src.user.service import create_user_provider

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


@router.post("/auth/login", response_model=Token)
async def login_with_email_and_password(
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    """Login using username or email and password"""
    user = await service.authenticate_user(form_data.username, form_data.password)
    access_token = service.create_access_token(data={"sub": user.username})

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/auth/google/login")
async def login_with_google():
    """Initialize auth and redirect to google"""
    try:
        with google_sso:
            return await google_sso.get_login_redirect(
                params={"prompt": "consent", "access_type": "offline"}
            )
    except Exception as e:
        return {"detail": e}


@router.get("/auth/google/callback")
async def google_auth_callback(request: Request):
    """Verify login from google"""
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

            return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        return {"detail": e}


@router.get("/auth/github/login")
async def login_with_github():
    """Initialize auth and redirect to github"""
    try:
        with github_sso:
            return await github_sso.get_login_redirect()
    except Exception as e:
        return {"detail": e}


@router.get("/auth/github/callback")
async def github_auth_callback(request: Request):
    """Verify login from github"""
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

            return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        return {"detail": e}
