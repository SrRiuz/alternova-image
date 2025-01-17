# Models
from sqlalchemy import Column, String
from core.db.models import Model


class Image(Model):
    __tablename__ = "image"
    name = Column(String(250), nullable=False)
