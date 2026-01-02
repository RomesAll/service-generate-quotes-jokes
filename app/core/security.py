import uuid

def create_primary_key() -> bytes:
    return str(uuid.uuid4())