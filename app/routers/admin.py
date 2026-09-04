from fastapi import APIRouter, status, Depends

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.services.unidade_saude_service import service_criar_unidade_saude

from app.schemas.unidade_saude_schema import UnidadeSaude_Create

from app.services.auth_service import verificar_credencial_admin

admin_router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

@admin_router.post("/create-unidade-saude", status_code=status.HTTP_201_CREATED)
async def criar_unidade_saude(
    unidade_saude_create: UnidadeSaude_Create, 
    autorizado: bool = Depends(verificar_credencial_admin),
    db: Session = Depends(get_db)
):
    return service_criar_unidade_saude(db, unidade_saude_create)