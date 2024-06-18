from datetime import datetime, timedelta
from typing import Dict, Union

from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext

from src.auth.exceptions import IncorrectEmailOrPassword
from src.auth.schemas import UserLogin
from src.config import config
from src.database import database

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/signin")


def verify_password(plain_password, hashed_password) -> str:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=60)
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
