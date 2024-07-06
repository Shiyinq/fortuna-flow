from pydantic import BaseModel


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
