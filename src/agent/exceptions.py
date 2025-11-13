"""
Custom exceptions for the Z.AI web search agent
"""

from typing import Optional, Any, Dict


class ZAIApiError(Exception):
    """Base exception for Z.AI API errors"""
    
    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response_data: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize the base Z.AI API error.
        
        Args:
            message: Error message
            status_code: HTTP status code (if applicable)
            response_data: Response data from the API (if applicable)
        """
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.response_data = response_data or {}


class ZAIAuthenticationError(ZAIApiError):
    """Raised when authentication with Z.AI API fails"""
    
    def __init__(
        self,
        message: str = "Authentication failed",
        status_code: Optional[int] = None,
        response_data: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize authentication error.
        
        Args:
            message: Error message
            status_code: HTTP status code (if applicable)
            response_data: Response data from the API (if applicable)
        """
        super().__init__(message, status_code, response_data)


class ZAIRateLimitError(ZAIApiError):
    """Raised when Z.AI API rate limit is exceeded"""
    
    def __init__(
        self,
        message: str = "Rate limit exceeded",
        status_code: Optional[int] = None,
        response_data: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize rate limit error.
        
        Args:
            message: Error message
            status_code: HTTP status code (if applicable)
            response_data: Response data from the API (if applicable)
        """
        super().__init__(message, status_code, response_data)


class ZAIInvalidRequestError(ZAIApiError):
    """Raised when the request to Z.AI API is invalid"""
    
    def __init__(
        self,
        message: str = "Invalid request",
        status_code: Optional[int] = None,
        response_data: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize invalid request error.
        
        Args:
            message: Error message
            status_code: HTTP status code (if applicable)
            response_data: Response data from the API (if applicable)
        """
        super().__init__(message, status_code, response_data)


class ZAIServerError(ZAIApiError):
    """Raised when the Z.AI API server encounters an error (5xx status codes)"""
    
    def __init__(
        self,
        message: str = "Server error",
        status_code: Optional[int] = None,
        response_data: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize server error.
        
        Args:
            message: Error message
            status_code: HTTP status code (if applicable)
            response_data: Response data from the API (if applicable)
        """
        super().__init__(message, status_code, response_data)