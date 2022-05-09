from typing import Type
from .base_repository import BaseRepository
from ..tables import AnalystModel
from ...api.schemas import AnalystSchema


class AnalystRepository(BaseRepository):
    @property
    def _table(self) -> Type[AnalystModel]:
        return AnalystModel

    @property
    def _schema(self) -> Type[AnalystSchema]:
        return AnalystSchema
