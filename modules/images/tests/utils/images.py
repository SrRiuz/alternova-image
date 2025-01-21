# Python
import base64


def get_base64_image() -> str:
    MEDIA_TEST_PATH = "modules/images/tests/media/test.png"
    with open(MEDIA_TEST_PATH, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()
