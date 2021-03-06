"""Defines routes for v1 API."""
from typing import List

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBasicCredentials

from starlette import status

# NOTE: use relative imports to be compatible with uvicorn without needing a python package
from app.api.schemas import (
    AnalystInputSchema,
    AssetInputSchema,
    AssetSchema,
    AnalystSchema,
    SubscriptionInputSchema,
    SubscriptionSchema,
)
from app.api.security import SECURITY, SECURITY_SERVICE
from app.db.tables import AssetModel, AnalystModel
from app.db.repositories import (
    AssetRepository,
    AnalystRepository,
    SubscriptionRepository,
)

API_PREFIX = "/api/v1"

assets_repo = AssetRepository()
analysts_repo = AnalystRepository()
subscription_repo = SubscriptionRepository()

api_v1_router = APIRouter(prefix=API_PREFIX)


@api_v1_router.get("/assets", response_model=List[AssetSchema])
async def get_assets():
    """Retrieve all assets."""
    assets: List[AssetModel] = await assets_repo.fetch_all()
    return [AssetSchema(**asset) for asset in assets]


@api_v1_router.post(
    "/assets",
    status_code=status.HTTP_201_CREATED,
    response_model=AssetSchema,
)
async def create_asset(
    payload: AssetInputSchema, credentials: HTTPBasicCredentials = Depends(SECURITY)
):
    """Create a new asset."""
    SECURITY_SERVICE.verify(credentials)
    asset = await assets_repo.create(payload)
    return asset


@api_v1_router.get("/assets/{asset_id}", response_model=AssetSchema)
async def read_asset(asset_id: int):
    """Retrieve data on a specific asset given by `asset_id`."""
    asset = await assets_repo.read(asset_id)
    return asset


@api_v1_router.put("/assets/{asset_id}", response_model=AssetSchema)
async def update_asset(
    asset_id: int,
    payload: AssetInputSchema,
    credentials: HTTPBasicCredentials = Depends(SECURITY),
):
    """Update information on asset given by `asset_id`."""
    SECURITY_SERVICE.verify(credentials)
    asset = await assets_repo.update(asset_id, payload)
    return asset


@api_v1_router.delete("/assets/{asset_id}", response_model=AssetSchema)
async def delete_asset(
    asset_id: int, credentials: HTTPBasicCredentials = Depends(SECURITY)
):
    """Delete asset from database."""
    SECURITY_SERVICE.verify(credentials)
    asset = await assets_repo.delete(asset_id)
    return asset


@api_v1_router.get("/analysts", response_model=List[AnalystSchema])
async def get_analysts():
    """Retrieve list of analysts."""
    analysts: List[AnalystModel] = await analysts_repo.fetch_all()
    return [AnalystSchema(**analyst) for analyst in analysts]


@api_v1_router.post(
    "/analysts", status_code=status.HTTP_201_CREATED, response_model=AnalystSchema
)
async def create_analyst(
    payload: AnalystInputSchema, credentials: HTTPBasicCredentials = Depends(SECURITY)
):
    """Add a new analyst to the database."""
    SECURITY_SERVICE.verify(credentials)
    analyst = await analysts_repo.create(payload)
    return analyst


@api_v1_router.get("/analysts/{analyst_id}", response_model=AnalystSchema)
async def get_analyst_by_id(analyst_id: int):
    """Retrieve data on a specific analyst given by `analyst_id`."""
    analyst = await analysts_repo.read(analyst_id)
    return analyst


@api_v1_router.put("/analysts/{analyst_id}", response_model=AnalystSchema)
async def update_analyst(
    analyst_id: int,
    payload: AnalystSchema,
    credentials: HTTPBasicCredentials = Depends(SECURITY),
):
    """Update analyst information.


    ## Notes

    The asset information must be complete - partial information update is not supported.
    """
    SECURITY_SERVICE.verify(credentials)
    analyst = await analysts_repo.update(analyst_id, payload)
    return analyst


@api_v1_router.delete("/analysts/{analyst_id}", response_model=AnalystSchema)
async def delete_analyst(
    analyst_id: int, credentials: HTTPBasicCredentials = Depends(SECURITY)
):
    """Delete analyst from database."""
    SECURITY_SERVICE.verify(credentials)
    analyst = await analysts_repo.delete(analyst_id)
    return analyst


@api_v1_router.post("/assets/subscription")
async def subscribe_user_to_asset_events(
    payload: SubscriptionInputSchema,
    credentials: HTTPBasicCredentials = Depends(SECURITY),
):
    """Subscribe user to asset events."""
    SECURITY_SERVICE.verify(credentials)
    subscription = await subscription_repo.create(payload)
    return subscription


@api_v1_router.delete(
    "/subscriptions/{subscription_id}", response_model=SubscriptionSchema
)
async def unsubscribe_user_from_asset_events(
    subscription_id: int, credentials: HTTPBasicCredentials = Depends(SECURITY)
):
    """Remove user subscription from asset events."""
    SECURITY_SERVICE.verify(credentials)
    subscription = await subscription_repo.delete(subscription_id)
    return subscription
