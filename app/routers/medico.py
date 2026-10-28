from fastapi import APIRouter, status, Depends, Body

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.services.medico_service import service_criar_medico, service_deletar_medico, service_atualizar_status_medico
from app.services.auth_service import obter_session_cookie, obter_csrf_token

from app.schemas.medico_schema import Medico_Create

medico_router = APIRouter(
    prefix="/medico",
    tags=["Médico"]
)

@medico_router.post("/", status_code=status.HTTP_200_OK)
async def criar_medico(
    medico_create: Medico_Create,
    csrf_token: str | None = Depends(obter_csrf_token),
    session_cookie = Depends(obter_session_cookie),
    db: Session = Depends(get_db)
):
    return service_criar_medico(db, medico_create, csrf_token, session_cookie)

@medico_router.patch("/", status_code=status.HTTP_200_OK)
async def atualizar_status_medico(
    medico_id: int = Body(..., embed=True),
    status_medico: bool = Body(..., embed=True),
    csrf_token: str | None = Depends(obter_csrf_token),
    session_cookie: str | None = Depends(obter_session_cookie),
    db: Session = Depends(get_db)
):
    return service_atualizar_status_medico(db, medico_id, status_medico, csrf_token, session_cookie)

@medico_router.delete("/{medico_id}", status_code=status.HTTP_200_OK)
async def deletar_medico(
    medico_id: int,
    csrf_token: str | None = Depends(obter_csrf_token),
    session_cookie: str | None = Depends(obter_session_cookie),
    db: Session = Depends(get_db)
):
    return service_deletar_medico(db, medico_id, csrf_token, session_cookie)