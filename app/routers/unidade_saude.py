from fastapi import APIRouter, status, Depends, Response

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.services.unidade_saude_service import service_criar_unidade_saude, service_listar_unidades_saude, service_buscar_unidade_saude_by_id, service_atualizar_dados_unidade_saude
from app.services.auth_service import service_get_current_unidade_saude

from app.schemas.unidade_saude_schema import UnidadeSaude_Create, UnidadeSaude_Update

from app.services.auth_service import verificar_credencial_admin, obter_csrf_token, obter_session_cookie

unidade_saude_router = APIRouter(
    prefix="/unidade-saude",
    tags=["Unidade de Saúde"]
)

@unidade_saude_router.get("/", status_code=status.HTTP_200_OK)
async def obter_unidades_saude(db: Session = Depends(get_db)):
    return service_listar_unidades_saude(db)

@unidade_saude_router.get("/{unidade_id}", status_code=status.HTTP_200_OK)
async def obter_unidade_saude(unidade_id: int, db: Session = Depends(get_db)):
    return service_buscar_unidade_saude_by_id(db, unidade_id)

@unidade_saude_router.post("/", status_code=status.HTTP_201_CREATED)
async def criar_unidade_saude(
    unidade_saude_create: UnidadeSaude_Create, 
    autorizado: bool = Depends(verificar_credencial_admin),
    db: Session = Depends(get_db)
):
    return service_criar_unidade_saude(db, unidade_saude_create)


@unidade_saude_router.patch("/", status_code=status.HTTP_200_OK)
async def atualizar_dados_unidade_saude(
    dados_unidade_saude: UnidadeSaude_Update,
    csrf_token: str | None = Depends(obter_csrf_token),
    session_token: str | None = Depends(obter_session_cookie),
    db: Session = Depends(get_db)
):
    unidade_saude_id = service_get_current_unidade_saude(db, csrf_token, session_token)
    return service_atualizar_dados_unidade_saude(db, unidade_saude_id, dados_unidade_saude)