# Python
from http import HTTPStatus

# Libs
from modules.images.tests.utils.images import get_base64_image
from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


class TestImageRoute:

    def test_retrieve_images_list(self):
        response = client.get("/v1/images")
        assert response.status_code == HTTPStatus.OK

    def test_upload_image_object(self):
        image_data = get_base64_image()
        response = client.post(
            "/v1/images",
            json={
                "name": "test.png",
                "data": image_data,
            },
        )

        assert response.status_code == HTTPStatus.CREATED

    def test_get_image_download_link(self):
        image_data = get_base64_image()
        image = client.post(
            "/v1/images",
            json={
                "name": "test.png",
                "data": image_data,
            },
        ).json()

        image_id = image["id"]
        response = client.get(f"/v1/images/media/{image_id}")
        assert response.status_code == HTTPStatus.OK

    def test_upload_image_and_retrieve_object(self):
        image_data = get_base64_image()
        image = client.post(
            "/v1/images",
            json={"name": "test.png", "data": image_data},
        ).json()

        image_id = image["id"]

        response = client.get(f"/v1/images/{image_id}")
        assert response.status_code == HTTPStatus.OK

    def test_upload_image_and_delete_object(self):
        image_data = get_base64_image()
        image = client.post(
            "/v1/images",
            json={"name": "test.png", "data": image_data},
        ).json()

        image_id = image["id"]

        response = client.delete(f"/v1/images/{image_id}")
        assert response.status_code == HTTPStatus.OK

    def test_try_get_image_download_link_whith_invalid_image_id(self):
        response = client.get(f"/v1/images/media/some_id")
        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_try_retrieve_object_whith_invalid_image_id(self):
        response = client.get("/v1/images/some_id")
        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_try_delete_object_whith_invalid_image_id(self):
        response = client.delete("/v1/images/some_id")
        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_try_upload_image_object_whith_wrong_base64_data(self):
        response = client.post(
            "/v1/images",
            json={"name": "test.png", "data": "Some base64."},
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json() == {"detail": "Unable to decode file."}

    def test_try_upload_image_object_whith_invalid_image_extension(self):
        response = client.post(
            "/v1/images",
            json={"name": "test.exe", "data": "test"},
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json() == {"detail": "Invalid file extension."}
