# Python
from io import BytesIO

# Libs
from PIL import Image


def remove_bg_from_image(file_bytes: BytesIO, format: str) -> BytesIO:
    """
    This method is responsible for removing the
    background of an image.
    """
    from rembg import remove

    output_bytes = BytesIO()
    image = Image.open(file_bytes)
    image = remove(image)

    image.save(output_bytes, format=format.upper())
    output_bytes.seek(0)

    return output_bytes
