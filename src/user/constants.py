class ErrorCode:
    USERNAME_TAKEN = "Username already exist."
    EMAIL_TAKEN = "Email already exist."
    PASSWORD_MISMATCH = "The two passwords did not match."
    PASSWORD_RULES = (
        "Password must contain digits, no spaces, min 6 character and max 15 character."
    )


class Info:
    USER_CREATED = "Register success."
