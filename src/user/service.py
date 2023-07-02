from typing import Dict

from pymongo.errors import DuplicateKeyError

from src.db import database
from src.user.constants import Info
from src.user.exceptions import EmailTaken, ServerError, UsernameTaken
from src.user.schemas import UserCreate


async def create_user(user: UserCreate) -> Dict[str, str]:
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
    except Exception:
        raise ServerError()
