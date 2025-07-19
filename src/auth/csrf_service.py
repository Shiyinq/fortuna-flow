import secrets
from fastapi import Request, HTTPException, status


class CSRFService:
    CSRF_TOKEN_COOKIE = "csrf_token"
    CSRF_TOKEN_HEADER = "X-CSRF-Token"
    
    @staticmethod
    def set_csrf_cookie(response, is_dev: bool = False):
        response.set_cookie(
            key=CSRFService.CSRF_TOKEN_COOKIE,
            value=secrets.token_urlsafe(32),
            httponly=False,
            max_age=3600,
            path="/",
            samesite="lax",
            secure=not is_dev
        )
    
    @staticmethod
    def validate_csrf_token(request: Request) -> bool:
        header_token = request.headers.get(CSRFService.CSRF_TOKEN_HEADER)
        
        cookie_token = request.cookies.get(CSRFService.CSRF_TOKEN_COOKIE)
        
        if not header_token or not cookie_token:
            return False
            

        return secrets.compare_digest(header_token, cookie_token)
    
    @staticmethod
    def require_csrf_token(request: Request):
        if not CSRFService.validate_csrf_token(request):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid CSRF token"
            ) 