"""
Web search agent for interacting with the Z.AI API
"""

import json
import time
import logging
from typing import Optional, Dict, Any, Union
import requests
from .config import ZAIConfig
from .auth import ZAIAuthenticator
from .models import SearchRequest, SearchResponse, SearchResult
from .exceptions import (
    ZAIApiError,
    ZAIAuthenticationError,
    ZAIRateLimitError,
    ZAIInvalidRequestError,
    ZAIServerError
)
from .rate_limiter import RateLimiter

# Set up logger
logger = logging.getLogger(__name__)


class WebSearchAgent:
    """
    Main class for interacting with the Z.AI web search API
    
    This class provides methods to perform web searches using the Z.AI API,
    with support for various search parameters and proper error handling.
    """
    
    def __init__(
        self,
        config: Optional[ZAIConfig] = None,
        authenticator: Optional[ZAIAuthenticator] = None,
        api_key: Optional[str] = None,
        max_retries: int = 3,
        initial_backoff: float = 1.0,
        max_backoff: float = 60.0,
        rate_limit_requests: int = 100,
        rate_limit_window: int = 60
    ):
        """
        Initialize the WebSearchAgent
        
        Args:
            config: ZAIConfig instance with API settings (optional)
            authenticator: ZAIAuthenticator instance for authentication (optional)
            api_key: Z.AI API key (optional, overrides config.api_key if provided)
            max_retries: Maximum number of retry attempts for failed requests (default: 3)
            initial_backoff: Initial backoff time in seconds for exponential backoff (default: 1.0)
            max_backoff: Maximum backoff time in seconds for exponential backoff (default: 60.0)
            rate_limit_requests: Maximum number of requests allowed in the time window (default: 100)
            rate_limit_window: Time window in seconds for rate limiting (default: 60)
            
        Raises:
            ZAIAuthenticationError: If authentication fails
        """
        # Use provided config or create a default one
        self.config = config or ZAIConfig()
        
        # Use provided authenticator or create one from config or api_key
        if authenticator:
            self.authenticator = authenticator
        elif api_key:
            self.authenticator = ZAIAuthenticator(api_key=api_key)
        else:
            # Try to create from config, but handle potential authentication errors
            # This allows for initialization without actual credentials for testing
            try:
                self.authenticator = ZAIAuthenticator(config=self.config)
            except ZAIAuthenticationError:
                # Create a mock authenticator for testing purposes
                self.authenticator = None
        
        # Base URL for the search API endpoint
        self.search_endpoint = f"{self.config.base_url}/search"
        
        # Initialize rate limiter
        self.rate_limiter = RateLimiter(
            max_requests=rate_limit_requests,
            time_window=rate_limit_window
        )
        
        # Retry configuration
        self.max_retries = max_retries
        self.initial_backoff = initial_backoff
        self.max_backoff = max_backoff
        
        logger.debug(f"WebSearchAgent initialized with rate limiting: {rate_limit_requests} requests per {rate_limit_window} seconds")
    
    def _make_request_with_retry(self, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make an HTTP request to the Z.AI API with retry logic and rate limiting
        
        Args:
            endpoint: API endpoint URL
            params: Request parameters
            
        Returns:
            Dictionary containing the API response
            
        Raises:
            ZAIApiError: If the API request fails after all retries
            ZAIAuthenticationError: If authentication fails
            ZAIRateLimitError: If rate limit is exceeded
            ZAIInvalidRequestError: If the request is invalid
        """
        # Wait for rate limiter if needed
        wait_time = self.rate_limiter.wait_if_needed()
        if wait_time > 0:
            logger.debug(f"Rate limited: waited {wait_time:.2f} seconds")
        
        # Initialize retry variables
        retry_count = 0
        backoff_time = self.initial_backoff
        last_exception = None
        
        while retry_count <= self.max_retries:
            try:
                # Log the attempt
                if retry_count > 0:
                    logger.info(f"Retry attempt {retry_count}/{self.max_retries} after {backoff_time:.2f}s backoff")
                
                # Make the actual request
                return self._make_request(endpoint, params)
                
            except ZAIAuthenticationError as e:
                # Don't retry authentication errors
                logger.error(f"Authentication error: {str(e)}")
                raise e
                
            except ZAIInvalidRequestError as e:
                # Don't retry invalid request errors
                logger.error(f"Invalid request error: {str(e)}")
                raise e
                
            except ZAIRateLimitError as e:
                # For rate limit errors, use the retry-after header if available
                retry_after = None
                if e.response_data and 'retry_after' in e.response_data:
                    retry_after = e.response_data['retry_after']
                
                if retry_after:
                    wait_time = float(retry_after)
                    logger.warning(f"Rate limited by API. Waiting {wait_time} seconds as per retry-after header.")
                    time.sleep(wait_time)
                else:
                    # Use exponential backoff for rate limit errors
                    logger.warning(f"Rate limit exceeded. Waiting {backoff_time:.2f} seconds before retry.")
                    time.sleep(backoff_time)
                    backoff_time = min(backoff_time * 2, self.max_backoff)
                
                retry_count += 1
                last_exception = e
                
            except (ZAIApiError, requests.exceptions.RequestException) as e:
                # For other API errors, use exponential backoff
                logger.warning(f"API error: {str(e)}. Retrying in {backoff_time:.2f} seconds.")
                time.sleep(backoff_time)
                backoff_time = min(backoff_time * 2, self.max_backoff)
                
                retry_count += 1
                last_exception = ZAIApiError(str(e))
        
        # If we've exhausted all retries, raise the last exception
        logger.error(f"Request failed after {self.max_retries} retries")
        raise last_exception or ZAIApiError("Request failed after maximum retries")
    
    def _make_request(self, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make a single HTTP request to the Z.AI API
        
        Args:
            endpoint: API endpoint URL
            params: Request parameters
            
        Returns:
            Dictionary containing the API response
            
        Raises:
            ZAIApiError: If the API request fails
            ZAIAuthenticationError: If authentication fails
            ZAIRateLimitError: If rate limit is exceeded
            ZAIInvalidRequestError: If the request is invalid
        """
        try:
            # Check if authenticator is available
            if not self.authenticator:
                raise ZAIAuthenticationError("No authenticator available. Please provide valid API credentials.")
                
            # Get authentication headers
            headers = self.authenticator.get_auth_headers()
            
            # Log the request
            logger.debug(f"Making request to {endpoint} with params: {params}")
            
            # Make the HTTP request
            response = requests.get(
                endpoint,
                headers=headers,
                params=params,
                timeout=self.config.timeout
            )
            
            # Handle different HTTP status codes
            if response.status_code == 401:
                response_data = response.json() if response.content else {}
                logger.error(f"Authentication failed (401): {response_data}")
                raise ZAIAuthenticationError(
                    "Authentication failed. Please check your API key.",
                    status_code=response.status_code,
                    response_data=response_data
                )
            elif response.status_code == 429:
                response_data = response.json() if response.content else {}
                logger.warning(f"Rate limit exceeded (429): {response_data}")
                raise ZAIRateLimitError(
                    "Rate limit exceeded. Please try again later.",
                    status_code=response.status_code,
                    response_data=response_data
                )
            elif response.status_code == 400:
                response_data = response.json() if response.content else {}
                logger.error(f"Invalid request (400): {response_data}")
                raise ZAIInvalidRequestError(
                    "Invalid request. Please check your parameters.",
                    status_code=response.status_code,
                    response_data=response_data
                )
            elif 500 <= response.status_code < 600:
                response_data = response.json() if response.content else {}
                logger.error(f"Server error ({response.status_code}): {response_data}")
                raise ZAIServerError(
                    f"Server error with status code {response.status_code}",
                    status_code=response.status_code,
                    response_data=response_data
                )
            elif response.status_code != 200:
                response_data = response.json() if response.content else {}
                logger.error(f"Unexpected status code ({response.status_code}): {response_data}")
                raise ZAIApiError(
                    f"API request failed with status code {response.status_code}",
                    status_code=response.status_code,
                    response_data=response_data
                )
            
            # Parse and return the JSON response
            response_data = response.json()
            logger.debug(f"Request successful with {len(response_data.get('results', []))} results")
            return response_data
            
        except requests.exceptions.Timeout:
            logger.error(f"Request timed out after {self.config.timeout} seconds")
            raise ZAIApiError(f"Request timed out after {self.config.timeout} seconds")
        except requests.exceptions.ConnectionError:
            logger.error("Failed to connect to the Z.AI API")
            raise ZAIApiError("Failed to connect to the Z.AI API")
        except requests.exceptions.RequestException as e:
            logger.error(f"Request exception: {str(e)}")
            raise ZAIApiError(f"Request failed: {str(e)}")
        except json.JSONDecodeError:
            logger.error("Failed to parse API response as JSON")
            raise ZAIApiError("Failed to parse API response as JSON")
    
    def _transform_api_response(self, api_response: Dict[str, Any], request: SearchRequest) -> SearchResponse:
        """
        Transform the API response into a SearchResponse model
        
        Args:
            api_response: Raw API response
            request: Original search request
            
        Returns:
            SearchResponse model with transformed data
        """
        # Extract search results from API response
        results_data = api_response.get("results", [])
        
        # Transform each result into a SearchResult model
        results = []
        for result_data in results_data:
            # Extract domain from URL
            url = result_data.get("url", "")
            domain = url.split("/")[2] if "/" in url and len(url.split("/")) > 2 else ""
            
            result = SearchResult(
                title=result_data.get("title", ""),
                url=url,
                snippet=result_data.get("snippet", ""),
                position=result_data.get("position", 0),
                domain=domain,
                published_date=result_data.get("published_date"),
                thumbnail_url=result_data.get("thumbnail_url")
            )
            results.append(result)
        
        # Create and return the SearchResponse
        return SearchResponse(
            query=request.query,
            search_type=request.search_type,
            total_results=api_response.get("total_results", len(results)),
            results=results,
            search_time=api_response.get("search_time", 0.0),
            has_more=api_response.get("has_more", False),
            next_page_token=api_response.get("next_page_token")
        )
    
    def search(
        self,
        query: str,
        num_results: int = 10,
        include_domains: Optional[list] = None,
        exclude_domains: Optional[list] = None,
        search_type: str = "web",
        language: Optional[str] = None,
        region: Optional[str] = None,
        safe_search: str = "moderate"
    ) -> SearchResponse:
        """
        Perform a web search using the Z.AI API
        
        Args:
            query: Search query string (required)
            num_results: Number of results to return (1-20, default: 10)
            include_domains: List of domains to include in search results
            exclude_domains: List of domains to exclude from search results
            search_type: Type of search ("web", "news", "images", default: "web")
            language: Language code in ISO 639-1 format
            region: Region code in ISO 3166-1 format
            safe_search: Safe search level ("moderate", "strict", "off")
            
        Returns:
            SearchResponse object containing the search results
            
        Raises:
            ZAIAuthenticationError: If authentication fails
            ZAIRateLimitError: If rate limit is exceeded
            ZAIInvalidRequestError: If the request is invalid
            ZAIApiError: For other API errors
        """
        # Create a SearchRequest model with the provided parameters
        request = SearchRequest(
            query=query,
            num_results=num_results,
            include_domains=include_domains,
            exclude_domains=exclude_domains,
            search_type=search_type,
            language=language,
            region=region,
            safe_search=safe_search
        )
        
        # Convert the request to a dictionary for the API call
        params = request.dict(exclude_none=True)
        
        # Make the API request with retry logic and rate limiting
        logger.info(f"Searching for: {query}")
        api_response = self._make_request_with_retry(self.search_endpoint, params)
        
        # Transform the API response into a SearchResponse model
        response = self._transform_api_response(api_response, request)
        logger.info(f"Search completed with {len(response.results)} results")
        return response
    
    def search_with_request(self, request: SearchRequest) -> SearchResponse:
        """
        Perform a web search using a SearchRequest model
        
        Args:
            request: SearchRequest model with all search parameters
            
        Returns:
            SearchResponse object containing the search results
            
        Raises:
            ZAIAuthenticationError: If authentication fails
            ZAIRateLimitError: If rate limit is exceeded
            ZAIInvalidRequestError: If the request is invalid
            ZAIApiError: For other API errors
        """
        # Convert the request to a dictionary for the API call
        params = request.dict(exclude_none=True)
        
        # Make the API request with retry logic and rate limiting
        logger.info(f"Searching for: {request.query}")
        api_response = self._make_request_with_retry(self.search_endpoint, params)
        
        # Transform the API response into a SearchResponse model
        response = self._transform_api_response(api_response, request)
        logger.info(f"Search completed with {len(response.results)} results")
        return response