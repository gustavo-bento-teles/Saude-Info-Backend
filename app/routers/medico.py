from fastapi import APIRouter, status, Depends, Response

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.services.medico_service import service_criar_medico
from app.services.auth_service import obter_session_cookie

from app.schemas.medico_schema import Medico_Create

medico_router = APIRouter(
    prefix="/medico",
    tags=["Médico"]
)

@medico_router.post("/", status_code=status.HTTP_200_OK)
async def criar_medico(
    medico_create: Medico_Create,
    csrf_token: str,
    session_cookie = Depends(obter_session_cookie),
    db: Session = Depends(get_db)
):
    return service_criar_medico(db, medico_create, csrf_token, session_cookie)