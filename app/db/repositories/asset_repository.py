"""Provides `AssetRepository` class to abstract data operations."""
from typing import Type
from .base_repository import BaseRepository
from ..tables import AssetModel
from ...api.schemas import AssetSchema


class AssetRepository(BaseRepository):
    """Data repository for interacting with Assets."""

    @property
    def _table(self) -> Type[AssetModel]:
        return AssetModel

    @property
    def _schema(self) -> Type[AssetSchema]:
        return AssetSchema
