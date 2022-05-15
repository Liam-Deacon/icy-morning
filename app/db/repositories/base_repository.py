"""
Notes
-----
Modified from https://rogulski.it/blog/sqlalchemy-14-async-orm-with-fastapi/
"""
import abc
from typing import Generic, TypeVar, Type

from fastapi_async_sqlalchemy import db
from fastapi_async_sqlalchemy.middleware import DBSession
from sqlalchemy.ext.asyncio import AsyncSession

from ..tables.base import BaseModel
from ...api.errors import NotFoundException, ConflictException
from ...api.schemas import BaseSchema

IN_SCHEMA = TypeVar("IN_SCHEMA", bound=BaseSchema)
SCHEMA = TypeVar("SCHEMA", bound=BaseSchema)
TABLE = TypeVar("TABLE", bound=BaseModel)


class BaseRepository(Generic[IN_SCHEMA, SCHEMA, TABLE], metaclass=abc.ABCMeta):
    """Abstract base class for implementing the repository pattern."""

    def __init__(self, **kwargs) -> None:
        """Initialise repository instance."""
        self.__dict__.update(**kwargs)

    @property
    @abc.abstractmethod
    def _table(self) -> Type[TABLE]:
        ...

    @property
    @abc.abstractmethod
    def _schema(self) -> Type[SCHEMA]:
        ...

    async def _get_by_id(self, entry_id: int) -> SCHEMA:
        entry = await db.session.execute(self._table, entry_id)
        if not entry:
            raise NotFoundException(
                f"{self._table.__name__}<id:{entry_id}> does not exist"
            )
        return entry

    async def create(self, input_schema: IN_SCHEMA) -> SCHEMA:
        """Creates a new database row entry using `in_schema`."""
        entry = self._table(**input_schema.dict())
        async with db():
            db.session.add(entry)
            await db.session.commit()
            return self._schema.from_orm(entry)

    async def read(self, entry_id: int) -> SCHEMA:
        """Retrieve entry from database as REST API schema object."""
        async with db():
            entry = await self._get_by_id(entry_id)
            return self._schema.from_orm(entry)

    async def update(self, entry_id: int, schema: SCHEMA) -> SCHEMA:
        """Update entry in database from input schema."""
        schema_id = getattr(schema, 'id', None)
        if entry_id != schema_id:
            raise ConflictException(f"Entity primary key does not match route ({schema_id} vs {entry_id})")
        entry = self._table(**schema.dict(alias=True))
        async with db():
            db.session.merge(entry, load=True)
            await db.session.commit()
            return self._schema.from_orm(entry)

    async def delete(self, entry_id: int) -> SCHEMA:
        """Remove entry from database."""
        async with db():
            entry = await self._get_by_id(entry_id)
            await db.session.delete(entry)
            return self._schema.from_orm(entry)
