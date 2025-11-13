"""
Authentication module for Z.AI API
"""

import re
from typing import Dict, Optional
from .config import ZAIConfig
from .exceptions import ZAIAuthenticationError, ZAIInvalidRequestError


class ZAIAuthenticator:
    """
    Handles authentication with the Z.AI API.
    
    This class provides methods to initialize with an API key,
    generate authorization headers, and validate API key format.
    """
    
    # Regular expression for validating API key format (flexible for various providers)
    API_KEY_PATTERN: re.Pattern = re.compile(r"^[a-zA-Z0-9._-]{20,}$")
    
    def __init__(self, config: Optional[ZAIConfig] = None, api_key: Optional[str] = None):
        """
        Initialize the ZAI authenticator.
        
        Args:
            config: ZAIConfig instance with API settings (optional)
            api_key: Z.AI API key (optional, overrides config.api_key if provided)
            
        Raises:
            ZAIAuthenticationError: If no API key is provided
            ZAIInvalidRequestError: If the API key format is invalid
        """
        if api_key:
            self.api_key = api_key
        elif config and config.api_key:
            self.api_key = config.api_key
        else:
            raise ZAIAuthenticationError("API key is required for authentication")
        
        # Validate API key format
        self._validate_api_key(self.api_key)
        
        # Store config if provided
        self.config = config
    
    def _validate_api_key(self, api_key: str) -> None:
        """
        Validate the API key format.
        
        Args:
            api_key: API key string to validate
            
        Raises:
            ZAIInvalidRequestError: If the API key format is invalid
        """
        if not api_key:
            raise ZAIInvalidRequestError("API key cannot be empty")
        
        if not self.API_KEY_PATTERN.match(api_key):
            raise ZAIInvalidRequestError(
                f"Invalid API key format. Must be at least 20 characters with alphanumeric, dots, underscores, or hyphens"
            )
    
    def get_auth_headers(self) -> Dict[str, str]:
        """
        Generate authorization headers for API requests.
        
        Returns:
            Dictionary containing the authorization headers
            
        Raises:
            ZAIAuthenticationError: If authentication fails
        """
        try:
            return {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
        except Exception as e:
            raise ZAIAuthenticationError(f"Failed to generate auth headers: {str(e)}")
    
    def validate_credentials(self) -> bool:
        """
        Validate the API credentials.
        
        Returns:
            True if credentials are valid
            
        Raises:
            ZAIAuthenticationError: If credentials are invalid
        """
        try:
            self._validate_api_key(self.api_key)
            return True
        except ZAIInvalidRequestError as e:
            raise ZAIAuthenticationError(f"Invalid credentials: {str(e)}")
    
    @classmethod
    def from_api_key(cls, api_key: str) -> "ZAIAuthenticator":
        """
        Create an authenticator instance from an API key.
        
        Args:
            api_key: Z.AI API key
            
        Returns:
            ZAIAuthenticator instance
            
        Raises:
            ZAIAuthenticationError: If API key is invalid
            ZAIInvalidRequestError: If the API key format is invalid
        """
        return cls(api_key=api_key)
    
    @classmethod
    def from_config(cls, config: ZAIConfig) -> "ZAIAuthenticator":
        """
        Create an authenticator instance from a ZAIConfig.
        
        Args:
            config: ZAIConfig instance
            
        Returns:
            ZAIAuthenticator instance
            
        Raises:
            ZAIAuthenticationError: If API key is invalid
            ZAIInvalidRequestError: If the API key format is invalid
        """
        return cls(config=config)