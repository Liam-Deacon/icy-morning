"""This module provides exception classes for use with REST API responses."""
from functools import partial

from fastapi import HTTPException

#: Convenience definition for a 409 conflict error
ConflictException = partial(HTTPException, status_code=409)

#: Convenience definition for a 404 not found error
NotFoundException = partial(HTTPException, status_code=404)
