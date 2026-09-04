import secrets
import string

alfabeto = string.ascii_letters + string.digits + "!@#$%^&*"

def criar_string_aleatoria(n_range: int) -> str:
    return "".join(
        secrets.choice(alfabeto)
        for _ in range(n_range)
    )