from src.user.constants import ErrorCode
from src.exceptions import UnprocessableContent, Conflict, InternalServerError

class UsernameTaken(Conflict):
    DETAIL = ErrorCode.USERNAME_TAKEN

class EmailTaken(Conflict):
    DETAIL = ErrorCode.EMAIL_TAKEN

class PasswordNotMatch(UnprocessableContent):
    DETAIL = ErrorCode.PASSWORD_MISMATCH

class PasswordRules(UnprocessableContent):
    DETAIL = ErrorCode.PASSWORD_RULES

class ServerError(InternalServerError):
    pass