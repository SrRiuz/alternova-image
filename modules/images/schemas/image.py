# Libs
from core.schemas.schema import Schema
from modules.images.constants import MAX_TITLE_CHARACTERS_SIZE
from pydantic import constr


class ImageSchema(Schema):
    id: str
    name: str
    is_active: bool


class CreateImageSchema(Schema):

    name: constr(max_length=MAX_TITLE_CHARACTERS_SIZE)
    data: str
