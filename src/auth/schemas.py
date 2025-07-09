from pydantic import BaseModel
from typing import Optional


class UserLoginBase(BaseModel):
    userId: str
    profilePicture: str | None = None
    name: str
    email: str
    username: str


class UserLogin(UserLoginBase):
    password: str = None


class UserCurrent(UserLoginBase):
    pass


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class RefreshTokenData(BaseModel):
    userId: str
    refreshToken: str
    device: str
    ip: str
    browser: str
    createdAt: Optional[str] = None
    lastUsedAt: Optional[str] = None


class LoginHistory(BaseModel):
    userId: str
    device: str
    ip: str
    browser: str
    loginAt: str
    refreshToken: Optional[str] = None
    userAgentRaw: Optional[str] = None
