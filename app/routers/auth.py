from fastapi import APIRouter, status, Depends

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.services.unidade_saude_service import service_buscar_unidade_saude_by_nome_login
from app.services.auth_service import criar_access_and_refresh_token

from app.schemas.unidade_saude_schema import UnidadeSaude_Login
from app.schemas.auth_schema import Response_Access_And_Refresh_Token

auth_router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@auth_router.post("/login", status_code=status.HTTP_200_OK)
async def fazer_login(
    unidade_saude_login: UnidadeSaude_Login,
    db: Session = Depends(get_db)
) -> Response_Access_And_Refresh_Token:
    unidade_saude_id: int = service_buscar_unidade_saude_by_nome_login(db, unidade_saude_login)

    return criar_access_and_refresh_token(unidade_saude_id)