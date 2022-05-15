"""This module defines the main FastAPI app."""
import os

from fastapi import FastAPI
from fastapi_async_sqlalchemy import SQLAlchemyMiddleware

from mangum import Mangum

from app.api.routes.v1 import api_v1_router
from app.db.utils import setup_database


#: Defines the database connection URL, defaulting to local SQLite DB
sqlalchemy_connection_string: str = (
    os.environ.get("SQLALCHEMY_DATABASE_CONNECTION_URI")
    or "sqlite+aiosqlite:///db.sqlite"
)  # noqa: E501

# TODO: enabled in-memory database support (unable to create tables using sync + async drivers)
setup_database(sqlalchemy_connection_string)

app = FastAPI(
    title="Icy Morning REST API",
    description="""
A simple REST API for tracking assets and analysts.

""",
)

app.add_middleware(SQLAlchemyMiddleware, db_url=sqlalchemy_connection_string)

app.include_router(api_v1_router)

#: Wrapper for AWS API Gateway
handler: Mangum = Mangum(app)
