# Error Handling Guide

This document provides comprehensive information about error handling in the Z.AI Web Search Agent.

## Table of Contents

- [Exception Hierarchy](#exception-hierarchy)
- [Exception Types](#exception-types)
  - [ZAIApiError](#zaiapierror)
  - [ZAIAuthenticationError](#ziauthenticationerror)
  - [ZAIRateLimitError](#zairatelimiterror)
  - [ZAIInvalidRequestError](#zaiinvalidrequesterror)
  - [ZAIServerError](#zaiservererror)
- [Error Handling Patterns](#error-handling-patterns)
  - [Basic Error Handling](#basic-error-handling)
  - [Specific Exception Handling](#specific-exception-handling)
  - [Retry Logic](#retry-logic)
  - [Error Logging](#error-logging)
- [Common Error Scenarios](#common-error-scenarios)
  - [Authentication Errors](#authentication-errors)
  - [Rate Limit Errors](#rate-limit-errors)
  - [Invalid Request Errors](#invalid-request-errors)
  - [Server Errors](#server-errors)
  - [Network Errors](#network-errors)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

## Exception Hierarchy

The Z.AI Web Search Agent uses a structured exception hierarchy:

```
Exception
└── ZAIApiError
    ├── ZAIAuthenticationError
    ├── ZAIRateLimitError
    ├── ZAIInvalidRequestError
    └── ZAIServerError
```

All exceptions inherit from the base `ZAIApiError` class, which provides common functionality for error handling.

## Exception Types

### ZAIApiError

Base exception for Z.AI API errors.

**Attributes:**
- `message` (str): Error message
- `status_code` (Optional[int]): HTTP status code (if applicable)
- `response_data` (Optional[Dict[str, Any]]): Response data from the API (if applicable)

**Example:**
```python
from src.agent import ZAIApiError

try:
    # API call that might fail
    results = agent.search("test query")
except ZAIApiError as e:
    print(f"API Error: {e.message}")
    print(f"Status Code: {e.status_code}")
    print(f"Response Data: {e.response_data}")
```

### ZAIAuthenticationError

Raised when authentication with Z.AI API fails.

**Common Causes:**
- Invalid API key
- Expired API key
- Missing API key
- Incorrect API key format

**HTTP Status Code:** 401

**Example:**
```python
from src.agent import WebSearchAgent, ZAIAuthenticationError

try:
    agent = WebSearchAgent(api_key="invalid_key")
    results = agent.search("test query")
except ZAIAuthenticationError as e:
    print(f"Authentication failed: {e.message}")
    print(f"Status code: {e.status_code}")
    # Handle authentication error (e.g., prompt for new API key)
```

### ZAIRateLimitError

Raised when Z.AI API rate limit is exceeded.

**Common Causes:**
- Too many requests in a short time
- Exceeding quota limits
- Concurrent requests exceeding limits

**HTTP Status Code:** 429

**Special Features:**
- May include `retry_after` in `response_data` indicating when to retry

**Example:**
```python
from src.agent import WebSearchAgent, ZAIRateLimitError

try:
    agent = WebSearchAgent()
    # Make many requests rapidly
    for i in range(100):
        results = agent.search(f"query {i}")
except ZAIRateLimitError as e:
    print(f"Rate limit exceeded: {e.message}")
    
    # Check if retry-after is provided
    if e.response_data and 'retry_after' in e.response_data:
        retry_after = e.response_data['retry_after']
        print(f"Retry after {retry_after} seconds")
    else:
        print("Use exponential backoff for retry")
```

### ZAIInvalidRequestError

Raised when the request to Z.AI API is invalid.

**Common Causes:**
- Invalid search parameters
- Malformed request
- Missing required parameters
- Parameter validation errors

**HTTP Status Code:** 400

**Example:**
```python
from src.agent import WebSearchAgent, ZAIInvalidRequestError

try:
    agent = WebSearchAgent()
    # Invalid search type
    results = agent.search("test", search_type="invalid_type")
except ZAIInvalidRequestError as e:
    print(f"Invalid request: {e.message}")
    print(f"Status code: {e.status_code}")
    print(f"Response data: {e.response_data}")
    # Handle invalid request (e.g., fix parameters)
```

### ZAIServerError

Raised when the Z.AI API server encounters an error (5xx status codes).

**Common Causes:**
- Internal server errors
- Service unavailable
- Temporary server issues
- Maintenance downtime

**HTTP Status Codes:** 500-599

**Example:**
```python
from src.agent import WebSearchAgent, ZAIServerError

try:
    agent = WebSearchAgent()
    results = agent.search("test query")
except ZAIServerError as e:
    print(f"Server error: {e.message}")
    print(f"Status code: {e.status_code}")
    # Handle server error (e.g., retry later)
```

## Error Handling Patterns

### Basic Error Handling

```python
from src.agent import WebSearchAgent, ZAIApiError

agent = WebSearchAgent()

try:
    results = agent.search("your query here")
    # Process results
    print(f"Found {len(results.results)} results")
except ZAIApiError as e:
    # Handle any API error
    print(f"API error occurred: {e.message}")
    print(f"Status code: {e.status_code}")
```

### Specific Exception Handling

```python
from src.agent import (
    WebSearchAgent,
    ZAIAuthenticationError,
    ZAIRateLimitError,
    ZAIInvalidRequestError,
    ZAIServerError
)

agent = WebSearchAgent()

try:
    results = agent.search("your query here")
except ZAIAuthenticationError as e:
    print(f"Authentication failed: {e.message}")
    # Handle authentication (e.g., prompt for new API key)
except ZAIRateLimitError as e:
    print(f"Rate limit exceeded: {e.message}")
    # Handle rate limiting (e.g., wait and retry)
except ZAIInvalidRequestError as e:
    print(f"Invalid request: {e.message}")
    # Handle invalid request (e.g., fix parameters)
except ZAIServerError as e:
    print(f"Server error: {e.message}")
    # Handle server error (e.g., retry later)
```

### Retry Logic

The library includes built-in retry logic, but you may want to implement custom retry logic:

```python
import time
from src.agent import WebSearchAgent, ZAIServerError, ZAIRateLimitError

def search_with_retry(agent, query, max_retries=3):
    for attempt in range(max_retries):
        try:
            return agent.search(query)
        except (ZAIServerError, ZAIRateLimitError) as e:
            if attempt == max_retries - 1:
                raise  # Re-raise on last attempt
            
            # Calculate backoff time
            backoff_time = 2 ** attempt  # Exponential backoff
            
            # Use retry-after if available
            if e.response_data and 'retry_after' in e.response_data:
                backoff_time = e.response_data['retry_after']
            
            print(f"Attempt {attempt + 1} failed. Retrying in {backoff_time} seconds...")
            time.sleep(backoff_time)
    
    return None  # Should not reach here

# Usage
agent = WebSearchAgent()
results = search_with_retry(agent, "your query here")
```

### Error Logging

Implement comprehensive error logging:

```python
import logging
from src.agent import WebSearchAgent, ZAIApiError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def search_with_logging(agent, query):
    try:
        logger.info(f"Searching for: {query}")
        results = agent.search(query)
        logger.info(f"Found {len(results.results)} results")
        return results
    except ZAIApiError as e:
        logger.error(f"API error for query '{query}': {e.message}")
        logger.error(f"Status code: {e.status_code}")
        logger.error(f"Response data: {e.response_data}")
        raise  # Re-raise after logging

# Usage
agent = WebSearchAgent()
results = search_with_logging(agent, "your query here")
```

## Common Error Scenarios

### Authentication Errors

**Scenario:** Invalid or missing API key

```python
from src.agent import WebSearchAgent, ZAIAuthenticationError

def handle_authentication_error():
    try:
        agent = WebSearchAgent(api_key="invalid_key")
        results = agent.search("test query")
    except ZAIAuthenticationError as e:
        print(f"Authentication error: {e.message}")
        print("Please check your API key in the .env file")
        
        # Prompt for new API key
        new_key = input("Enter your API key: ")
        agent = WebSearchAgent(api_key=new_key)
        return agent
```

### Rate Limit Errors

**Scenario:** Too many requests in a short time

```python
import time
from src.agent import WebSearchAgent, ZAIRateLimitError

def handle_rate_limit_error(agent, queries):
    results = []
    for query in queries:
        while True:
            try:
                result = agent.search(query)
                results.append(result)
                break
            except ZAIRateLimitError as e:
                # Use retry-after if available
                if e.response_data and 'retry_after' in e.response_data:
                    wait_time = e.response_data['retry_after']
                else:
                    wait_time = 60  # Default wait time
                
                print(f"Rate limit exceeded. Waiting {wait_time} seconds...")
                time.sleep(wait_time)
    
    return results
```

### Invalid Request Errors

**Scenario:** Invalid search parameters

```python
from src.agent import WebSearchAgent, ZAIInvalidRequestError

def handle_invalid_request_error():
    agent = WebSearchAgent()
    
    try:
        # This will fail due to invalid search_type
        results = agent.search("test", search_type="invalid_type")
    except ZAIInvalidRequestError as e:
        print(f"Invalid request: {e.message}")
        
        # Fix the parameters and retry
        print("Retrying with valid parameters...")
        results = agent.search("test", search_type="web")
        return results
```

### Server Errors

**Scenario:** Temporary server issues

```python
import time
from src.agent import WebSearchAgent, ZAIServerError

def handle_server_error(agent, query, max_retries=3):
    for attempt in range(max_retries):
        try:
            return agent.search(query)
        except ZAIServerError as e:
            if attempt == max_retries - 1:
                print(f"Server error after {max_retries} attempts: {e.message}")
                raise
            
            wait_time = 2 ** attempt  # Exponential backoff
            print(f"Server error (attempt {attempt + 1}). Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
    
    return None
```

### Network Errors

**Scenario:** Network connectivity issues

```python
import requests
from src.agent import WebSearchAgent, ZAIApiError

def handle_network_error(agent, query):
    try:
        return agent.search(query)
    except ZAIApiError as e:
        # Check if it's a network-related error
        if "connection" in e.message.lower() or "timeout" in e.message.lower():
            print(f"Network error: {e.message}")
            print("Please check your internet connection")
            # Implement retry logic or notify user
        else:
            # Re-raise non-network errors
            raise
```

## Best Practices

### 1. Use Specific Exception Handling

Handle specific exceptions rather than catching the base `ZAIApiError`:

```python
# Good
try:
    results = agent.search(query)
except ZAIAuthenticationError as e:
    handle_auth_error(e)
except ZAIRateLimitError as e:
    handle_rate_limit(e)
except ZAIInvalidRequestError as e:
    handle_invalid_request(e)
except ZAIServerError as e:
    handle_server_error(e)

# Avoid this unless you have a generic handler
try:
    results = agent.search(query)
except ZAIApiError as e:
    handle_generic_error(e)
```

### 2. Implement Proper Logging

Log errors with sufficient context:

```python
import logging

logger = logging.getLogger(__name__)

try:
    results = agent.search(query)
except ZAIAuthenticationError as e:
    logger.error(f"Authentication failed for user {user_id}: {e.message}")
except ZAIRateLimitError as e:
    logger.warning(f"Rate limit exceeded for user {user_id}: {e.message}")
except ZAIInvalidRequestError as e:
    logger.error(f"Invalid request for user {user_id}: {e.message}")
    logger.error(f"Request parameters: {request_params}")
```

### 3. Provide User-Friendly Messages

Translate technical errors to user-friendly messages:

```python
def translate_error_to_user_message(error):
    if isinstance(error, ZAIAuthenticationError):
        return "Invalid API key. Please check your credentials."
    elif isinstance(error, ZAIRateLimitError):
        return "Too many requests. Please wait and try again."
    elif isinstance(error, ZAIInvalidRequestError):
        return "Invalid search parameters. Please check your input."
    elif isinstance(error, ZAIServerError):
        return "Server error. Please try again later."
    else:
        return "An error occurred. Please try again."
```

### 4. Implement Graceful Degradation

Handle errors gracefully without breaking the application:

```python
def search_with_fallback(query):
    try:
        # Primary search method
        return agent.search(query)
    except ZAIServerError:
        # Fallback to cached results
        return get_cached_results(query)
    except ZAIRateLimitError:
        # Fallback to limited results
        return agent.search(query, num_results=1)
```

### 5. Monitor Error Patterns

Track error patterns for proactive handling:

```python
from collections import defaultdict

error_counts = defaultdict(int)

def track_errors(error):
    error_type = type(error).__name__
    error_counts[error_type] += 1
    
    # Alert on high error rates
    if error_counts[error_type] > 10:
        send_alert(f"High error rate for {error_type}: {error_counts[error_type]}")
```

## Troubleshooting

### Common Issues and Solutions

#### 1. Authentication Errors

**Problem:** `ZAIAuthenticationError` occurs even with valid API key

**Solutions:**
- Verify API key format: `zai_[a-zA-Z0-9]{32}`
- Check for leading/trailing spaces in API key
- Ensure API key is not expired
- Verify API key permissions

#### 2. Rate Limit Errors

**Problem:** Frequent `ZAIRateLimitError` even with low request volume

**Solutions:**
- Check if multiple applications are using the same API key
- Implement proper rate limiting in your application
- Use the built-in rate limiter with appropriate settings
- Consider increasing time windows between requests

#### 3. Invalid Request Errors

**Problem:** `ZAIInvalidRequestError` with seemingly valid parameters

**Solutions:**
- Verify parameter values are within allowed ranges
- Check for proper data types (e.g., num_results as integer)
- Ensure search_type is one of: "web", "news", "images"
- Validate language and region codes (2-character ISO codes)

#### 4. Server Errors

**Problem:** Persistent `ZAIServerError` from API

**Solutions:**
- Check Z.AI API status page for service issues
- Implement retry logic with exponential backoff
- Consider using a different API endpoint if available
- Monitor error patterns and report issues

#### 5. Network Errors

**Problem:** Connection or timeout errors

**Solutions:**
- Check internet connectivity
- Verify firewall settings allow API access
- Increase timeout configuration if needed
- Implement retry logic for transient network issues

### Debug Mode

Enable debug logging to troubleshoot issues:

```python
import logging
from src.agent import WebSearchAgent

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

agent = WebSearchAgent()
results = agent.search("test query")
```

### Error Reporting

Report bugs or issues with the following information:

1. Exception type and message
2. HTTP status code (if available)
3. Response data (if available)
4. Request parameters (sanitized)
5. Library version
6. Python version
7. Operating system

Example error report format:

```
Exception: ZAIAuthenticationError
Message: Authentication failed. Please check your API key.
Status Code: 401
Response Data: {"error": "invalid_api_key"}
Request Parameters: {"query": "test", "num_results": 10}
Library Version: 0.1.0
Python Version: 3.9.0
Operating System: Windows 10