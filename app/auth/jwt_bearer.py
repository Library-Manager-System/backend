from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from auth.jwt_handler import decodeJWT

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True, min_permission=1):
        self.min_permission = min_permission
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403,
                    detail="Invalid authentication scheme."
                )
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(
                    status_code=403,
                    detail="Invalid token or expired token."
                )
            if self.permission < self.min_permission:
                raise HTTPException(
                    status_code=403,
                    detail="Insufficient permissions."
                )
            return {
                "token": credentials.credentials,
                "permission": self.permission,
                "email": self.email
            }
        else:
            raise HTTPException(
                status_code=403,
                detail="Invalid authorization code."
            )
    
    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False
        try:
            payload = decodeJWT(jwtoken)
            self.permission = payload["type"]
            self.email = payload["email"]
        except:
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid
