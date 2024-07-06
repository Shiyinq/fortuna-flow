from datetime import datetime
from uuid import UUID, uuid4

from password_validator import PasswordValidator
from pydantic import BaseModel, EmailStr, Field, root_validator

from src.auth.service import get_password_hash
from src.users.exceptions import PasswordNotMatch, PasswordRules


class UserBase(BaseModel):
    userId: UUID = Field(default_factory=lambda: str(uuid4()))
    profilePicture: str = Field(max_length=255, default=None)
    name: str = Field(max_length=20)
    username: str = Field(max_length=50)
    email: EmailStr
    provider: str = Field(default=None)
    createdAt: datetime = Field(default_factory=datetime.now, example=None)
    updatedAt: datetime = Field(default_factory=datetime.now, example=None)

    class Config:
        schema_extra = {
            "example": {
                "name": "string",
                "username": "string",
                "email": "user@example.com",
                "password": "string123",
                "confirmPassword": "string123",
            }
        }


class PasswordBase(UserBase):
    password: str
    confirmPassword: str

    @root_validator(skip_on_failure=True)
    def verify_password_match(cls, values):
        password = values.get("password")
        confirm_password = values.get("confirmPassword")

        if password != confirm_password:
            raise PasswordNotMatch

        password_rules = PasswordValidator()
        password_rules.min(6).max(15).has().digits().has().no().spaces()
        if not password_rules.validate(password):
            raise PasswordRules

        return values


class UserCreate(PasswordBase):
    def to_dict(self):
        data = self.dict()
        data["password"] = get_password_hash(data["password"])
        data.pop("confirmPassword")
        return data


class ProviderUserCreate(UserBase):
    def to_dict(self):
        return self.dict()


class UserCreateResponse(BaseModel):
    detail: str
