import resend

from src.config import config
from src.logging_config import create_logger

logger = create_logger("email", __name__)

# Setup Resend
resend.api_key = config.resend_api_key


class EmailService:
    @staticmethod
    async def send_email_verification(email: str, token: str, username: str):
        """Send email verification"""
        verification_url = f"{config.frontend_url}/auth/verify-email?token={token}"

        html_content = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h2 style="color: #333;">Verify Your Email</h2>
            <p>Hello {username},</p>
            <p>Thank you for registering with Fortuna Flow. Please verify your email by clicking the button below:</p>
            <div style="text-align: center; margin: 30px 0;">
                <a href="{verification_url}" 
                   style="background-color: #007bff; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block;">
                    Verify Email
                </a>
            </div>
            <p>Or copy this link to your browser:</p>
            <p style="word-break: break-all; color: #666;">{verification_url}</p>
            <p>This link will expire in {config.email_verification_expire_hours} hours.</p>
            <p>If you did not register with Fortuna Flow, please ignore this email.</p>
            <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
            <p style="color: #666; font-size: 12px;">Fortuna Flow - Track Your Finances, Unleash Your Fortune</p>
        </div>
        """

        try:
            logger.info(f"[EMAIL_VERIFICATION] Sending verification email to {email}")
            r = resend.Emails.send(
                {
                    "from": config.email_from,
                    "to": email,
                    "subject": "Verify Your Email - Fortuna Flow",
                    "html": html_content,
                }
            )
            logger.info(f"[EMAIL_VERIFICATION] Email sent successfully to {email}")
            return r
        except Exception as e:
            logger.exception(
                f"[EMAIL_VERIFICATION] Error sending email to {email}: {e}"
            )
            return None

    @staticmethod
    async def send_password_reset(email: str, token: str, username: str):
        """Send password reset email"""
        reset_url = f"{config.frontend_url}/auth/reset-password?token={token}"

        html_content = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h2 style="color: #333;">Reset Your Password</h2>
            <p>Hello {username},</p>
            <p>We received a request to reset your account password. Please click the button below to create a new password:</p>
            <div style="text-align: center; margin: 30px 0;">
                <a href="{reset_url}" 
                   style="background-color: #dc3545; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block;">
                    Reset Password
                </a>
            </div>
            <p>Or copy this link to your browser:</p>
            <p style="word-break: break-all; color: #666;">{reset_url}</p>
            <p>This link will expire in {config.password_reset_expire_hours} hour.</p>
            <p>If you did not request a password reset, please ignore this email. Your password will not be changed.</p>
            <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
            <p style="color: #666; font-size: 12px;">Fortuna Flow - Track Your Finances, Unleash Your Fortune</p>
        </div>
        """

        try:
            logger.info(f"[PASSWORD_RESET] Sending password reset email to {email}")
            r = resend.Emails.send(
                {
                    "from": config.email_from,
                    "to": email,
                    "subject": "Reset Your Password - Fortuna Flow",
                    "html": html_content,
                }
            )
            logger.info(f"[PASSWORD_RESET] Email sent successfully to {email}")
            return r
        except Exception as e:
            logger.exception(
                f"[PASSWORD_RESET] Error sending password reset email to {email}: {e}"
            )
            return None

    @staticmethod
    async def send_account_locked_notification(
        email: str, username: str, lockout_duration: int
    ):
        """Send account locked notification"""
        html_content = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h2 style="color: #dc3545;">Your Account Has Been Locked</h2>
            <p>Hello {username},</p>
            <p>Your account has been temporarily locked due to too many failed login attempts.</p>
            <p>Your account will be automatically unlocked in {lockout_duration} minutes.</p>
            <p>If you forgot your password, please use the "Forgot Password" feature to reset your password.</p>
            <p>If you believe this is an error, please contact our support team.</p>
            <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
            <p style="color: #666; font-size: 12px;">Fortuna Flow - Track Your Finances, Unleash Your Fortune</p>
        </div>
        """

        try:
            logger.info(
                f"[ACCOUNT_LOCKED] Sending account locked notification to {email}"
            )
            r = resend.Emails.send(
                {
                    "from": config.email_from,
                    "to": email,
                    "subject": "Account Locked - Fortuna Flow",
                    "html": html_content,
                }
            )
            logger.info(f"[ACCOUNT_LOCKED] Email sent successfully to {email}")
            return r
        except Exception as e:
            logger.exception(
                f"[ACCOUNT_LOCKED] Error sending account locked notification to {email}: {e}"
            )
            return None
