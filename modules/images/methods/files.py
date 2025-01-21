# Python
import uuid
import hashlib
import base64
import io
from typing import Tuple, Optional


def base64_to_bytes_io(base64_str: str) -> bytes:
    """Decodes a base64 string to bytes."""
    byte_data = base64.b64decode(base64_str)
    return io.BytesIO(byte_data)


def generate_hashed_name(file_name: str) -> Tuple[str, Optional[str]]:
    """Generates a random name for a file."""
    uuid4 = uuid.uuid4().__str__().encode()
    random_hash = hashlib.sha256(uuid4).hexdigest()
    if "." in file_name:
        file_split_name = file_name.split(".")
        file_format = file_split_name[1]
        return f"{random_hash}.{file_format}", file_format

    return random_hash, None
