# Python
import io
import os

# Libs
from core.settings import LOCAL_STORAGE_DIR


def upload_file(file_bytes: io.BytesIO, file_name: str) -> None:
    """Upload a new file in to the local storage"""
    with open(f"{LOCAL_STORAGE_DIR}/{file_name}", "wb") as file:
        file.write(file_bytes.getbuffer())
        file.close()


def delete_file(file_name) -> None:
    """It is responsible for deleting a file in the storage folder"""
    os.remove(f"{LOCAL_STORAGE_DIR}/{file_name}")
