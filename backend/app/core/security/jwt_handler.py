from datetime import datetime, timedelta
from typing import Any, Dict, Optional
from jose import jwt
from app.core.config import get_settings

settings = get_settings()

ALGORITHM = "HS256"

def create_access_token(subject: str, merchant_id: str, role: str, expires_delta: Optional[timedelta] = None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=60)
        
    to_encode = {
        "exp": expire,
        "sub": str(subject),
        "merchant_id": str(merchant_id),
        "role": role
    }
    encoded_jwt = jwt.encode(to_encode, settings.RAZORPAY_KEY_SECRET or "test_secret_key", algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> Dict[str, Any]:
    # Will raise jwt.JWTError if invalid
    payload = jwt.decode(token, settings.RAZORPAY_KEY_SECRET or "test_secret_key", algorithms=[ALGORITHM])
    return payload
