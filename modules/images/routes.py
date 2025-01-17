# Python
import base64
from typing import Literal
from http import HTTPStatus

# FastApi
import fastapi
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi.responses import StreamingResponse

# Models
from modules.images.models.image import Image

# Managers
from modules.images.manager.image import Images

# Schemas
from modules.images.schemas.image import ImageSchema, CreateImageSchema

# Libs
from utils.shortcuts import get_object_or_404
from core.pagination.pagination import Pagination
from modules.images.constants import ALLOWED_IMAGES_EXTENSIONS, PNG_FILE_EXTENSION, JPEG_FILE_EXTENSION, JPG_FILE_EXTENSION, WEBP_FILE_EXTENSION
from modules.images.methods.storage import upload_file, delete_file, get_base64_from_file_name
from modules.images.methods.convert import change_image_format
from modules.images.methods.files import base64_to_bytes_io, generate_hashed_name


router = fastapi.APIRouter(prefix="/v1/images")


@router.get(
    "",
    tags=["healthcheck"],
    summary="Obtains a list with the data of the active images.",
    responses={
        200: {
            "description": "Obtains a list with the data of the active images.",
            "content": {
                "application/json": {
                    "example": {
                        "total_count": 4,
                        "count": 4,
                        "next": None,
                        "previews": None,
                        "data": [
                            {
                                "id": "...",
                                "name": "...",
                                "is_active": False,
                            },
                        ],
                    }
                }
            },
        },
    },
)
async def get_images_list() -> JSONResponse:
    """Obtains a list with the data of the active images."""
    queryset = Images.objects.get_active_images()
    pagination = Pagination(queryset=queryset, page=0, schema=ImageSchema)
    return JSONResponse(pagination.get_paginated_response(), HTTPStatus.OK)


@router.get(
    "/{image_id}",
    tags=["healthcheck"],
    summary="Gets information about an image.",
    responses={
        200: {
            "description": "Gets information about an image.",
            "content": {
                "application/json": {
                    "example": {
                        "id": "...",
                        "name": "...",
                        "is_active": True,
                    }
                }
            },
        },
    },
)
async def get_image_from_id(image_id: str) -> JSONResponse:
    """Gets information about an image."""
    media = get_object_or_404(Image, id=image_id)
    data = ImageSchema.parse_obj(media.to_dict()).dict()
    return JSONResponse(data, status_code=HTTPStatus.OK)


@router.post(
    "",
    tags=["Image"],
    summary="Handles uploading new files to storage.",
    responses={
        200: {
            "description": "Handles uploading new files to storage.",
            "content": {
                "application/json": {
                    "example": {
                        "id": "...",
                        "name": "...",
                        "is_active": False,
                        "media_link": "...",
                    }
                }
            },
        },
    },
)
async def create_media_object(data: CreateImageSchema) -> JSONResponse:
    """Handles uploading new files to storage."""
    try:
        file_bytes = base64_to_bytes_io(data.data)
    except (base64.binascii.Error, ValueError):
        raise HTTPException(
            detail="Unable to decode file.",
            status_code=HTTPStatus.BAD_REQUEST,
        )

    file_name, file_format = generate_hashed_name(data.name)
    if file_format not in ALLOWED_IMAGES_EXTENSIONS:
        raise HTTPException(
            detail="Invalid file extension.",
            status_code=HTTPStatus.BAD_REQUEST,
        )

    upload_file(file_bytes, file_name)

    media = Images.objects.create(file_name=file_name)
    data = ImageSchema.parse_obj(media.to_dict()).dict()

    return JSONResponse(data, HTTPStatus.CREATED)


@router.delete(
    "/{image_id}",
    tags=["Media"],
    summary="Delete a file.",
    responses={
        200: {
            "description": "Remove an object from local storage.",
            "content": {"application/json": {"example": {}}},
        },
        404: {
            "description": "Error if the object id not exists",
            "content": {"application/json": {"example": {"detail": "Object not found"}}},
        },
    },
)
def delete_object(image_id: str) -> JSONResponse:
    """Remove an object from local storage."""
    media = get_object_or_404(Image, id=image_id)

    # Delete the file of the local storage
    delete_file(media.name)

    # Remove the database
    Images.objects.delete(id=media.id)

    return JSONResponse({}, HTTPStatus.OK)


@router.get(
    "/media/{image_id}",
    tags=["Media"],
    summary="It is responsible for obtaining a download link for an image.",
    responses={
        200: {
            "description": "It is responsible for obtaining a download link for an image..",
            "content": {"image/png": {"example": {}}},
        },
        404: {
            "description": "Error if the object id not exists",
            "content": {"application/json": {"example": {"detail": "Object not found"}}},
        },
    },
)
def get_image_static_url(image_id: str) -> StreamingResponse:
    """It is responsible for obtaining a download link for an image."""
    media = get_object_or_404(Image, id=image_id)
    _, extension = media.name.split(".")
    base64_file = get_base64_from_file_name(media.name)
    file_bytes = base64_to_bytes_io(base64_file)
    return StreamingResponse(file_bytes, media_type=f"image/{extension}")


@router.post(
    "/convert/{image_id}/{output_format}",
    tags=["Media"],
    summary="It is responsible for changing the format of an image.",
    responses={
        200: {
            "description": "It is responsible for changing the format of an image.",
            "content": {
                "application/json": {
                    "example": {
                        "id": "...",
                        "name": "...",
                        "is_active": False,
                        "media_link": "...",
                    },
                }
            },
        },
        404: {
            "description": "Error if the object id not exists",
            "content": {"application/json": {"example": {"detail": "Object not found"}}},
        },
    },
)
def image_change_format(
    image_id: str,
    output_format: Literal[
        PNG_FILE_EXTENSION,
        JPEG_FILE_EXTENSION,
        JPG_FILE_EXTENSION,
        WEBP_FILE_EXTENSION,
    ],
) -> JSONResponse:
    """It is responsible for changing the format of an image."""
    media = get_object_or_404(Image, id=image_id)
    _, format = media.name.split(".")

    if format == output_format:
        raise HTTPException(
            detail="The extension must be different from the current extension.",
            status_code=HTTPStatus.BAD_REQUEST,
        )

    base64_file = get_base64_from_file_name(media.name)
    file_bytes = base64_to_bytes_io(base64_file)

    file_name, _ = generate_hashed_name(f"{image_id}.{output_format}")
    new_format_bytes = change_image_format(file_bytes, output_format)

    upload_file(new_format_bytes, file_name)

    media = Images.objects.create(file_name=file_name)
    data = ImageSchema.parse_obj(media.to_dict()).dict()

    return JSONResponse(data, HTTPStatus.CREATED)
