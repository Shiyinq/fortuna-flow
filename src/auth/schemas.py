from pydantic import BaseModel
class UserBase(BaseModel):
    userId: str
    email: str
    username: str

class UserLogin(UserBase):
    password: str

class UserCurrent(UserBase):
    pass

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None