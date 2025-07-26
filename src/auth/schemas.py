from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserLoginBase(BaseModel):
    userId: str
    profilePicture: str | None = None
    name: str
    email: str
    username: str


class UserLogin(UserLoginBase):
    password: str = None
    isEmailVerified: bool = False
    failedLoginAttempts: int = 0
    isAccountLocked: bool = False
    accountLockedUntil: Optional[datetime] = None


class UserCurrent(UserLoginBase):
    pass


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class RefreshTokenData(BaseModel):
    userId: str
    hashRefreshToken: str
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
    userAgentRaw: Optional[str] = None


# Email Verification Schemas
class EmailVerificationRequest(BaseModel):
    email: str


class EmailVerificationResponse(BaseModel):
    message: str


class VerifyEmailRequest(BaseModel):
    token: str


class VerifyEmailResponse(BaseModel):
    message: str


# Password Reset Schemas
class PasswordResetRequest(BaseModel):
    email: str


class PasswordResetResponse(BaseModel):
    message: str


class PasswordResetConfirmRequest(BaseModel):
    token: str
    new_password: str
    confirm_password: str


class PasswordResetConfirmResponse(BaseModel):
    message: str


# Security Schemas
class SecurityStatus(BaseModel):
    isEmailVerified: bool
    failedLoginAttempts: int
    isAccountLocked: bool
    accountLockedUntil: Optional[datetime] = None
    lastLoginAt: Optional[str] = None


class VerificationToken(BaseModel):
    userId: str
    email: str
    token: str
    tokenType: str  # 'email_verification' or 'password_reset'
    expiresAt: datetime
    createdAt: datetime


class ResendVerificationRequest(BaseModel):
    email: str


class ResendVerificationResponse(BaseModel):
    message: str


class LogoutResponse(BaseModel):
    message: str
