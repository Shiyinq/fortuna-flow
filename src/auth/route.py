import os

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_sso.sso.github import GithubSSO

from src.auth import service
from src.auth.schemas import Token
from src.user.schemas import GithubUserCreate
from src.user.service import create_github_user

load_dotenv(verbose=True)

GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
GITHUB_REDIRECT_URI = os.getenv("GITHUB_REDIRECT_URI")

router = APIRouter()


sso = GithubSSO(
    client_id=GITHUB_CLIENT_ID,
    client_secret=GITHUB_CLIENT_SECRET,
    redirect_uri=GITHUB_REDIRECT_URI,
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


@router.get("/auth/github/login")
async def login_with_github():
    """Initialize auth and redirect to github"""
    try:
        with sso:
            return await sso.get_login_redirect()
    except Exception as e:
        return {"detail": e}


@router.get("/auth/github/callback")
async def github_auth_callback(request: Request):
    """Verify login from github"""
    try:
        with sso:
            user = await sso.verify_and_process(request)
            check_user = await service.authenticate_user(
                username_or_email=user.email, provider=user.provider
            )
            if not check_user:
                github_user = {
                    "profilePicture": user.picture,
                    "name": user.display_name,
                    "username": user.email,
                    "email": user.email,
                    "provider": user.provider,
                }
                github_user = GithubUserCreate(**github_user)
                await create_github_user(github_user)

            access_token = service.create_access_token(data={"sub": user.email})

            return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        return {"detail": e}
