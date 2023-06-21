from jose import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

from src.db import database
from src.config import config
from src.auth.schemas import UserLogin
from src.auth.exceptions import IncorrectEmailOrPassword

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/signin")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.secret_key, algorithm=config.algorithm)
    return encoded_jwt

async def get_user(username_or_email: str):
    query = {
        "$or": [
            {"username": username_or_email},
            {"email": username_or_email}
        ]
    }
    user = await database["users"].find_one(query)
    if user:
        return UserLogin(**user)

async def authenticate_user(username_or_email: str, password: str):
    user = await get_user(username_or_email)
    if not user:
        raise IncorrectEmailOrPassword()
    if not verify_password(password, user.password):
        raise IncorrectEmailOrPassword()

    return user
