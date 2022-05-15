"""Provides SQLAlchemy ORM model defining an asset."""
import datetime

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship

from app.db.tables.base import BaseModel
from app.db.tables.analysts import AnalystModel


class AssetModel(BaseModel):
    """ORM model defining an asset."""
    __tablename__ = 'assets'

    id = Column(Integer, index=True, primary_key=True, unique=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    inception_date = Column(Date, index=True, default=datetime.date.today)
    analyst_id = Column(Integer, ForeignKey("analysts.id"))
    is_active = Column(Boolean)

    # analyst = relationship(AnalystModel)
