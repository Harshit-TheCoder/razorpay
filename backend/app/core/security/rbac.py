from enum import Enum
from fastapi import HTTPException, status, Depends
from .auth_dependency import get_current_user, TokenPayload

class Role(str, Enum):
    MERCHANT_ADMIN = "merchant_admin"
    OPS_VIEWER = "ops_viewer"
    SYSTEM = "system"

def require_role(allowed_roles: list[Role]):
    async def role_checker(current_user: TokenPayload = Depends(get_current_user)):
        if current_user.role not in [role.value for role in allowed_roles]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        return current_user
    return role_checker
