# Python
from pydantic import constr

# Libs
from core.schemas.schema import Schema
from core.settings import MEDIA_URL
from modules.images.constants import MAX_TITLE_CHARACTERS_SIZE


class ImageSchema(Schema):
    id: str
    name: str
    is_active: bool

    def to_representation(self) -> dict:
        representation = super().to_representation()
        return {**representation, "media_link": f"{MEDIA_URL}/{self.id}"}


class CreateImageSchema(Schema):

    name: constr(max_length=MAX_TITLE_CHARACTERS_SIZE)
    data: str
