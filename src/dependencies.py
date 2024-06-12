from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from src.auth.exceptions import JwtTokenError
from src.auth.schemas import TokenData, UserCurrent
from src.auth.service import get_user
from src.config import config

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/signin")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, config.secret_key, algorithms=[config.algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise JwtTokenError()
        token_data = TokenData(username=username)
    except JWTError:
        raise JwtTokenError()
    user = await get_user(username_or_email=token_data.username)
    if user is None:
        raise JwtTokenError()
    return UserCurrent(**user.dict())
