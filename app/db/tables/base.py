"""Provides BaseModel class for defining SQLAlchemy ORM models."""
from sqlalchemy.ext.declarative import as_declarative, declared_attr

import re


@as_declarative()
class BaseModel:
    """Base model for defining SQL tables as ORM classes."""
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        """
        Defines the SQLAlchemy table name as the 
        lowercase representation of the class itself.
        """
        return re.sub('model$', '', cls.__name__.lower())