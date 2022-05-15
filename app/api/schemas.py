"""Module for defining key schemas used within the REST API."""
import datetime

from typing import Optional, Union

import pydantic
import pydantic.main


class BaseSchema(pydantic.main.BaseModel):
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
class AnalystInputSchema(_AnalystBaseSchema):
    """Schema for representing Analyst input data model."""
    ...


class AnalystSchema(_AnalystBaseSchema, _AnalystPrimaryKeySchema):
    """Complete model representing an analyst."""


#: Type alias for covering possible date types
DateType = Union[datetime.date, datetime.datetime]


class _AssetPrimaryKeySchema(BaseSchema):
    """Mixin class providing primary key for Asset model."""
    asset_id: int = pydantic.Field(alias='id')


class _AssetBaseSchema(BaseSchema):
    """Model representing common attributes of an asset."""
    name: str
    description: Optional[str] = None
    inception_date: DateType  # TODO: check whether time part is required
    is_active: bool
    analyst_id: int


#: Define alias for more explicit meaning when exported for use in REST API.
class AssetInputSchema(_AssetBaseSchema):
    """Schema for representing asset input data model."""
    ...


class AssetSchema(_AssetBaseSchema, _AssetPrimaryKeySchema):
    """Complete model representing an asset."""
    analyst: AnalystSchema
