from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src import dependencies
from src.auth import service
from src.auth.schemas import Token

router = APIRouter()


@router.post("/signin", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login using username or email and password"""
    user = await service.authenticate_user(form_data.username, form_data.password)
    access_token = service.create_access_token(data={"sub": user.username})

    return {"access_token": access_token, "token_type": "bearer"}
