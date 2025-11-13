# Async usage example for the Z.AI Web Search Agent
# This file demonstrates how to use the web search agent with asyncio

import os
import sys
import asyncio
import time
from typing import List, Dict, Any
from concurrent.futures import ThreadPoolExecutor

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


class AsyncWebSearchAgent:
    """
    Wrapper class to add async capabilities to the WebSearchAgent
    """
    
    def __init__(self, agent: WebSearchAgent):
        """
        Initialize the async wrapper with a WebSearchAgent instance
        
        Args:
            agent: WebSearchAgent instance to wrap
        """
        self.agent = agent
        self.executor = ThreadPoolExecutor(max_workers=5)
    
    async def search(self, *args, **kwargs) -> Any:
        """
        Async wrapper for the search method
        
        Args:
            *args: Positional arguments to pass to search
            **kwargs: Keyword arguments to pass to search
            
        Returns:
            SearchResponse object
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            self.executor, 
            lambda: self.agent.search(*args, **kwargs)
        )
    
    async def search_with_request(self, request: SearchRequest) -> Any:
        """
        Async wrapper for the search_with_request method
        
        Args:
            request: SearchRequest model with all search parameters
            
        Returns:
            SearchResponse object
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            self.executor, 
            lambda: self.agent.search_with_request(request)
        )
    
    def close(self):
        """Close the thread pool executor"""
        self.executor.shutdown(wait=True)


async def basic_async_search_example():
    """
    Example of a basic async search
    """
    print("=== Basic Async Search Example ===")
    
    try:
        # Initialize the agent
        agent = WebSearchAgent()
        async_agent = AsyncWebSearchAgent(agent)
        
        # Example search query
        query = "latest developments in artificial intelligence"
        
        # Perform the async search
        start_time = time.time()
        results = await async_agent.search(query)
        end_time = time.time()
        
        # Display results
        print(f"Async search for '{query}' completed in {end_time - start_time:.2f} seconds")
        print(f"Found {len(results.results)} results in {results.search_time:.2f} seconds")
        
        for i, result in enumerate(results.results[:3], 1):  # Show first 3 results
            print(f"\n{i}. {result.title}")
            print(f"   URL: {result.url}")
            print(f"   Snippet: {result.snippet[:100]}...")
        
        # Clean up
        async_agent.close()
        
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


async def concurrent_searches_example():
    """
    Example of running multiple searches concurrently
    """
    print("\n=== Concurrent Searches Example ===")
    
    try:
        # Initialize the agent
        agent = WebSearchAgent()
        async_agent = AsyncWebSearchAgent(agent)
        
        # Define multiple search queries
        queries = [
            "machine learning in healthcare",
            "renewable energy trends",
            "space exploration missions",
            "quantum computing breakthroughs",
            "climate change solutions"
        ]
        
        # Create tasks for concurrent execution
        start_time = time.time()
        tasks = [async_agent.search(query, num_results=5) for query in queries]
        results = await asyncio.gather(*tasks)
        end_time = time.time()
        
        # Display results
        print(f"Completed {len(queries)} searches concurrently in {end_time - start_time:.2f} seconds")
        
        for i, (query, result) in enumerate(zip(queries, results), 1):
            print(f"\n{i}. Search: '{query}'")
            print(f"   Results: {len(result.results)} items")
            if result.results:
                print(f"   Top result: {result.results[0].title}")
        
        # Clean up
        async_agent.close()
        
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


async def sequential_vs_concurrent_example():
    """
    Example comparing sequential vs concurrent search performance
    """
    print("\n=== Sequential vs Concurrent Performance Example ===")
    
    try:
        # Initialize the agent
        agent = WebSearchAgent()
        async_agent = AsyncWebSearchAgent(agent)
        
        # Define search queries
        queries = [
            "artificial intelligence ethics",
            "blockchain technology applications",
            "gene editing research",
            "nanotechnology innovations"
        ]
        
        # Sequential execution
        print("Running searches sequentially...")
        sequential_start = time.time()
        sequential_results = []
        for query in queries:
            result = await async_agent.search(query, num_results=5)
            sequential_results.append(result)
        sequential_end = time.time()
        sequential_time = sequential_end - sequential_start
        
        # Concurrent execution
        print("Running searches concurrently...")
        concurrent_start = time.time()
        tasks = [async_agent.search(query, num_results=5) for query in queries]
        concurrent_results = await asyncio.gather(*tasks)
        concurrent_end = time.time()
        concurrent_time = concurrent_end - concurrent_start
        
        # Compare results
        print(f"\nPerformance comparison:")
        print(f"Sequential execution time: {sequential_time:.2f} seconds")
        print(f"Concurrent execution time: {concurrent_time:.2f} seconds")
        print(f"Performance improvement: {sequential_time/concurrent_time:.2f}x faster")
        
        # Verify results are the same
        results_match = True
        for seq_result, conc_result in zip(sequential_results, concurrent_results):
            if seq_result.query != conc_result.query or len(seq_result.results) != len(conc_result.results):
                results_match = False
                break
        
        print(f"Results match: {results_match}")
        
        # Clean up
        async_agent.close()
        
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


