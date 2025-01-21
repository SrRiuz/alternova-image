# Python
from io import BytesIO

# Libs
from PIL import Image
from modules.images.constants import JPEG_FILE_EXTENSION, JPG_FILE_EXTENSION


def change_image_format(file_bytes: BytesIO, out_format: str) -> BytesIO:
    """It is responsible for changing the format of an image."""
    if out_format == JPG_FILE_EXTENSION:
        out_format = JPEG_FILE_EXTENSION

    image = Image.open(file_bytes)

    output_io = BytesIO()
    image.convert("RGB").save(output_io, format=out_format.upper())
    return output_io
