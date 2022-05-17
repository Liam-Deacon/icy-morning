"""Provides `BaseSecurityService` class to act as security interface for different security solutions."""
import abc
from typing import Optional

from fastapi import status, HTTPException


class BaseSecurityService(abc.ABC):
    """Abstract base class for defining a security service interface."""

    @staticmethod
    def raise_401(detail="Unable to authenticate user", headers: Optional[dict] = None):
        """Raise 401 HTTP error to indicate user is not authorized."""
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers=headers or {},
        )

    @abc.abstractmethod
    def verify(self, *args, **kwargs):
        """Verify whether user is authenticated."""
        ...
