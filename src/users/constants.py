class ErrorCode:
    USERNAME_TAKEN = "Username already exist."
    EMAIL_TAKEN = "Email already exist."
    PASSWORD_MISMATCH = "The two passwords did not match."
    PASSWORD_RULES = "Password must contain at least 8 characters, including uppercase, lowercase, digits, and symbols. No spaces allowed."


class Info:
    USER_CREATED = "Register success."
    USER_CREATED_WITH_EMAIL = (
        "Register success. Please check your email for verification link."
    )
