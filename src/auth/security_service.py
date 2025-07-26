import secrets
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

from src.auth.email_service import EmailService
from src.config import config
from src.database import database


class SecurityService:
    @staticmethod
    def create_token() -> str:
        """Create secure token for verification or password reset"""
        return secrets.token_urlsafe(32)

    @staticmethod
    async def save_token(user_id: str, token: str, token_type: str, expire_hours: int):
        """Save verification token to general collection"""
        # Delete old tokens for this user and type first
        await database["verification_tokens"].delete_many(
            {"userId": user_id, "tokenType": token_type}
        )

        expires_at = datetime.now(timezone.utc) + timedelta(hours=expire_hours)
        data = {
            "userId": user_id,
            "hashToken": token,
            "tokenType": token_type,
            "expiresAt": expires_at,
            "createdAt": datetime.now(timezone.utc),
        }
        await database["verification_tokens"].insert_one(data)

    @staticmethod
    async def get_token(token: str, token_type: str) -> Optional[Dict[str, Any]]:
        """Get token data by type"""
        return await database["verification_tokens"].find_one(
            {"hashToken": token, "tokenType": token_type}
        )

    @staticmethod
    async def delete_token(token: str, token_type: str):
        """Delete token by type"""
        await database["verification_tokens"].delete_one(
            {"hashToken": token, "tokenType": token_type}
        )

    @staticmethod
    async def verify_token(token: str, token_type: str) -> Optional[Dict[str, Any]]:
        """Verify token and return token data if valid"""
        token_data = await SecurityService.get_token(token, token_type)

        if not token_data:
            return None

        # Ensure expires_at has timezone info
        expires_at = token_data["expiresAt"]
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)

        # Check if token expired
        if expires_at < datetime.now(timezone.utc):
            # Delete expired token
            await SecurityService.delete_token(token, token_type)
            return None

        return token_data

    @staticmethod
    async def verify_email_token(token: str) -> Optional[str]:
        """Verify email verification token"""
        token_data = await SecurityService.verify_token(token, "email_verification")

        if not token_data:
            return None

        # Mark user email as verified
        await database["users"].update_one(
            {"userId": token_data["userId"]}, {"$set": {"isEmailVerified": True}}
        )

        # Delete token after successful verification
        await SecurityService.delete_token(token, "email_verification")

        return token_data["userId"]

    @staticmethod
    async def increment_failed_login_attempts(user_id: str):
        """Increment failed login attempts count"""
        await database["users"].update_one(
            {"userId": user_id}, {"$inc": {"failedLoginAttempts": 1}}
        )

    @staticmethod
    async def reset_failed_login_attempts(user_id: str):
        """Reset failed login attempts count"""
        await database["users"].update_one(
            {"userId": user_id}, {"$set": {"failedLoginAttempts": 0}}
        )

    @staticmethod
    async def lock_account(user_id: str, duration_minutes: int = 15):
        """Lock account temporarily"""
        locked_until = datetime.now(timezone.utc) + timedelta(minutes=duration_minutes)

        await database["users"].update_one(
            {"userId": user_id},
            {"$set": {"isAccountLocked": True, "accountLockedUntil": locked_until}},
        )

    @staticmethod
    async def unlock_account(user_id: str):
        """Unlock account"""
        await database["users"].update_one(
            {"userId": user_id},
            {
                "$set": {
                    "isAccountLocked": False,
                    "accountLockedUntil": None,
                    "failedLoginAttempts": 0,
                }
            },
        )

    @staticmethod
    async def check_account_lock_status(user_id: str) -> Dict[str, Any]:
        """Check account lock status"""
        user = await database["users"].find_one({"userId": user_id})
        if not user:
            return {"is_locked": False, "locked_until": None}

        is_locked = user.get("isAccountLocked", False)
        locked_until = user.get("accountLockedUntil")

        # Auto unlock if expired
        if is_locked and locked_until:
            # Ensure locked_until has timezone info
            if locked_until.tzinfo is None:
                locked_until = locked_until.replace(tzinfo=timezone.utc)

            if locked_until < datetime.now(timezone.utc):
                await SecurityService.unlock_account(user_id)
                return {"is_locked": False, "locked_until": None}

        return {"is_locked": is_locked, "locked_until": locked_until}

    @staticmethod
    async def handle_failed_login(user_id: str, email: str, username: str):
        """Handle failed login with security measures"""
        # Increment failed attempts
        await SecurityService.increment_failed_login_attempts(user_id)

        # Check if account needs to be locked
        user = await database["users"].find_one({"userId": user_id})
        if user and user.get("failedLoginAttempts", 0) >= config.max_login_attempts:
            await SecurityService.lock_account(user_id, config.account_lockout_minutes)

            # Send email notification
            await EmailService.send_account_locked_notification(
                email, username, config.account_lockout_minutes
            )

    @staticmethod
    async def delete_expired_verification_tokens():
        """Delete expired verification tokens"""
        current_time = datetime.now(timezone.utc)
        await database["verification_tokens"].delete_many(
            {"expiresAt": {"$lt": current_time}}
        )

    @staticmethod
    async def cleanup_expired_tokens():
        """Clean up all expired tokens"""
        await SecurityService.delete_expired_verification_tokens()
        await SecurityService.delete_expired_refresh_tokens()

    @staticmethod
    async def delete_expired_refresh_tokens():
        """Delete expired refresh tokens"""
        from src.auth.constants import REFRESH_TOKEN_MAX_AGE
        from src.auth.service import delete_refresh_token

        # Find expired refresh tokens
        expired_tokens = (
            await database["refresh_tokens"]
            .find(
                {
                    "createdAt": {
                        "$lt": (
                            datetime.now(timezone.utc)
                            - timedelta(days=REFRESH_TOKEN_MAX_AGE)
                        ).isoformat()
                    }
                }
            )
            .to_list(length=None)
        )

        # Delete each expired token
        for token_data in expired_tokens:
            await delete_refresh_token(token_data["hashRefreshToken"])
