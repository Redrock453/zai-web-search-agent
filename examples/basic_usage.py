# Basic usage example for the Z.AI Web Search Agent
# This file demonstrates how to use the web search agent with various configurations

import os
import sys
from typing import Optional

# Add the parent directory to the path so we can import the agent module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agent import (
    WebSearchAgent, 
    ZAIConfig, 
    ZAIAuthenticator,
    SearchRequest,
    ZAIAuthenticationError,
    ZAIRateLimitError,
    ZAIInvalidRequestError,
    ZAIApiError
)


def basic_search_example():
    """
    Example of a basic search using default configuration
    """
    print("=== Basic Search Example ===")
    
    try:
        # Initialize the agent with default configuration
        agent = WebSearchAgent()
        
        # Example search query
        query = "latest developments in artificial intelligence"
        
        # Perform the search
        results = agent.search(query)
        
        # Display results
        print(f"Search results for '{query}':")
        print(f"Found {len(results.results)} results in {results.search_time:.2f} seconds")
        
        for i, result in enumerate(results.results[:3], 1):  # Show first 3 results
            print(f"\n{i}. {result.title}")
            print(f"   URL: {result.url}")
            print(f"   Snippet: {result.snippet[:100]}...")
            print(f"   Domain: {result.domain}")
        
    except ZAIAuthenticationError as e:
        print(f"Authentication error: {e.message}")
        print("Please check your API key in the .env file")
    except ZAIRateLimitError as e:
        print(f"Rate limit error: {e.message}")
        print("Please wait before making more requests")
    except ZAIInvalidRequestError as e:
        print(f"Invalid request error: {e.message}")
        print("Please check your search parameters")
    except ZAIApiError as e:
        print(f"API error: {e.message}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def advanced_search_example():
    """
    Example of an advanced search with all parameters
    """
    print("\n=== Advanced Search Example ===")
    
    try:
        # Initialize the agent with custom configuration
        agent = WebSearchAgent(
            max_retries=5,
            initial_backoff=2.0,
            max_backoff=30.0,
            rate_limit_requests=50,
            rate_limit_window=60
        )
        
        # Perform an advanced search with all parameters
        results = agent.search(
            query="machine learning applications in healthcare",
            num_results=15,
            include_domains=["nature.com", "science.org", "nejm.org"],
            exclude_domains=["spam.com", "fake-news.com"],
            search_type="web",
            language="en",
            region="us",
            safe_search="moderate"
        )
        
        # Display results
        print(f"Advanced search for '{results.query}'")
        print(f"Search type: {results.search_type}")
        print(f"Total results available: {results.total_results}")
        print(f"Results returned: {len(results.results)}")
        print(f"Search time: {results.search_time:.2f} seconds")
        print(f"Has more results: {results.has_more}")
        
        # Show first result with all details
        if results.results:
            result = results.results[0]
            print(f"\nFirst result details:")
            print(f"  Title: {result.title}")
            print(f"  URL: {result.url}")
            print(f"  Snippet: {result.snippet}")
            print(f"  Position: {result.position}")
            print(f"  Domain: {result.domain}")
            if result.published_date:
                print(f"  Published: {result.published_date}")
            if result.thumbnail_url:
                print(f"  Thumbnail: {result.thumbnail_url}")
        
    except ZAIAuthenticationError as e:
        print(f"Authentication error: {e.message}")
    except ZAIRateLimitError as e:
        print(f"Rate limit error: {e.message}")
    except ZAIInvalidRequestError as e:
        print(f"Invalid request error: {e.message}")
    except ZAIApiError as e:
        print(f"API error: {e.message}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def search_with_request_model_example():
    """
    Example using the SearchRequest model
    """
    print("\n=== Search with Request Model Example ===")
    
    try:
        # Initialize the agent
        agent = WebSearchAgent()
        
        # Create a search request model
        request = SearchRequest(
            query="renewable energy trends 2023",
            num_results=10,
            search_type="news",
            language="en",
            safe_search="moderate"
        )
        
        # Perform the search using the request model
        results = agent.search_with_request(request)
        
        # Display results
        print(f"News search for '{results.query}'")
        print(f"Found {len(results.results)} news articles")
        
        for i, result in enumerate(results.results[:3], 1):
            print(f"\n{i}. {result.title}")
            print(f"   URL: {result.url}")
            if result.published_date:
                print(f"   Published: {result.published_date}")
            print(f"   Snippet: {result.snippet[:100]}...")
        
    except ZAIAuthenticationError as e:
        print(f"Authentication error: {e.message}")
    except ZAIRateLimitError as e:
        print(f"Rate limit error: {e.message}")
    except ZAIInvalidRequestError as e:
        print(f"Invalid request error: {e.message}")
    except ZAIApiError as e:
        print(f"API error: {e.message}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def configuration_from_env_example():
    """
    Example of loading configuration from environment variables
    """
    print("\n=== Configuration from Environment Example ===")
    
    try:
        # Load configuration from environment variables
        config = ZAIConfig.from_env()
        
        # Create an authenticator from the config
        authenticator = ZAIAuthenticator.from_config(config)
        
        # Initialize the agent with the config and authenticator
        agent = WebSearchAgent(config=config, authenticator=authenticator)
        
        # Perform a search
        results = agent.search("climate change solutions")
        
        # Display results
        print(f"Search using environment configuration")
        print(f"Found {len(results.results)} results")
        
        for i, result in enumerate(results.results[:2], 1):
            print(f"\n{i}. {result.title}")
            print(f"   URL: {result.url}")
            print(f"   Snippet: {result.snippet[:100]}...")
        
    except ZAIAuthenticationError as e:
        print(f"Authentication error: {e.message}")
        print("Please set your ZAI_API_KEY in the .env file")
    except Exception as e:
        print(f"An error occurred: {e}")


def custom_configuration_example():
    """
    Example of creating a custom configuration
    """
    print("\n=== Custom Configuration Example ===")
    
    try:
        # Create a custom configuration
        config = ZAIConfig(
            api_key="zai_your_api_key_here",  # Replace with actual API key
            base_url="https://api.z.ai/v1",
            timeout=45,
            max_retries=5
        )
        
        # Create an authenticator with API key
        authenticator = ZAIAuthenticator.from_api_key("zai_your_api_key_here")  # Replace with actual API key
        
        # Initialize the agent with custom settings
        agent = WebSearchAgent(
            config=config,
            authenticator=authenticator,
            max_retries=5,
            initial_backoff=1.5,
            max_backoff=45.0,
            rate_limit_requests=80,
            rate_limit_window=60
        )
        
        # Perform a search
        results = agent.search(
            "space exploration recent achievements",
            num_results=8,
            search_type="web",
            language="en"
        )
        
        # Display results
        print(f"Search with custom configuration")
        print(f"API endpoint: {config.base_url}")
        print(f"Timeout: {config.timeout} seconds")
        print(f"Max retries: {config.max_retries}")
        print(f"Results found: {len(results.results)}")
        
        for i, result in enumerate(results.results[:2], 1):
            print(f"\n{i}. {result.title}")
            print(f"   URL: {result.url}")
            print(f"   Snippet: {result.snippet[:100]}...")
        
    except ZAIAuthenticationError as e:
        print(f"Authentication error: {e.message}")
        print("Please replace 'zai_your_api_key_here' with your actual API key")
    except Exception as e:
        print(f"An error occurred: {e}")


def error_handling_example():
    """
    Example demonstrating error handling
    """
    print("\n=== Error Handling Example ===")
    
    # Example 1: Invalid API key
    try:
        agent = WebSearchAgent(api_key="invalid_key")
        results = agent.search("test query")
    except ZAIAuthenticationError as e:
        print(f"Caught authentication error: {e.message}")
        print(f"Status code: {e.status_code}")
    
    # Example 2: Invalid request parameters
    try:
        agent = WebSearchAgent()
        # This will raise an error due to invalid search_type
        results = agent.search("test", search_type="invalid_type")
    except ZAIInvalidRequestError as e:
        print(f"Caught invalid request error: {e.message}")
        print(f"Status code: {e.status_code}")
    
    # Example 3: Handling rate limit errors
    try:
        agent = WebSearchAgent()
        # Simulate a rate limit scenario (this would normally happen with many requests)
        print("Note: Rate limit errors typically occur after many rapid requests")
        print("The agent automatically handles rate limiting with exponential backoff")
    except ZAIRateLimitError as e:
        print(f"Caught rate limit error: {e.message}")
        print(f"Status code: {e.status_code}")
        if e.response_data and 'retry_after' in e.response_data:
            print(f"Retry after: {e.response_data['retry_after']} seconds")


def main():
    """
    Run all examples
    """
    print("Z.AI Web Search Agent - Basic Usage Examples")
    print("=" * 50)
    
    # Run all examples
    basic_search_example()
    advanced_search_example()
    search_with_request_model_example()
    configuration_from_env_example()
    custom_configuration_example()
    error_handling_example()
    
    print("\n" + "=" * 50)
    print("Examples completed!")
    print("\nNote: Some examples may fail if you don't have a valid API key configured.")
    print("Please set your ZAI_API_KEY in the .env file or in your environment variables.")


if __name__ == "__main__":
    main()