import os

from collections import defaultdict
from typing import Any, Type

from fastapi.security import HTTPBasic, HTTPBearer  # noqa: F401

from .base_auth import BaseSecurityService
from .basic_auth import BasicAuthSecurityService

AUTH_TYPE_LOOKUP: dict[str, Type[BaseSecurityService]] = defaultdict(
    lambda: BasicAuthSecurityService,
    {
        "basic": BasicAuthSecurityService,
    },
)

AUTH_TYPE = AUTH_TYPE_LOOKUP[os.getenv("AUTH_TYPE")]


SECURITY_TYPE_LOOKUP: dict[str, Any] = defaultdict(
    lambda: HTTPBasic,
    {
        "basic": HTTPBasic,
    },
)

SECURITY = SECURITY_TYPE_LOOKUP[AUTH_TYPE]()

SECURITY_SERVICE: BaseSecurityService = AUTH_TYPE()
