"""Module for defining key schemas used within the REST API."""
import datetime

from typing import Optional, Union
import pydantic


class BaseSchema(pydantic.BaseModel):
    """Base model class with desired common config."""
    class Config:
        """Common configuration."""
        orm_mode = True


class _AnalystPrimaryKeySchema(BaseSchema):
    """Primary key schema fragment for analyst models."""
    analyst_id: int = pydantic.Field(alias='id')


class _AnalystBaseSchema(BaseSchema):
    """Model representing an analyst which acts one or more assets."""
    name: str
    company: str


#: Define alias for more explicit meaning when exported for use in REST API.
AnalystInputSchema = _AnalystBaseSchema


class AnalystSchema(_AnalystPrimaryKeySchema, _AnalystBaseSchema):
    """Complete model representing an analyst."""


#: Type alias for covering possible date types
DateType = Union[datetime.date, datetime.datetime]


class _AssetPrimaryKeySchema(BaseSchema):
    asset_id: int = pydantic.Field(alias='id')


class _AssetBaseSchema(BaseSchema):
    """Model representing common attributes of an asset."""
    name: str
    description: Optional[str] = None
    inception_date: DateType  # TODO: check whether time part is required
    is_active: bool
    analyst_id: int


#: Define alias for more explicit meaning when exported for use in REST API.
AssetInputSchema = _AssetBaseSchema


class AssetSchema(_AssetPrimaryKeySchema, _AssetBaseSchema):
    """Complete model representing an asset."""
    analyst: AnalystSchema
