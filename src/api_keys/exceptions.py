from src.api_keys.constants import ErrorCode
from src.exceptions import NotFound

class APIKeyNotFound(NotFound):
    DETAIL = ErrorCode.API_KEY_NOT_FOUND