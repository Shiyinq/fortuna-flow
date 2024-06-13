from fastapi import APIRouter, Depends

from src import dependencies
from src.auth.schemas import UserCurrent
from src.users import service
from src.users.schemas import UserCreate, UserCreateResponse

router = APIRouter()


@router.post("/users/signup", status_code=201, response_model=UserCreateResponse)
async def signup(user: UserCreate):
    """Create new user"""
    new_user = await service.create_user(user)
    return new_user


@router.get("/users/profile", response_model=UserCurrent)
async def user_profile(current_user=Depends(dependencies.get_current_user)):
    """Get info current user login"""
    return current_user