async def advanced_async_search_example():
    """
    Example of advanced async search with custom parameters
    """
    print("\n=== Advanced Async Search Example ===")
    
    try:
        # Create a custom configuration
        config = ZAIConfig.from_env()
        
        # Initialize the agent with custom settings
        agent = WebSearchAgent(
            config=config,
            max_retries=5,
            initial_backoff=1.5,
            max_backoff=30.0,
            rate_limit_requests=50,
            rate_limit_window=60
        )
        async_agent = AsyncWebSearchAgent(agent)
        
        # Create search requests with different parameters
        requests = [
            SearchRequest(
                query="machine learning applications",
                num_results=10,
                search_type="web",
                language="en",
                safe_search="moderate"
            ),
            SearchRequest(
                query="latest AI research papers",
                num_results=8,
                search_type="news",
                language="en",
                include_domains=["arxiv.org", "nature.com", "science.org"]
            ),
            SearchRequest(
                query="artificial intelligence images",
                num_results=5,
                search_type="images",
                safe_search="moderate"
            )
        ]
        
        # Execute searches concurrently
        start_time = time.time()
        tasks = [async_agent.search_with_request(request) for request in requests]
        results = await asyncio.gather(*tasks)
        end_time = time.time()
        
        # Display results
        print(f"Completed {len(requests)} advanced searches in {end_time - start_time:.2f} seconds")
        
        for i, (request, result) in enumerate(zip(requests, results), 1):
            print(f"\n{i}. Search: '{request.query}'")
            print(f"   Type: {request.search_type}")
            print(f"   Results: {len(result.results)} items")
            print(f"   Search time: {result.search_time:.2f} seconds")
            if result.results:
                print(f"   Top result: {result.results[0].title}")
        
        # Clean up
        async_agent.close()
        
    except ZAIAuthenticationError as e:
        print(f"Authentication error: {e.message}")
        print("Please check your API key in the .env file")
    except ZAIRateLimitError as e:
        print(f"Rate limit error: {e.message}")
    except ZAIInvalidRequestError as e:
        print(f"Invalid request error: {e.message}")
    except ZAIApiError as e:
        print(f"API error: {e.message}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


async def error_handling_async_example():
    """
    Example of error handling in async operations
    """
    print("\n=== Async Error Handling Example ===")
    
    # Example 1: Handling authentication errors
    try:
        agent = WebSearchAgent(api_key="invalid_key")
        async_agent = AsyncWebSearchAgent(agent)
        
        await async_agent.search("test query")
        async_agent.close()
    except ZAIAuthenticationError as e:
        print(f"Caught authentication error: {e.message}")
        print(f"Status code: {e.status_code}")
    
    # Example 2: Handling invalid request parameters
    try:
        agent = WebSearchAgent()
        async_agent = AsyncWebSearchAgent(agent)
        
        # This will raise an error due to invalid search_type
        await async_agent.search("test", search_type="invalid_type")
        async_agent.close()
    except ZAIInvalidRequestError as e:
        print(f"Caught invalid request error: {e.message}")
        print(f"Status code: {e.status_code}")
    
    # Example 3: Handling errors in concurrent operations
    try:
        agent = WebSearchAgent()
        async_agent = AsyncWebSearchAgent(agent)
        
        # Mix of valid and invalid requests
        tasks = [
            async_agent.search("valid query"),
            async_agent.search("another valid query"),
            async_agent.search("invalid query", search_type="invalid_type")  # This will fail
        ]
        
        # Use asyncio.gather with return_exceptions=True to handle individual failures
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        print(f"Processed {len(results)} tasks with mixed success/failure:")
        for i, result in enumerate(results, 1):
            if isinstance(result, Exception):
                print(f"  Task {i}: Failed with error: {str(result)}")
            else:
                print(f"  Task {i}: Succeeded with {len(result.results)} results")
        
        async_agent.close()
    except Exception as e:
        print(f"Unexpected error in concurrent operations: {e}")


async def rate_limiting_async_example():
    """
    Example demonstrating rate limiting in async operations
    """
    print("\n=== Async Rate Limiting Example ===")
    
    try:
        # Initialize the agent with strict rate limiting
        agent = WebSearchAgent(
            rate_limit_requests=5,  # Only 5 requests per minute
            rate_limit_window=60
        )
        async_agent = AsyncWebSearchAgent(agent)
        
        # Define many search queries
        queries = [f"search query {i+1}" for i in range(10)]
        
        # Execute searches concurrently (will be rate limited)
        print(f"Executing {len(queries)} searches with rate limit of 5 requests/minute...")
        start_time = time.time()
        
        tasks = [async_agent.search(query, num_results=3) for query in queries]
        results = await asyncio.gather(*tasks)
        
        end_time = time.time()
        
        # Display results
        print(f"Completed {len(queries)} searches in {end_time - start_time:.2f} seconds")
        print("Note: The agent automatically handles rate limiting with exponential backoff")
        
        for i, result in enumerate(results[:3], 1):
            print(f"  Search {i}: '{result.query}' - {len(result.results)} results")
        
        # Clean up
        async_agent.close()
        
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


async def main():
    """
    Run all async examples
    """
    print("Z.AI Web Search Agent - Async Usage Examples")
    print("=" * 50)
    
    # Run all examples
    await basic_async_search_example()
    await concurrent_searches_example()
    await sequential_vs_concurrent_example()
    await advanced_async_search_example()
    await error_handling_async_example()
    await rate_limiting_async_example()
    
    print("\n" + "=" * 50)
    print("Async examples completed!")
    print("\nNote: Some examples may fail if you don't have a valid API key configured.")
    print("Please set your ZAI_API_KEY in the .env file or in your environment variables.")


if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())