# Models
from modules.images.models.image import Image

# Libs
from sqlalchemy.exc import DatabaseError
from sqlalchemy.orm.query import Query


class AbstractImageManager:

    def get_active_images(self) -> Query:
        """ """
        return Image.query().filter((Image.is_active == True))

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
