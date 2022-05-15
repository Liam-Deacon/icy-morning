"""
Notes
-----
Modified from https://rogulski.it/blog/sqlalchemy-14-async-orm-with-fastapi/
"""
import abc
from typing import Generic, List, TypeVar, Type

from fastapi_async_sqlalchemy import db

from ..tables.base import BaseModel
from ...api.errors import NotFoundException
from ...api.schemas import BaseSchema

InSchema = TypeVar("InSchema", bound=BaseSchema)
Schema = TypeVar("Schema", bound=BaseSchema)
Table = TypeVar("Table", bound=BaseModel)


class BaseRepository(Generic[InSchema, Schema, Table], metaclass=abc.ABCMeta):
    """Abstract base class for implementing the repository pattern."""

    def __init__(self, **kwargs) -> None:
        """Initialise repository instance."""
        self.__dict__.update(**kwargs)

    @property
    @abc.abstractmethod
    def _table(self) -> Type[Table]:
        ...

    @property
    @abc.abstractmethod
    def _schema(self) -> Type[Schema]:
        ...

    async def fetch_all(self) -> List[Schema]:
        """Retrieve all rows for table within database."""
        objs = await db.session.execute(f"""SELECT * FROM {self._table.__tablename__};""")
        return [dict(row) for row in objs]

    async def _get_by_id(self, entry_id: int) -> Schema:
        entry = await db.session.get(self._table, entry_id)
        if not entry:
            raise NotFoundException(
                f"{self._table.__name__}<id:{entry_id}> does not exist"
            )
        return entry

    def _get_pkey_col(self) -> str:
        return getattr(self, 'id', 'id')

    async def create(self, input_schema: InSchema) -> Schema:
        """Creates a new database row entry using `InSchema`."""
        entry = self._table(**input_schema.dict())
        async with db():
            db.session.add(entry)
            await db.session.flush()
            data = self._schema.from_orm(entry)
            await db.session.commit()
            return data

    async def read(self, entry_id: int) -> Schema:
        """Retrieve entry from database as REST API schema object."""
        async with db():
            entry = await self._get_by_id(entry_id)
            return self._schema.from_orm(entry)

    async def update(self, entry_id: int, schema: Schema | dict) -> Schema:
        """Update entry in database from input schema."""
        schema_dict = schema if isinstance(schema, dict) else schema.dict(by_alias=True)
        async with db():
            _old_entry = await self._get_by_id(entry_id)
            pkey = self._get_pkey_col()
            entry = self._table(**{**schema_dict, **{pkey: getattr(_old_entry, pkey, entry_id)}})
            await db.session.merge(entry)
            await db.session.commit()
            return self._schema.from_orm(entry)

    async def delete(self, entry_id: int) -> Schema:
        """Remove entry from database."""
        async with db():
            entry = await self._get_by_id(entry_id)
            await db.session.delete(entry)
            await db.session.commit()
            return self._schema.from_orm(entry)
