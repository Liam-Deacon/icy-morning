from urllib.parse import urlparse

from loguru import logger

from sqlalchemy.engine import create_engine
from sqlalchemy_utils.functions import create_database, database_exists

from app.db.tables.base import BaseModel


def is_in_memory_database(url_connection_string: str):
    url = urlparse(url_connection_string)
    return url.path.startswith('sqlite') and \
        (not url.path.lstrip('/') or url.path == ':memory:')


def setup_database(url: str):
    sanitised_url = url.replace('+aiosqlite', '')
    if url != sanitised_url:
        logger.debug(f'Sanitising database connection string {url!r} -> {sanitised_url!r}')
    logger.info(f'Setting up database {sanitised_url!r}...')
    engine = create_engine(sanitised_url)
    if not database_exists(sanitised_url) or is_in_memory_database(sanitised_url):
        logger.debug(f'Creating database {sanitised_url!r}...')
        create_database(sanitised_url)
    
    BaseModel.metadata.create_all(engine, checkfirst=True)
