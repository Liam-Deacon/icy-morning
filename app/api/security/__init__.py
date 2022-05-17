"""Subpackage for security backends."""
import os

from collections import defaultdict
from typing import Any, Dict, Type

from fastapi.security import HTTPBasic, HTTPBearer  # noqa: F401

from app.api.security.base_auth import BaseSecurityService
from app.api.security.basic_auth import BasicAuthSecurityService

#: Hashmap lookup for authentication types
AUTH_TYPE_LOOKUP: Dict[str, Type[BaseSecurityService]] = defaultdict(
    lambda: BasicAuthSecurityService,
    {
        "basic": BasicAuthSecurityService,
    },
)

#: The authentication type to use for the current environment
AUTH_TYPE = AUTH_TYPE_LOOKUP[os.getenv("AUTH_TYPE")]

#: Hashmap lookup for different security types
SECURITY_TYPE_LOOKUP: Dict[str, Any] = defaultdict(
    lambda: HTTPBasic,
    {
        "basic": HTTPBasic,
    },
)

#: The security type to use for the current environment
SECURITY = SECURITY_TYPE_LOOKUP[AUTH_TYPE]()

#: The security service to use for the current environment
SECURITY_SERVICE: BaseSecurityService = AUTH_TYPE()

# TODO: Provide facades to allow routers to use BasicAuth, BearerAuth etc. in same way.
