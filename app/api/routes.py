import os

from typing import Any, List

from fastapi import FastAPI
from fastapi_async_sqlalchemy import SQLAlchemyMiddleware, db

from starlette import status
from mangum import Mangum

# NOTE: use relative imports to be compatible with uvicorn without needing a python package
from .schemas import AnalystInputSchema, AssetInputSchema, AssetSchema, AnalystSchema
from ..db.tables import AssetModel, AnalystModel
from ..db.repositories import AssetRepository, AnalystRepository
from ..db.utils import setup_database

#: Defines the database connection URL, defaulting to local SQLite DB
sqlalchemy_connection_string: str = \
    os.environ.get('SQLALCHEMY_DATABASE_CONNECTION_URI') or 'sqlite+aiosqlite:///db.sqlite'  # noqa: E501

# TODO: enabled in-memory database support (unable to create tables using sync + async drivers)
setup_database(sqlalchemy_connection_string)

app = FastAPI(title="Icy Morning REST API")

app.add_middleware(SQLAlchemyMiddleware, db_url=sqlalchemy_connection_string)

api_prefix = '/api/v1'

assets_repo = AssetRepository()
analysts_repo = AnalystRepository()


@app.get(f'{api_prefix}/assets', response_model=List[AssetSchema])
async def get_assets():
    """Retrieves all assets."""
    assets: List[AssetModel] = await db.session.query(AssetModel).all()
    return [AssetSchema.from_orm(asset) for asset in assets]


@app.post(f'{api_prefix}/assets',
          status_code=status.HTTP_201_CREATED,
          response_model=AssetSchema)
async def create_asset(payload: AssetSchema):
    """Create a new asset."""
    asset = await assets_repo.create(payload)
    return asset


@app.get(f'{api_prefix}/assets/{{asset_id}}', response_model=AssetSchema)
async def read_asset(asset_id: int):
    """Retrieve data on a specific asset given by `asset_id`."""
    asset = await assets_repo.read(asset_id)
    return asset


@app.put(f'{api_prefix}/assets/{{asset_id}}', response_model=AssetSchema)
async def update_asset(asset_id: int, payload: AssetInputSchema):
    """Update information on asset given by `asset_id`."""
    asset = await assets_repo.update(asset_id, payload)
    return asset


@app.delete(f'{api_prefix}/assets/{{asset_id}}', response_model=AssetSchema)
async def delete_asset(asset_id: int):
    """Delete asset from database."""
    asset = await assets_repo.delete(asset_id)
    return asset


@app.get(f'{api_prefix}/analysts', response_model=List[AnalystSchema])
async def get_analysts():
    """Retrieve list of analysts."""
    analysts: List[AnalystModel] = await db.session.query(AnalystModel).all()
    return [AnalystSchema(analyst) for analyst in analysts]


@app.post(f'{api_prefix}/analysts',
          status_code=status.HTTP_201_CREATED,
          response_model=AnalystSchema)
async def create_analyst(payload: AnalystInputSchema):
    """Add a new analyst to the database."""
    analyst = await analysts_repo.create(payload)
    return analyst


@app.get(f'{api_prefix}/analysts/{{analyst_id}}', response_model=AnalystSchema)
async def get_analyst_by_id(analyst_id: int):
    """Retrieve data on a specific analyst given by `analyst_id`."""
    analyst = await analysts_repo.read(analyst_id)
    return analyst


@app.put(f'{api_prefix}/analysts/{{analyst_id}}', response_model=AnalystSchema)
async def update_analyst(analyst_id: int, payload: AnalystSchema):
    """Update analyst information.


    ## Notes

    The asset information must be complete - partial information update is not supported.    
    """
    analyst = await analysts_repo.update(analyst_id, payload)
    return analyst


@app.delete(f'{api_prefix}/analysts/{{analyst_id}}', response_model=AnalystSchema)
async def delete_analyst(analyst_id: int):
    """Delete analyst from database."""
    analyst = await analysts_repo.delete(analyst_id)
    return analyst



@app.post(f'{api_prefix}/assets/subscription')
async def subscribe_user_to_asset_events(payload: Any):
    ...  # TODO: implement


@app.delete(f'{api_prefix}/subscriptions/{{subscription_id}}')
async def unsubscribe_user_from_asset_events(payload: Any):
    ...  # TODO: implement


#: Wrapper for AWS API Gateway
handler: Mangum = Mangum(app)
