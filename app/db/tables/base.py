"""Provides BaseModel class for defining SQLAlchemy ORM models."""
import re

from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class BaseModel:
    """Base model for defining SQL tables as ORM classes."""

    __name__: str

    @declared_attr
    @classmethod
    def __tablename__(cls) -> str:  # noqa: N805,E0213
        """Defines the SQLAlchemy table name as the lowercase representation of the class itself."""
        return re.sub("model$", "", cls.__name__.lower())
