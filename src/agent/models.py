"""
Pydantic models for Z.AI web search API request and response data structures
"""

from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field, validator


class SearchRequest(BaseModel):
    """
    Model for web search request parameters
    
    Attributes:
        query: Search query string (required)
        num_results: Number of results to return (1-20, default: 10)
        include_domains: List of domains to include in search results
        exclude_domains: List of domains to exclude from search results
        search_type: Type of search ("web", "news", "images", default: "web")
        language: Language code in ISO 639-1 format
        region: Region code in ISO 3166-1 format
        safe_search: Safe search level ("moderate", "strict", "off")
    """
    
    query: str = Field(..., description="Search query string")
    num_results: int = Field(default=10, ge=1, le=20, description="Number of results to return (1-20)")
    include_domains: Optional[List[str]] = Field(default=None, description="List of domains to include in search")
    exclude_domains: Optional[List[str]] = Field(default=None, description="List of domains to exclude from search")
    search_type: str = Field(default="web", description="Type of search: 'web', 'news', or 'images'")
    language: Optional[str] = Field(default=None, description="Language code in ISO 639-1 format")
    region: Optional[str] = Field(default=None, description="Region code in ISO 3166-1 format")
    safe_search: str = Field(default="moderate", description="Safe search level: 'moderate', 'strict', or 'off'")
    
    @validator("search_type")
    def validate_search_type(cls, v: str) -> str:
        """Validate search_type parameter"""
        allowed_types = ["web", "news", "images"]
        if v not in allowed_types:
            raise ValueError(f"search_type must be one of: {', '.join(allowed_types)}")
        return v
    
    @validator("safe_search")
    def validate_safe_search(cls, v: str) -> str:
        """Validate safe_search parameter"""
        allowed_levels = ["moderate", "strict", "off"]
        if v not in allowed_levels:
            raise ValueError(f"safe_search must be one of: {', '.join(allowed_levels)}")
        return v
    
    @validator("language")
    def validate_language(cls, v: Optional[str]) -> Optional[str]:
        """Validate language code format"""
        if v and len(v) != 2:
            raise ValueError("Language code must be in ISO 639-1 format (2 characters)")
        return v
    
    @validator("region")
    def validate_region(cls, v: Optional[str]) -> Optional[str]:
        """Validate region code format"""
        if v and len(v) != 2:
            raise ValueError("Region code must be in ISO 3166-1 format (2 characters)")
        return v


class SearchResult(BaseModel):
    """
    Model for an individual search result
    
    Attributes:
        title: Title of the search result
        url: URL of the search result
        snippet: Snippet or description of the search result
        position: Position of the result in the search results
        domain: Domain of the search result
        published_date: Publication date of the content (for news results)
        thumbnail_url: URL to thumbnail image (for image results)
    """
    
    title: str = Field(..., description="Title of the search result")
    url: str = Field(..., description="URL of the search result")
    snippet: str = Field(..., description="Snippet or description of the search result")
    position: int = Field(..., description="Position of the result in the search results")
    domain: str = Field(..., description="Domain of the search result")
    published_date: Optional[str] = Field(default=None, description="Publication date of the content")
    thumbnail_url: Optional[str] = Field(default=None, description="URL to thumbnail image")


class SearchResponse(BaseModel):
    """
    Model for the complete API response
    
    Attributes:
        query: The original search query
        search_type: Type of search that was performed
        total_results: Total number of results available
        results: List of search results
        search_time: Time taken for the search in seconds
        has_more: Whether there are more results available
        next_page_token: Token for retrieving the next page of results
    """
    
    query: str = Field(..., description="The original search query")
    search_type: str = Field(..., description="Type of search that was performed")
    total_results: int = Field(..., description="Total number of results available")
    results: List[SearchResult] = Field(..., description="List of search results")
    search_time: float = Field(..., description="Time taken for the search in seconds")
    has_more: bool = Field(default=False, description="Whether there are more results available")
    next_page_token: Optional[str] = Field(default=None, description="Token for retrieving the next page")