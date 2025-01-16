# Python
import hashlib
import uuid

# Sqlalchemy
from sqlalchemy.orm import as_declarative, declared_attr
from sqlalchemy import Column, DateTime, func, Boolean, String
from sqlalchemy.inspection import inspect

# Libs
from core.db.session import session


@as_declarative()
class Model:
    id = Column(
        String(64),
        primary_key=True,
        unique=True,
        nullable=False,
        default=lambda: hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest(),
    )

    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    def to_dict(self):
        def model_to_dict(instance):
            return {c.key: getattr(instance, c.key) for c in inspect(instance).mapper.column_attrs}

        route_dict = model_to_dict(self)
        return route_dict

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    @classmethod
    def query(cls):
        return session.query(cls)
