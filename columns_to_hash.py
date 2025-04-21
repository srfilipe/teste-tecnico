from hashlib import sha256

def hashid(columns_to_hash: str) -> str:
    return sha256(columns_to_hash.encode('utf-8')).hexdigest()