from fastapi import APIRouter, Depends

from src import dependencies
from src.auth.schemas import UserCurrent
from src.logging_config import create_logger
from src.users import service
from src.users.schemas import UserCreate, UserCreateResponse

router = APIRouter()

logger = create_logger("users", __name__)


@router.post("/users/signup", status_code=201, response_model=UserCreateResponse)
async def signup(user: UserCreate):
    """
    Register a new user account.

    Parameters:
        user (UserCreate): The user registration data.

    Returns:
        UserCreateResponse: Confirmation message or created user data.
    """
    logger.info(
        f"[SIGNUP] Incoming request to create user: username={user.username if hasattr(user, 'username') else ''}"
    )
    try:
        new_user = await service.create_user(user)
        logger.info(
            f"[SIGNUP] User created successfully: user_id={getattr(new_user, 'userId', None)}"
        )
        return new_user
    except Exception as e:
        logger.exception(f"[SIGNUP] Error creating user: {str(e)}")
        raise


@router.get("/users/profile", response_model=UserCurrent)
async def user_profile(current_user=Depends(dependencies.get_current_user)):
    """
    Get the profile information of the currently logged-in user.

    Returns:
        UserCurrent: The current user's profile data.
    """
    logger.info(
        f"[PROFILE] Incoming request to get user profile: user_id={current_user.userId}"
    )
    try:
        return current_user
    except Exception as e:
        logger.exception(f"[PROFILE] Error getting user profile: {str(e)}")
        raise
