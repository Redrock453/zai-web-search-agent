"""
Z.AI Web Search Agent

This package provides a Python client for interacting with the Z.AI API.
"""

from .config import ZAIConfig
from .auth import ZAIAuthenticator
from .models import SearchRequest, SearchResult, SearchResponse
from .web_search_agent import WebSearchAgent
from .exceptions import (
    ZAIApiError,
    ZAIAuthenticationError,
    ZAIRateLimitError,
    ZAIInvalidRequestError,
    ZAIServerError
)
from .rate_limiter import RateLimiter

__version__ = "0.1.0"
__all__ = [
    "ZAIConfig",
    "ZAIAuthenticator",
    "WebSearchAgent",
    "SearchRequest",
    "SearchResult",
    "SearchResponse",
    "ZAIApiError",
    "ZAIAuthenticationError",
    "ZAIRateLimitError",
    "ZAIInvalidRequestError",
    "ZAIServerError",
    "RateLimiter"
]