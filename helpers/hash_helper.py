from constants.hashing_constants import HashMethod
import hashlib


def get_hash_string(string=None,hash_method = HashMethod.MD5):
    if string:
        if hash_method==HashMethod.MD5:
            return hashlib.md5(string.encode("utf-8")).hexdigest()
        
        if hash_method is HashMethod.SHA256:
            return hashlib.sha256(string.encode("utf-8")).hexdigest()
    
    return None