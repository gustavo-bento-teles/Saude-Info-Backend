from fastapi import APIRouter, status, Depends
from app.schemas.unidade_saude import UnidadeMedica_Create

from app.security.autenticacao_admin import verificar_credencial_admin

admin_router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

@admin_router.post("/create-unidade-medica", status_code=status.HTTP_201_CREATED)
async def criar_unidade_medica(
    unidade_medica: UnidadeMedica_Create, 
    autorizado: bool = Depends(verificar_credencial_admin)
):
    return unidade_medica