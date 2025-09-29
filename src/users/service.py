from typing import Dict

from pymongo.errors import DuplicateKeyError

from src.auth.service import send_email_verification
from src.users import repository
from src.users.constants import Info
from src.users.exceptions import EmailTaken, ServerError, UsernameTaken
from src.users.schemas import ProviderUserCreate, UserCreate


async def base_create_user(user) -> Dict[str, str]:
    try:
        user_data = user.to_dict()
        await repository.insert_user(user_data)
        return {"detail": Info.USER_CREATED}
    except DuplicateKeyError as dk:
        dk = str(dk)
        if "username" in dk:
            raise UsernameTaken()
        elif "email" in dk:
            raise EmailTaken()
    except Exception as e:
        print(e)
        raise ServerError()


async def create_user(user: UserCreate) -> Dict[str, str]:
    await base_create_user(user)

    # Send email verification for regular signup
    try:
        await send_email_verification(user.userId, user.email, user.username)
        # Return success message with email verification info
        return {"detail": Info.USER_CREATED_WITH_EMAIL}
    except Exception as e:
        print(f"Error sending verification email: {e}")
        # Don't fail the signup if email fails, return basic success message
        return {"detail": Info.USER_CREATED}


async def create_user_provider(user: ProviderUserCreate) -> Dict[str, str]:
    # For provider users, mark email as verified since it's already verified by the provider
    user_data = user.to_dict()
    user_data["isEmailVerified"] = True
    user_data["provider"] = user.provider

    try:
        await repository.insert_user(user_data)
        return {"detail": Info.USER_CREATED}
    except DuplicateKeyError as dk:
        dk = str(dk)
        if "username" in dk:
            raise UsernameTaken()
        elif "email" in dk:
            raise EmailTaken()
    except Exception as e:
        print(e)
        raise ServerError()
