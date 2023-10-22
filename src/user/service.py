from typing import Dict

from pymongo.errors import DuplicateKeyError

from src.database import database
from src.user.constants import Info
from src.user.exceptions import EmailTaken, ServerError, UsernameTaken
from src.user.schemas import GithubUserCreate, UserCreate


async def base_create_user(user) -> Dict[str, str]:
    try:
        user_data = user.to_dict()
        await database["users"].insert_one(user_data)
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
    return await base_create_user(user)


async def create_github_user(user: GithubUserCreate) -> Dict[str, str]:
    return await base_create_user(user)
