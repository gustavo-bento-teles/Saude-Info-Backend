from fastapi import APIRouter, status, Depends

from app.schemas.unidade_saude import UnidadeSaude_Create

from app.security.autenticacao_admin import verificar_credencial_admin
from app.security.criador_senhas import criar_senha_aleatoria
from app.security.hasher import hashear_senha

admin_router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

@admin_router.post("/create-unidade-saude", status_code=status.HTTP_201_CREATED)
async def criar_unidade_saude(
    unidade_medica: UnidadeSaude_Create, 
    autorizado: bool = Depends(verificar_credencial_admin)
):  
    return unidade_medica