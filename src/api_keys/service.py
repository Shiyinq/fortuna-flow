import secrets
from src.config import config
from src.api_keys.exceptions import APIKeyNotFound, InvalidAPIKey
from src.api_keys.schemas import APIKeysResponse, CreateAPIKey
from src.api_keys.constants import Info
from src.utils import hash_token
from src.api_keys import repository


async def create_api_key(user_id: str) -> APIKeysResponse:
    api_key = f"{config.api_key_prefix}{secrets.token_urlsafe(32)}"
    hash_key = hash_token(api_key)
    data = CreateAPIKey(userId=user_id, hashKey=hash_key)

    await check_and_delete_api_key(user_id)
    await repository.insert_api_key(data.model_dump())

    return APIKeysResponse(apiKey=api_key, detail=Info.API_KEY_CREATED + " " + Info.API_KEY_WARNING)


async def check_and_delete_api_key(user_id: str) -> bool:
    curent_api_key = await repository.find_user_api_key(user_id)
    if curent_api_key:
        deleted = await repository.delete_user_api_key(user_id)
        return  deleted.deleted_count == 1
    
    return False


async def delete_api_key(user_id: str) -> APIKeysResponse:
    if await check_and_delete_api_key(user_id):
            return APIKeysResponse(apiKey="", detail=Info.API_KEY_DELETED)

    raise APIKeyNotFound()


async def update_last_used_api_key(user_id: str) -> bool:
    updated = await repository.update_last_used_api_key(user_id)
    return updated.modified_count == 1


async def validate_api_key(api_key: str) -> bool:
    hash_key = hash_token(api_key)
    query = [
        {
            '$match': {
                'hashKey': hash_key
            }
        }, {
            '$lookup': {
                'from': 'users', 
                'localField': 'userId', 
                'foreignField': 'userId', 
                'as': 'user'
            }
        }, {
            '$unwind': {
                'path': '$user', 
                'preserveNullAndEmptyArrays': True
            }
        }, {
            '$project': {
                'userId': 1, 
                'profilePicture': '$user.profilePicture', 
                'name': '$user.name', 
                'username': '$user.username', 
                'email': '$user.email'
            }
        }
    ]

    user = await repository.find_api_key(query)
    if not len(user):
        raise InvalidAPIKey()
    
    await update_last_used_api_key(user[0]['userId'])

    return user[0]