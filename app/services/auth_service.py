from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException

from app.core import ADMIN_PASSWORD

from app.schemas.auth_schema import Response_Access_And_Refresh_Token

from app.security.gerenciador_jwt import criar_access_token
from app.security.criador_strings import criar_string_aleatoria

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


def criar_access_and_refresh_token(entity_id: int) -> Response_Access_And_Refresh_Token:
    return Response_Access_And_Refresh_Token(
        access_token=criar_access_token(entity_id),
        refresh_token=criar_string_aleatoria(64)
    )