"""Defines `AnalystRepository` class for retrieving analyst data from database."""
from typing import Type
from .base_repository import BaseRepository
from ..tables import AnalystModel
from ...api.schemas import AnalystSchema


class AnalystRepository(BaseRepository):
    """Repository for interacting with analyst data layer."""

    @property
    def _table(self) -> Type[AnalystModel]:
        return AnalystModel

    @property
    def _schema(self) -> Type[AnalystSchema]:
        return AnalystSchema
