from sqlalchemy import Column, Integer, String

from app.db.tables.base import BaseModel


class AnalystModel(BaseModel):
    __tablename__ = 'analysts'

    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String, nullable=False)
    company = Column(String, nullable=False)
