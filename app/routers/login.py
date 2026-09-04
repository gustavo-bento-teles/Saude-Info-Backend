from fastapi import APIRouter, status, Depends

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.services.unidade_saude_service import buscar_unidade_saude_nome_login_service

from app.schemas.unidade_saude_schema import UnidadeSaude_Login

login_router = APIRouter(
    prefix="/login",
    tags=["Login"]
)

@login_router.post("/", status_code=status.HTTP_200_OK)
async def fazer_login(
    unidade_saude_login: UnidadeSaude_Login,
    db: Session = Depends(get_db)
):
    return buscar_unidade_saude_nome_login_service(db, unidade_saude_login)