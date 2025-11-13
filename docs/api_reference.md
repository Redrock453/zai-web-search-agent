# API Reference

This document provides detailed API reference for the Z.AI Web Search Agent.

## Table of Contents

- [WebSearchAgent](#websearchagent)
  - [Constructor](#constructor)
  - [Methods](#methods)
    - [search](#search)
    - [search_with_request](#search_with_request)
- [Data Models](#data-models)
  - [SearchRequest](#searchrequest)
  - [SearchResponse](#searchresponse)
  - [SearchResult](#searchresult)
- [Authentication](#authentication)
  - [ZAIAuthenticator](#ziauthenticator)
  - [Methods](#methods-1)
- [Configuration](#configuration)
  - [ZAIConfig](#zaiconfig)
  - [Methods](#methods-2)
- [Exceptions](#exceptions)
- [Rate Limiting](#rate-limiting)
  - [RateLimiter](#ratelimiter)
  - [Methods](#methods-3)

## WebSearchAgent

The main class for interacting with the Z.AI web search API.

### Constructor

```python
WebSearchAgent(
    config: Optional[ZAIConfig] = None,
    authenticator: Optional[ZAIAuthenticator] = None,
    api_key: Optional[str] = None,
    max_retries: int = 3,
    initial_backoff: float = 1.0,
    max_backoff: float = 60.0,
    rate_limit_requests: int = 100,
    rate_limit_window: int = 60
)
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| config | Optional[ZAIConfig] | None | ZAIConfig instance with API settings |
| authenticator | Optional[ZAIAuthenticator] | None | ZAIAuthenticator instance for authentication |
| api_key | Optional[str] | None | Z.AI API key (overrides config.api_key if provided) |
| max_retries | int | 3 | Maximum number of retry attempts for failed requests |
| initial_backoff | float | 1.0 | Initial backoff time in seconds for exponential backoff |
| max_backoff | float | 60.0 | Maximum backoff time in seconds for exponential backoff |
| rate_limit_requests | int | 100 | Maximum number of requests allowed in the time window |
| rate_limit_window | int | 60 | Time window in seconds for rate limiting |

**Raises:**
- `ZAIAuthenticationError`: If authentication fails

### Methods

#### search

```python
search(
    query: str,
    num_results: int = 10,
    include_domains: Optional[list] = None,
    exclude_domains: Optional[list] = None,
    search_type: str = "web",
    language: Optional[str] = None,
    region: Optional[str] = None,
    safe_search: str = "moderate"
) -> SearchResponse
```

Perform a web search using the Z.AI API.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| query | str | Required | Search query string |
| num_results | int | 10 | Number of results to return (1-20) |
| include_domains | Optional[list] | None | List of domains to include in search results |
| exclude_domains | Optional[list] | None | List of domains to exclude from search results |
| search_type | str | "web" | Type of search ("web", "news", "images") |
| language | Optional[str] | None | Language code in ISO 639-1 format |
| region | Optional[str] | None | Region code in ISO 3166-1 format |
| safe_search | str | "moderate" | Safe search level ("moderate", "strict", "off") |

**Returns:** `SearchResponse` object containing the search results

**Raises:**
- `ZAIAuthenticationError`: If authentication fails
- `ZAIRateLimitError`: If rate limit is exceeded
- `ZAIInvalidRequestError`: If the request is invalid
- `ZAIApiError`: For other API errors

**Example:**
```python
agent = WebSearchAgent()
results = agent.search(
    query="artificial intelligence",
    num_results=15,
    include_domains=["nature.com", "science.org"],
    search_type="web",
    language="en",
    safe_search="moderate"
)
```

#### search_with_request

```python
search_with_request(request: SearchRequest) -> SearchResponse
```

Perform a web search using a SearchRequest model.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| request | SearchRequest | SearchRequest model with all search parameters |

**Returns:** `SearchResponse` object containing the search results

**Raises:**
- `ZAIAuthenticationError`: If authentication fails
- `ZAIRateLimitError`: If rate limit is exceeded
- `ZAIInvalidRequestError`: If the request is invalid
- `ZAIApiError`: For other API errors

**Example:**
```python
from src.agent import SearchRequest

request = SearchRequest(
    query="machine learning",
    num_results=10,
    search_type="news",
    language="en"
)

agent = WebSearchAgent()
results = agent.search_with_request(request)
```

## Data Models

### SearchRequest

Model for web search request parameters.

**Fields:**

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| query | str | Required | Search query string |
| num_results | int | 10 | Number of results to return (1-20) |
| include_domains | Optional[List[str]] | None | List of domains to include in search |
| exclude_domains | Optional[List[str]] | None | List of domains to exclude from search |
| search_type | str | "web" | Type of search: 'web', 'news', or 'images' |
| language | Optional[str] | None | Language code in ISO 639-1 format |
| region | Optional[str] | None | Region code in ISO 3166-1 format |
| safe_search | str | "moderate" | Safe search level: 'moderate', 'strict', or 'off' |

**Validators:**
- `validate_search_type`: Ensures search_type is one of: "web", "news", "images"
- `validate_safe_search`: Ensures safe_search is one of: "moderate", "strict", "off"
- `validate_language`: Ensures language code is 2 characters (ISO 639-1)
- `validate_region`: Ensures region code is 2 characters (ISO 3166-1)

**Example:**
```python
from src.agent import SearchRequest

request = SearchRequest(
    query="quantum computing",
    num_results=8,
    include_domains=["nature.com", "science.org"],
    search_type="web",
    language="en",
    safe_search="moderate"
)
```

### SearchResponse

Model for the complete API response.

**Fields:**

| Field | Type | Description |
|-------|------|-------------|
| query | str | The original search query |
| search_type | str | Type of search that was performed |
| total_results | int | Total number of results available |
| results | List[SearchResult] | List of search results |
| search_time | float | Time taken for the search in seconds |
| has_more | bool | Whether there are more results available |
| next_page_token | Optional[str] | Token for retrieving the next page of results |

**Example:**
```python
response = agent.search("artificial intelligence")

print(f"Query: {response.query}")
print(f"Total results: {response.total_results}")
print(f"Search time: {response.search_time:.2f} seconds")
print(f"Results returned: {len(response.results)}")
print(f"Has more: {response.has_more}")

# Access individual results
for result in response.results:
    print(f"Title: {result.title}")
    print(f"URL: {result.url}")
```

### SearchResult

Model for an individual search result.

**Fields:**

| Field | Type | Description |
|-------|------|-------------|
| title | str | Title of the search result |
| url | str | URL of the search result |
| snippet | str | Snippet or description of the search result |
| position | int | Position of the result in the search results |
| domain | str | Domain of the search result |
| published_date | Optional[str] | Publication date of the content |
| thumbnail_url | Optional[str] | URL to thumbnail image |

**Example:**
```python
result = response.results[0]

print(f"Title: {result.title}")
print(f"URL: {result.url}")
print(f"Snippet: {result.snippet}")
print(f"Position: {result.position}")
print(f"Domain: {result.domain}")
if result.published_date:
    print(f"Published: {result.published_date}")
if result.thumbnail_url:
    print(f"Thumbnail: {result.thumbnail_url}")
```

## Authentication

### ZAIAuthenticator

Handles authentication with the Z.AI API.

**Methods:**

#### Constructor

```python
ZAIAuthenticator(config: Optional[ZAIConfig] = None, api_key: Optional[str] = None)
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| config | Optional[ZAIConfig] | None | ZAIConfig instance with API settings |
| api_key | Optional[str] | None | Z.AI API key (overrides config.api_key if provided) |

**Raises:**
- `ZAIAuthenticationError`: If no API key is provided
- `ZAIInvalidRequestError`: If the API key format is invalid

#### get_auth_headers

```python
get_auth_headers() -> Dict[str, str]
```

Generate authorization headers for API requests.

**Returns:** Dictionary containing the authorization headers

**Raises:**
- `ZAIAuthenticationError`: If authentication fails

#### validate_credentials

```python
validate_credentials() -> bool
```

Validate the API credentials.

**Returns:** True if credentials are valid

**Raises:**
- `ZAIAuthenticationError`: If credentials are invalid

#### from_api_key

```python
@classmethod
from_api_key(cls, api_key: str) -> "ZAIAuthenticator"
```

Create an authenticator instance from an API key.

**Parameters:**
- `api_key` (str): Z.AI API key

**Returns:** ZAIAuthenticator instance

**Raises:**
- `ZAIAuthenticationError`: If API key is invalid
- `ZAIInvalidRequestError`: If the API key format is invalid

#### from_config

```python
@classmethod
from_config(cls, config: ZAIConfig) -> "ZAIAuthenticator"
```

Create an authenticator instance from a ZAIConfig.

**Parameters:**
- `config` (ZAIConfig): ZAIConfig instance

**Returns:** ZAIAuthenticator instance

**Raises:**
- `ZAIAuthenticationError`: If API key is invalid
- `ZAIInvalidRequestError`: If the API key format is invalid

## Configuration

### ZAIConfig

Configuration settings for Z.AI API using Pydantic for validation.

**Fields:**

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| api_key | str | Required | Z.AI API key |
| base_url | str | "https://api.z.ai/v1" | Base URL for Z.AI API |
| timeout | int | 30 | Request timeout in seconds |
| max_retries | int | 3 | Maximum number of retries for failed requests |

**Validators:**
- `validate_api_key`: Validates API key format (must match pattern: `^zai_[a-zA-Z0-9]{32}$`)
- `validate_timeout`: Ensures timeout is a positive integer
- `validate_max_retries`: Ensures max_retries is a non-negative integer

**Methods:**

#### from_env

```python
@classmethod
from_env(cls, env_file: Optional[str] = None) -> "ZAIConfig"
```

Load configuration from environment variables.

**Parameters:**
- `env_file` (Optional[str]): Path to .env file

**Returns:** ZAIConfig instance with values from environment

**Example:**
```python
# Load from default .env file
config = ZAIConfig.from_env()

# Load from custom file
config = ZAIConfig.from_env("custom.env")
```

## Exceptions

The library provides specific exception types for different error scenarios:

### ZAIApiError

Base exception for Z.AI API errors.

**Parameters:**
- `message` (str): Error message
- `status_code` (Optional[int]): HTTP status code (if applicable)
- `response_data` (Optional[Dict[str, Any]]): Response data from the API (if applicable)

### ZAIAuthenticationError

Raised when authentication with Z.AI API fails.

### ZAIRateLimitError

Raised when Z.AI API rate limit is exceeded.

### ZAIInvalidRequestError

Raised when the request to Z.AI API is invalid.

### ZAIServerError

Raised when the Z.AI API server encounters an error (5xx status codes).

## Rate Limiting

### RateLimiter

Rate limiter implementation using the token bucket algorithm.

**Constructor:**

```python
RateLimiter(max_requests: int = 100, time_window: int = 60)
```

**Parameters:**
- `max_requests` (int): Maximum number of requests allowed in the time window
- `time_window` (int): Time window in seconds

**Methods:**

#### can_make_request

```python
can_make_request() -> bool
```

Check if a request can be made without waiting.

**Returns:** True if a request can be made immediately, False otherwise

#### wait_if_needed

```python
wait_if_needed() -> float
```

Wait until a request can be made, if necessary.

**Returns:** The time waited in seconds

#### acquire_token

```python
acquire_token() -> bool
```

Try to acquire a token for making a request.

**Returns:** True if a token was acquired, False if no tokens are available

#### get_available_tokens

```python
get_available_tokens() -> int
```

Get the current number of available tokens.

**Returns:** The number of available tokens (integer)

#### get_time_until_next_token

```python
get_time_until_next_token() -> float
```

Get the time in seconds until the next token becomes available.

**Returns:** Time in seconds until next token, or 0 if tokens are available now

#### reset

```python
reset() -> None
```

Reset the rate limiter to its initial state.