import hashlib

from urllib.parse import quote

from typing import AnyStr

def encrypt_password(s: str) -> AnyStr:
    sha = hashlib.sha512()
    sha.update(quote(str(s)).encode("utf-8"))
    return sha.hexdigest()
    
