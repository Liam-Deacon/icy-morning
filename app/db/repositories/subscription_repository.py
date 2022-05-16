"""Provides `SubscriptionRepository` class to abstract data operations."""
from typing import Type
from .base_repository import BaseRepository
from ..tables import SubscriptionModel
from ...api.schemas import SubscriptionSchema


class SubscriptionRepository(BaseRepository):
    """Data repository for interacting with Subscriptions."""

    @property
    def _table(self) -> Type[SubscriptionModel]:
        return SubscriptionModel

    @property
    def _schema(self) -> Type[SubscriptionSchema]:
        return SubscriptionSchema
