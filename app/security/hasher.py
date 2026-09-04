from pwdlib import PasswordHash

password_hasher = PasswordHash.recommended()


def hashear_string(string: str) -> str:
    return password_hasher.hash(string)


def verificar_hash(string: str, string_hasheada: str) -> bool:
    try:
        return password_hasher.verify(string, string_hasheada)
    except Exception:
        return False