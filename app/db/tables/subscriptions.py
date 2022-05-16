"""Provides SQLAlchemy ORM model defining a subscription."""
from sqlalchemy import Column, Integer, String

from app.db.tables.base import BaseModel


class SubscriptionModel(BaseModel):
    """ORM model defining an subscription."""

    __tablename__ = "subscriptions"

    id = Column(Integer, index=True, primary_key=True, unique=True)
    email = Column(String, index=True, nullable=False)
    topic = Column(String, nullable=False)
