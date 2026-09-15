from fastapi import HTTPException, status
from fastapi.responses import JSONResponse

class SessaoInvalidaException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sessão inválida"
        )


async def sessao_invalida_handler(request, exc):
    response = JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )
    
    response.delete_cookie("session", path="/")
    response.delete_cookie("csrf_token", path="/")
    
    return response