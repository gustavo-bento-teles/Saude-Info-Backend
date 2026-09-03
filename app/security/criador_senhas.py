import secrets
import string

alfabeto = string.ascii_letters + string.digits + "!@#$%^&*"

def criar_senha_aleatoria() -> str:
    return "".join(
        secrets.choice(alfabeto)
        for _ in range(24)
    )