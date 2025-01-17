# Models
from modules.images.models.image import Image

# Libs
from sqlalchemy.exc import DatabaseError
from sqlalchemy.orm.query import Query


class AbstractImageManager:

    def get_active_images(self) -> Query:
        """Gets a list of active images."""
        return Image.query().filter((Image.is_active == True))

    def delete(self, id: str) -> None:
        """
        It is responsible for deleting the registration
        of an image.
        """
        try:
            session = Image.query().session
            media = Image.query().filter((Image.id == id)).first()
            media.is_active = False
            session.commit()
            session.close()
        except DatabaseError as e:
            session.rollback()
            session.close()
            raise e

    def create(self, file_name: str) -> Image:
        """It allows creating a new multimedia file."""
        try:
            session = Image.query().session
            media = Image(name=file_name)
            session.add(media)
            session.commit()
            return media
        except DatabaseError as e:
            session.rollback()
            session.close()
            raise e


class Images:
    objects = AbstractImageManager()
