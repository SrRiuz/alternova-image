# Python
import io
import os
import base64

# Libs
from core.settings import LOCAL_STORAGE_DIR


def get_base64_from_file_name(file_name: str) -> str:
    """ """
    file_path = f"{LOCAL_STORAGE_DIR}/{file_name}"
    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"""We could not find any file named: '{file_name}'""",
        )

    with open(file_path, "rb") as file:
        file_content = file.read()
        return base64.b64encode(file_content).decode("utf-8")


def upload_file(file_bytes: io.BytesIO, file_name: str) -> None:
    """Upload a new file in to the local storage"""
    with open(f"{LOCAL_STORAGE_DIR}/{file_name}", "wb") as file:
        file.write(file_bytes.getbuffer())
        file.close()


def delete_file(file_name) -> None:
    """It is responsible for deleting a file in the storage folder"""
    os.remove(f"{LOCAL_STORAGE_DIR}/{file_name}")
