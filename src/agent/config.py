"""
Configuration management for the Z.AI web search agent
"""

import os
import re
from typing import Optional, ClassVar
from dotenv import load_dotenv
from pydantic import BaseSettings, Field, validator


class ZAIConfig(BaseSettings):
    """
    Configuration settings for Z.AI API using Pydantic for validation.
    
    Attributes:
        api_key: Z.AI API key (required)
        base_url: Base URL for Z.AI API (default: "https://api.z.ai/v1")
        timeout: Request timeout in seconds (default: 30)
        max_retries: Maximum number of retries for failed requests (default: 3)
    """
    
    api_key: str = Field(..., description="Z.AI API key")
    base_url: str = Field(default="https://api.z.ai/v1", description="Base URL for Z.AI API")
    timeout: int = Field(default=30, description="Request timeout in seconds")
    max_retries: int = Field(default=3, description="Maximum number of retries for failed requests")
    
    # Regular expression for validating API key format
    API_KEY_PATTERN: ClassVar[re.Pattern] = re.compile(r"^zai_[a-zA-Z0-9]{32}$")
    
    class Config:
        env_prefix = "ZAI_"
        env_file = ".env"
        case_sensitive = False
    
    @validator("api_key")
    def validate_api_key(cls, v: str) -> str:
        """
        Validate the API key format.
        
        Args:
            v: API key string to validate
            
        Returns:
            The validated API key
            
        Raises:
            ValueError: If the API key format is invalid
        """
        if not v:
            raise ValueError("API key is required")
        
        if not cls.API_KEY_PATTERN.match(v):
            raise ValueError(
                f"Invalid API key format. Expected pattern: {cls.API_KEY_PATTERN.pattern}"
            )
        
        return v
    
    @validator("timeout")
    def validate_timeout(cls, v: int) -> int:
        """
        Validate the timeout value.
        
        Args:
            v: Timeout value in seconds
            
        Returns:
            The validated timeout value
            
        Raises:
            ValueError: If the timeout is not a positive integer
        """
        if v <= 0:
            raise ValueError("Timeout must be a positive integer")
        return v
    
    @validator("max_retries")
    def validate_max_retries(cls, v: int) -> int:
        """
        Validate the max_retries value.
        
        Args:
            v: Maximum number of retries
            
        Returns:
            The validated max_retries value
            
        Raises:
            ValueError: If max_retries is not a non-negative integer
        """
        if v < 0:
            raise ValueError("Max retries must be a non-negative integer")
        return v
    
    @classmethod
    def from_env(cls, env_file: Optional[str] = None) -> "ZAIConfig":
        """
        Load configuration from environment variables.
        
        Args:
            env_file: Path to .env file (optional)
            
        Returns:
            ZAIConfig instance with values from environment
        """
        if env_file:
            load_dotenv(env_file)
        else:
            load_dotenv()
        
        return cls(
            api_key=os.getenv("ZAI_API_KEY", ""),
            base_url=os.getenv("ZAI_BASE_URL", "https://api.z.ai/v1"),
            timeout=int(os.getenv("ZAI_TIMEOUT", "30")),
            max_retries=int(os.getenv("ZAI_MAX_RETRIES", "3"))
        )