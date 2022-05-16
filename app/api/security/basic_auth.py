"""Provide a basic auth security service."""
import os
import secrets

from fastapi import Depends
from fastapi.security import HTTPBasicCredentials

from .base_auth import BaseSecurityService


class BasicAuthSecurityService(BaseSecurityService):
    """Implements basic auth security service."""

    def __init__(self):
        self.username = os.getenv("BASIC_AUTH_USERNAME")
        self.password = os.getenv("BASIC_AUTH_PASSWORD")

    def verify(self, credentials, *args, **kwargs) -> None:
        correct_credentials = secrets.compare_digest(
            (credentials.username or "") + (credentials.password or ""),
            (self.username or "") + (self.password or ""),
        )
        if not correct_credentials:
            self.raise_401(
                headers={"WWW-Authenticate": "Basic"},
                detail="Incorrect email or password",
            )
