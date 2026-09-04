from jose import jwt
from datetime import datetime, timedelta, timezone

from app.core import JWT_SECRET_KEY

ALGORITHM = "HS256"

def criar_access_token(entity_id: int) -> str:
    agora = datetime.now(timezone.utc)

    payload = {
        "sub": str(entity_id),
        "type": "access",
        "iat": agora,
        "exp": agora + timedelta(minutes=15)
    }

    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=ALGORITHM)

def ler_access_token(token: str) -> dict[str, any]:
    return jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])