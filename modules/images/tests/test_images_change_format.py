# Python
from http import HTTPStatus

# Libs
from modules.images.tests.utils.images import get_base64_image
from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


class TestImageRoute:

    def test_change_image_format_from_png_to_jepg(self):
        image_data = get_base64_image()
        image = client.post(
            "/v1/images",
            json={
                "name": "test.png",
                "data": image_data,
            },
        ).json()
        image_id = image["id"]

        response = client.post(f"/v1/images/convert/{image_id}/jepg")

    def test_change_image_format_from_png_to_jpg(self):
        image_data = get_base64_image()
        image = client.post(
            "/v1/images",
            json={
                "name": "test.png",
                "data": image_data,
            },
        ).json()
        image_id = image["id"]

        response = client.post(f"/v1/images/convert/{image_id}/jpg")
        assert response.status_code == HTTPStatus.CREATED

    def test_change_image_format_from_png_to_webp(self):
        image_data = get_base64_image()
        image = client.post(
            "/v1/images",
            json={
                "name": "test.png",
                "data": image_data,
            },
        ).json()
        image_id = image["id"]

        response = client.post(f"/v1/images/convert/{image_id}/webp")
        assert response.status_code == HTTPStatus.CREATED

    def test_try_change_image_format_with_invalid_image_id(self):
        response = client.post(f"/v1/images/convert/some_id/png")
        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_try_change_image_format_with_the_same_format(self):
        image_data = get_base64_image()
        image = client.post(
            "/v1/images",
            json={
                "name": "test.png",
                "data": image_data,
            },
        ).json()
        image_id = image["id"]

        response = client.post(f"/v1/images/convert/{image_id}/png")
        assert response.status_code == HTTPStatus.BAD_REQUEST
