# Python
from http import HTTPStatus

# Libs
from modules.images.tests.utils.images import get_base64_image
from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


class TestRemoveImageBgRoute:

    def test_remove_image_bg(self):
        image_data = get_base64_image()
        image = client.post(
            "/v1/images",
            json={
                "name": "test.png",
                "data": image_data,
            },
        ).json()
        image_id = image["id"]

        response = client.post(f"/v1/images/rembg/{image_id}")
        assert response.status_code == HTTPStatus.CREATED

    def test_try_remove_image_bg_using_invalid_image_id(self):
        response = client.post("/v1/images/rembg/some_id")
        assert response.status_code == HTTPStatus.NOT_FOUND
