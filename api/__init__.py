"""API clients package for API testing."""

from .base_api import BaseAPI
from .jsonplaceholder_api import JSONPlaceholderAPI

__all__ = ["BaseAPI", "JSONPlaceholderAPI"] 