"""Defines routes for v1 API."""
from typing import Any, List

from fastapi import APIRouter

from starlette import status

# NOTE: use relative imports to be compatible with uvicorn without needing a python package
from app.api.schemas import AnalystInputSchema, AssetInputSchema, AssetSchema, AnalystSchema
from app.db.tables import AssetModel, AnalystModel
from app.db.repositories import AssetRepository, AnalystRepository

API_PREFIX = '/api/v1'

assets_repo = AssetRepository()
analysts_repo = AnalystRepository()

api_v1_router = APIRouter(prefix=API_PREFIX)


@api_v1_router.get('/assets', response_model=List[AssetSchema])
async def get_assets():
    """Retrieve all assets."""
    assets: List[AssetModel] = await assets_repo.fetch_all()
    return [AssetSchema.from_orm(asset) for asset in assets]


@api_v1_router.post('/assets',
                    status_code=status.HTTP_201_CREATED,
                    response_model=AssetSchema)
async def create_asset(payload: AssetSchema):
    """Create a new asset."""
    asset = await assets_repo.create(payload)
    return asset


@api_v1_router.get('/assets/{asset_id}', response_model=AssetSchema)
async def read_asset(asset_id: int):
    """Retrieve data on a specific asset given by `asset_id`."""
    asset = await assets_repo.read(asset_id)
    return asset


@api_v1_router.put('/assets/{asset_id}', response_model=AssetSchema)
async def update_asset(asset_id: int, payload: AssetInputSchema):
    """Update information on asset given by `asset_id`."""
    asset = await assets_repo.update(asset_id, payload)
    return asset


@api_v1_router.delete('/assets/{asset_id}', response_model=AssetSchema)
async def delete_asset(asset_id: int):
    """Delete asset from database."""
    asset = await assets_repo.delete(asset_id)
    return asset


@api_v1_router.get('/analysts', response_model=List[AnalystSchema])
async def get_analysts():
    """Retrieve list of analysts."""
    analysts: List[AnalystModel] = await analysts_repo.fetch_all()
    return [AnalystSchema(**analyst) for analyst in analysts]


@api_v1_router.post('/analysts',
                    status_code=status.HTTP_201_CREATED,
                    response_model=AnalystSchema)
async def create_analyst(payload: AnalystInputSchema):
    """Add a new analyst to the database."""
    analyst = await analysts_repo.create(payload)
    return analyst


@api_v1_router.get(f'/analysts/{{analyst_id}}', response_model=AnalystSchema)
async def get_analyst_by_id(analyst_id: int):
    """Retrieve data on a specific analyst given by `analyst_id`."""
    analyst = await analysts_repo.read(analyst_id)
    return analyst


@api_v1_router.put(f'/analysts/{{analyst_id}}', response_model=AnalystSchema)
async def update_analyst(analyst_id: int, payload: AnalystSchema):
    """Update analyst information.


    ## Notes

    The asset information must be complete - partial information update is not supported.
    """
    analyst = await analysts_repo.update(analyst_id, payload)
    return analyst


@api_v1_router.delete('/analysts/{analyst_id}', response_model=AnalystSchema)
async def delete_analyst(analyst_id: int):
    """Delete analyst from database."""
    analyst = await analysts_repo.delete(analyst_id)
    return analyst


@api_v1_router.post('/assets/subscription')
async def subscribe_user_to_asset_events(payload: Any):
    ...  # TODO: implement


@api_v1_router.delete('/subscriptions/{subscription_id}')
async def unsubscribe_user_from_asset_events(payload: Any):
    ...  # TODO: implement


