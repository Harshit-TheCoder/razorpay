from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
from .jwt_handler import decode_access_token
from pydantic import BaseModel

security = HTTPBearer()

class TokenPayload(BaseModel):
    sub: str
    merchant_id: str
    role: str

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> TokenPayload:
    token = credentials.credentials
    try:
        payload_dict = decode_access_token(token)
        payload = TokenPayload(**payload_dict)
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload
