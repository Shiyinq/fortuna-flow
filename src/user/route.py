from fastapi import APIRouter

from src.user import service
from src.user.schemas import UserCreate, UserCreateResponse

router = APIRouter()

@router.post('/signup', status_code=201, response_model=UserCreateResponse)
async def signup(user: UserCreate):
	new_user = await service.create_user(user)
	return new_user