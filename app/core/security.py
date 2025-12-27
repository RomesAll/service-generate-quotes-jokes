import uuid

def check_exists_primary_key(key: bytes) -> bool:
    pass

def create_primary_key() -> bytes:
    for i in range(10):
        if not check_exists_primary_key('key'):
            return str(uuid.uuid4())
    return None