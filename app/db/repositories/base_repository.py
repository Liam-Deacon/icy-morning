"""
Notes
-----
Modified from https://rogulski.it/blog/sqlalchemy-14-async-orm-with-fastapi/
"""
import abc
from typing import Generic, TypeVar, Type

from sqlalchemy.ext.asyncio import AsyncSession

from ..tables.base import BaseModel
from ...api.errors import NotFoundException, ConflictException
from ...api.schemas import BaseSchema

IN_SCHEMA = TypeVar("IN_SCHEMA", bound=BaseSchema)
SCHEMA = TypeVar("SCHEMA", bound=BaseSchema)
TABLE = TypeVar("TABLE", bound=BaseModel)


class BaseRepository(Generic[IN_SCHEMA, SCHEMA, TABLE], metaclass=abc.ABCMeta):
    """Abstract base class for implementing the repository pattern."""

    def __init__(self, db_session: AsyncSession, **kwargs) -> None:
        """Initialise repository instance with `db_session`.

        Parameters
        ----------
        db_session: AsyncSession
            SQLAlchemy session object in which to perform database transactions. 
        """
        if not isinstance(db_session, AsyncSession):
            raise TypeError(f'db_session must be an AsyncSession object, not ({type(db_session)})')  # noqa: E501
        self._db_session: AsyncSession = db_session
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
        entry = await self._db_session.get(self._table, entry_id)
        if not entry:
            raise NotFoundException(
                f"{self._table.__name__}<id:{entry_id}> does not exist"
            )
        return entry

    async def create(self, input_schema: IN_SCHEMA) -> SCHEMA:
        """Creates a new database row entry using `in_schema`."""
        entry = self._table(**input_schema.dict(alias=True))
        self._db_session.add(entry)
        await self._db_session.commit()
        return self._schema.from_orm(entry)

    async def read(self, entry_id: int) -> SCHEMA:
        """Retrieve entry from database as REST API schema object."""
        entry = await self._get_by_id(entry_id)
        return self._schema.from_orm(entry)

    async def update(self, entry_id: int, schema: SCHEMA) -> SCHEMA:
        """Update entry in database from input schema."""
        schema_id = getattr(schema, 'id', None)
        if entry_id != schema_id:
            raise ConflictException(f"Entity primary key does not match route ({schema_id} vs {entry_id})")
        entry = self._table(**schema.dict(alias=True))
        self._db_session.merge(entry, load=True)
        await self._db_session.commit()
        return self._schema.from_orm(entry)

    async def delete(self, entry_id: int) -> SCHEMA:
        """Remove entry from database."""
        entry = await self._get_by_id(entry_id)
        await self._db_session.delete(entry)
        return self._schema.from_orm(entry)
