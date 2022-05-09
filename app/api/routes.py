import os

from typing import List

from fastapi import FastAPI
from fastapi_async_sqlalchemy import SQLAlchemyMiddleware, db

from starlette import status

# NOTE: use relative imports to be compatible with uvicorn without needing a python package
from .schemas import AnalystInputSchema, AssetInputSchema, AssetSchema, AnalystSchema
from ..db.tables import AssetModel, AnalystModel
from ..db.repositories import AssetRepository, AnalystRepository

#: Defines the database connection URL, defaulting to in-memory SQLite DB
sqlalchemy_connection_string: str = \
    os.environ.get('SQLALCHEMY_DATABASE_CONNECTION_URI') or 'sqlite+aiosqlite://'  # noqa: E501

app = FastAPI()

app.add_middleware(SQLAlchemyMiddleware, db_url=sqlalchemy_connection_string)


api_prefix = '/api/v1'

assets_repo = AssetRepository(db)
analysts_repo = AnalystRepository(db)


@app.get(f'{api_prefix}/assets')
async def get_assets():
    assets: List[AssetModel] = await db.session.query(AssetModel).all()
    return [AssetSchema.from_orm(asset) for asset in assets]


@app.post(f'{api_prefix}/assets', status_code=status.HTTP_201_CREATED)
async def create_asset(payload: AssetSchema):
    return await assets_repo.create(payload)


@app.get(f'{api_prefix}/assets/{{asset_id}}')
async def read_asset(asset_id: int):
    return await assets_repo.read(asset_id)


@app.put(f'{api_prefix}/assets/{{asset_id}}')
async def update_asset(asset_id: int, payload: AssetInputSchema):
    return await assets_repo.update(asset_id, payload)


@app.delete(f'{api_prefix}/assets/{{asset_id}}')
async def delete_asset(asset_id: int):
    return await assets_repo.delete(asset_id)


@app.get(f'{api_prefix}/analysts')
async def get_analysts():
    analysts: List[AnalystModel] = await db.session.query(AnalystModel).all()
    return [AnalystSchema(analyst) for analyst in analysts]


@app.post(f'{api_prefix}/analysts', status_code=status.HTTP_201_CREATED)
async def create_analyst(payload: AnalystInputSchema):
    return await analysts_repo.create(payload)


@app.get(f'{api_prefix}/analysts/{{analyst_id}}')
async def get_analyst_by_id(analyst_id: int):
    return await analysts_repo.read(analyst_id) 


@app.put(f'{api_prefix}/analysts/{{analyst_id}}')
async def update_analyst(analyst_id: int, payload: AnalystSchema):
    return await analysts_repo.update(analyst_id, payload)


@app.delete(f'{api_prefix}/analysts/{{analyst_id}}')
async def delete_analyst(analyst_id: int):
    return await analysts_repo.delete(analyst_id)
