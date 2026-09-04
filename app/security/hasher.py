from pwdlib import PasswordHash

password_hasher = PasswordHash.recommended()

def hashear_string(string: str) -> str:
    return password_hasher.hash(string)


def verficicar_hash(string: str, string_hasheada: str):
    try:
        if password_hasher.verify(string, string_hasheada):
            return True
        return False

    except Exception as e:
        pass