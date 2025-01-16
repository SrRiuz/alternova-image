# Libs
from pydantic import BaseModel


class Schema(BaseModel):

    def to_representation(self) -> dict:
        return self.dict()
