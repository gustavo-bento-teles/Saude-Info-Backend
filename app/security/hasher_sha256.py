import hashlib

def hashear_sha256(string: str):
    return hashlib.sha256(
        string.encode()
    ).hexdigest()