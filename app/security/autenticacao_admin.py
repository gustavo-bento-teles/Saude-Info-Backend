from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException

from app.core import ADMIN_PASSWORD

security = HTTPBearer()

def verificar_credencial_admin(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    credencial = credentials.credentials

    if credencial != ADMIN_PASSWORD:
        raise HTTPException(
            status_code=401,
            detail="Credencial inválida"
        )

    return True