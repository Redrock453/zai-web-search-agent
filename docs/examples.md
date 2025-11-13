# Examples Guide

This document provides detailed examples of using the Z.AI Web Search Agent for various use cases.

## Table of Contents

- [Basic Usage Examples](#basic-usage-examples)
  - [Simple Search](#simple-search)
  - [Advanced Search](#advanced-search)
  - [Search with Request Model](#search-with-request-model)
  - [Configuration from Environment](#configuration-from-environment)
  - [Custom Configuration](#custom-configuration)
  - [Error Handling](#error-handling)
- [Async Usage Examples](#async-usage-examples)
  - [Basic Async Search](#basic-async-search)
  - [Concurrent Searches](#concurrent-searches)
  - [Sequential vs Concurrent](#sequential-vs-concurrent)
  - [Advanced Async Search](#advanced-async-search)
  - [Error Handling in Async](#error-handling-in-async)
  - [Rate Limiting in Async](#rate-limiting-in-async)
- [Batch Search Examples](#batch-search-examples)
  - [Basic Batch Search](#basic-batch-search)
  - [Advanced Batch Search](#advanced-batch-search)
  - [Sequential vs Concurrent](#sequential-vs-concurrent)
  - [Exporting Results](#exporting-results)
  - [Error Handling in Batch](#error-handling-in-batch)
- [Custom Agent Examples](#custom-agent-examples)
  - [Basic Custom Agent](#basic-custom-agent)
  - [Sentiment-based Search](#sentiment-based-search)
  - [Credibility-based Search](#credibility-based-search)
  - [Query Comparison](#query-comparison)
  - [Custom Configuration](#custom-configuration-1)

## Basic Usage Examples

### Simple Search

Perform a basic web search with minimal configuration:

```python
from src.agent import WebSearchAgent

# Initialize the agent
agent = WebSearchAgent()

# Perform a simple search
results = agent.search("latest developments in artificial intelligence")

# Display results
print(f"Found {len(results.results)} results in {results.search_time:.2f} seconds")

for i, result in enumerate(results.results[:3], 1):
    print(f"\n{i}. {result.title}")
    print(f"   URL: {result.url}")
    print(f"   Snippet: {result.snippet[:100]}...")
```

### Advanced Search

Perform a search with all available parameters:

```python
from src.agent import WebSearchAgent

# Initialize the agent with custom settings
agent = WebSearchAgent(
    max_retries=5,
    initial_backoff=2.0,
    max_backoff=30.0,
    rate_limit_requests=50,
    rate_limit_window=60
)

# Perform an advanced search
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

# Display detailed results
print(f"Search for '{results.query}'")
print(f"Type: {results.search_type}")
print(f"Total results available: {results.total_results}")
print(f"Results returned: {len(results.results)}")

for result in results.results:
    print(f"\n{result.title}")
    print(f"  URL: {result.url}")
    print(f"  Domain: {result.domain}")
    if result.published_date:
        print(f"  Published: {result.published_date}")
```

### Search with Request Model

Use the SearchRequest model for structured searches:

```python
from src.agent import WebSearchAgent, SearchRequest

# Initialize the agent
agent = WebSearchAgent()

# Create a search request
request = SearchRequest(
    query="renewable energy trends 2023",
    num_results=10,
    search_type="news",
    language="en",
    safe_search="moderate"
)

# Perform the search
results = agent.search_with_request(request)

# Process results
for result in results.results:
    print(f"{result.title}")
    print(f"  Published: {result.published_date}")
    print(f"  Snippet: {result.snippet[:100]}...")
```

### Configuration from Environment

Load configuration from environment variables:

```python
from src.agent import WebSearchAgent, ZAIConfig, ZAIAuthenticator

# Load configuration from environment
config = ZAIConfig.from_env()

# Create authenticator from config
authenticator = ZAIAuthenticator.from_config(config)

# Initialize agent with environment configuration
agent = WebSearchAgent(config=config, authenticator=authenticator)

# Perform search
results = agent.search("climate change solutions")
print(f"Found {len(results.results)} results")
```

### Custom Configuration

Create a custom configuration:

```python
from src.agent import WebSearchAgent, ZAIConfig, ZAIAuthenticator

# Create custom configuration
config = ZAIConfig(
    api_key="zai_your_api_key_here",
    base_url="https://api.z.ai/v1",
    timeout=45,
    max_retries=5
)

# Create authenticator
authenticator = ZAIAuthenticator.from_api_key("zai_your_api_key_here")

# Initialize agent with custom settings
agent = WebSearchAgent(
    config=config,
    authenticator=authenticator,
    max_retries=5,
    initial_backoff=1.5,
    max_backoff=45.0,
    rate_limit_requests=80,
    rate_limit_window=60
)

# Perform search
results = agent.search(
    "space exploration recent achievements",
    num_results=8,
    search_type="web",
    language="en"
)
```

### Error Handling

Implement comprehensive error handling:

```python
from src.agent import (
    WebSearchAgent,
    ZAIAuthenticationError,
    ZAIRateLimitError,
    ZAIInvalidRequestError,
    ZAIServerError,
    ZAIApiError
)

def search_with_error_handling(query):
    try:
        agent = WebSearchAgent()
        results = agent.search(query)
        
        print(f"Search completed successfully")
        print(f"Found {len(results.results)} results")
        return results
        
    except ZAIAuthenticationError as e:
        print(f"Authentication error: {e.message}")
        print("Please check your API key in the .env file")
    except ZAIRateLimitError as e:
        print(f"Rate limit error: {e.message}")
        print("Please wait before making more requests")
    except ZAIInvalidRequestError as e:
        print(f"Invalid request error: {e.message}")
        print("Please check your search parameters")
    except ZAIServerError as e:
        print(f"Server error: {e.message}")
        print("Please try again later")
    except ZAIApiError as e:
        print(f"API error: {e.message}")
    except Exception as e:
        print(f"Unexpected error: {e}")

# Usage
search_with_error_handling("artificial intelligence")
```

## Async Usage Examples

### Basic Async Search

Perform a basic async search:

```python
import asyncio
from examples.async_usage import AsyncWebSearchAgent
from src.agent import WebSearchAgent

async def basic_async_search():
    # Create agent and async wrapper
    agent = WebSearchAgent()
    async_agent = AsyncWebSearchAgent(agent)
    
    # Perform async search
    query = "latest developments in artificial intelligence"
    results = await async_agent.search(query)
    
    # Display results
    print(f"Async search for '{query}'")
    print(f"Found {len(results.results)} results")
    
    for result in results.results[:3]:
        print(f"\n{result.title}")
        print(f"  URL: {result.url}")
    
    # Clean up
    async_agent.close()

# Run the async function
asyncio.run(basic_async_search())
```

### Concurrent Searches

Perform multiple searches concurrently:

```python
import asyncio
from examples.async_usage import AsyncWebSearchAgent
from src.agent import WebSearchAgent

async def concurrent_searches():
    # Create agent and async wrapper
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
    tasks = [async_agent.search(query, num_results=5) for query in queries]
    results = await asyncio.gather(*tasks)
    
    # Display results
    for query, result in zip(queries, results):
        print(f"\nSearch: '{query}'")
        print(f"Results: {len(result.results)} items")
        if result.results:
            print(f"Top result: {result.results[0].title}")
    
    # Clean up
    async_agent.close()

# Run the async function
asyncio.run(concurrent_searches())
```

### Sequential vs Concurrent

Compare sequential vs concurrent performance:

```python
import asyncio
import time
from examples.async_usage import AsyncWebSearchAgent
from src.agent import WebSearchAgent

async def compare_performance():
    # Create agent and async wrapper
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
    print(f"Sequential: {sequential_time:.2f} seconds")
    print(f"Concurrent: {concurrent_time:.2f} seconds")
    print(f"Improvement: {sequential_time/concurrent_time:.2f}x faster")
    
    # Clean up
    async_agent.close()

# Run the async function
asyncio.run(compare_performance())
```

### Advanced Async Search

Advanced async search with custom parameters:

```python
import asyncio
from examples.async_usage import AsyncWebSearchAgent
from src.agent import WebSearchAgent, SearchRequest

async def advanced_async_search():
    # Create agent and async wrapper
    agent = WebSearchAgent()
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
    tasks = [async_agent.search_with_request(request) for request in requests]
    results = await asyncio.gather(*tasks)
    
    # Display results
    for request, result in zip(requests, results):
        print(f"\nSearch: '{request.query}'")
        print(f"Type: {request.search_type}")
        print(f"Results: {len(result.results)} items")
        print(f"Search time: {result.search_time:.2f} seconds")
    
    # Clean up
    async_agent.close()

# Run the async function
asyncio.run(advanced_async_search())
```

### Error Handling in Async

Handle errors in async operations:

```python
import asyncio
from examples.async_usage import AsyncWebSearchAgent
from src.agent import WebSearchAgent

async def async_error_handling():
    # Create agent and async wrapper
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
    
    # Process results
    for i, result in enumerate(results, 1):
        if isinstance(result, Exception):
            print(f"Task {i}: Failed with error: {str(result)}")
        else:
            print(f"Task {i}: Succeeded with {len(result.results)} results")
    
    # Clean up
    async_agent.close()

# Run the async function
asyncio.run(async_error_handling())
```

### Rate Limiting in Async

Handle rate limiting in async operations:

```python
import asyncio
import time
from examples.async_usage import AsyncWebSearchAgent
from src.agent import WebSearchAgent

async def async_rate_limiting():
    # Create agent with strict rate limiting
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
    
    print(f"Completed {len(queries)} searches in {end_time - start_time:.2f} seconds")
    
    # Clean up
    async_agent.close()

# Run the async function
asyncio.run(async_rate_limiting())
```

## Batch Search Examples

### Basic Batch Search

Process multiple searches in a batch:

```python
from examples.batch_search import BatchSearchProcessor, BatchSearchItem
from src.agent import WebSearchAgent

# Create agent and processor
agent = WebSearchAgent()
processor = BatchSearchProcessor(agent, max_workers=3)

# Define search items
items = [
    BatchSearchItem(id="1", query="artificial intelligence trends"),
    BatchSearchItem(id="2", query="machine learning applications"),
    BatchSearchItem(id="3", query="deep learning frameworks"),
    BatchSearchItem(id="4", query="natural language processing"),
    BatchSearchItem(id="5", query="computer vision applications")
]

# Process batch
results = processor.process_batch(items)

# Display results
successful = sum(1 for r in results if r.success)
failed = len(results) - successful

print(f"Processed {len(items)} searches")
print(f"Successful: {successful}")
print(f"Failed: {failed}")

for result in results:
    if result.success:
        print(f"\nID {result.item.id}: '{result.item.query}'")
        print(f"  Results: {len(result.results.results)} items")
        print(f"  Execution time: {result.execution_time:.2f} seconds")
    else:
        print(f"\nID {result.item.id}: '{result.item.query}' - FAILED")
        print(f"  Error: {result.error_message}")
```

### Advanced Batch Search

Process advanced batch searches with different types:

```python
from examples.batch_search import BatchSearchProcessor, BatchSearchItem
from src.agent import WebSearchAgent

# Create agent and processor
agent = WebSearchAgent()
processor = BatchSearchProcessor(agent, max_workers=5)

# Define search items with different types and parameters
items = [
    BatchSearchItem(
        id="web1",
        query="latest AI research",
        search_type="web",
        num_results=10,
        language="en",
        safe_search="moderate"
    ),
    BatchSearchItem(
        id="news1",
        query="artificial intelligence breakthrough",
        search_type="news",
        num_results=8,
        language="en",
        include_domains=["techcrunch.com", "wired.com", "arstechnica.com"]
    ),
    BatchSearchItem(
        id="web2",
        query="machine learning healthcare",
        search_type="web",
        num_results=5,
        language="en",
        include_domains=["nature.com", "science.org", "nejm.org"]
    ),
    BatchSearchItem(
        id="images1",
        query="AI generated art",
        search_type="images",
        num_results=5,
        safe_search="moderate"
    )
]

# Process batch
results = processor.process_batch(items)

# Display results
for result in results:
    if result.success:
        print(f"\nID {result.item.id}: '{result.item.query}' ({result.item.search_type})")
        print(f"  Results: {len(result.results.results)} items")
        print(f"  Execution time: {result.execution_time:.2f} seconds")
        print(f"  Search time: {result.results.search_time:.2f} seconds")
    else:
        print(f"\nID {result.item.id}: '{result.item.query}' - FAILED")
        print(f"  Error: {result.error_message}")
```

### Sequential vs Concurrent

Compare batch processing performance:

```python
from examples.batch_search import BatchSearchProcessor, BatchSearchItem
from src.agent import WebSearchAgent
import time

# Create agent and processor
agent = WebSearchAgent()
processor = BatchSearchProcessor(agent, max_workers=5)

# Define search items
items = [
    BatchSearchItem(id=f"search_{i}", query=f"artificial intelligence research paper {i+1}")
    for i in range(8)
]

# Sequential processing
print("Running batch search sequentially...")
sequential_start = time.time()
sequential_results = processor.process_batch_sequential(items)
sequential_end = time.time()
sequential_time = sequential_end - sequential_start

# Concurrent processing
print("Running batch search concurrently...")
concurrent_start = time.time()
concurrent_results = processor.process_batch(items)
concurrent_end = time.time()
concurrent_time = concurrent_end - concurrent_start

# Compare results
print(f"\nPerformance comparison:")
print(f"Sequential: {sequential_time:.2f} seconds")
print(f"Concurrent: {concurrent_time:.2f} seconds")
print(f"Improvement: {sequential_time/concurrent_time:.2f}x faster")

# Verify results
sequential_successful = sum(1 for r in sequential_results if r.success)
concurrent_successful = sum(1 for r in concurrent_results if r.success)

print(f"Sequential successful: {sequential_successful}/{len(items)}")
print(f"Concurrent successful: {concurrent_successful}/{len(items)}")
```

### Exporting Results

Export batch search results to different formats:

```python
from examples.batch_search import BatchSearchProcessor, BatchSearchItem
from src.agent import WebSearchAgent

# Create agent and processor
agent = WebSearchAgent()
processor = BatchSearchProcessor(agent, max_workers=3)

# Define search items
items = [
    BatchSearchItem(id="ai1", query="artificial intelligence ethics"),
    BatchSearchItem(id="ml1", query="machine learning algorithms"),
    BatchSearchItem(id="dl1", query="deep learning architectures"),
    BatchSearchItem(id="nlp1", query="natural language processing models")
]

# Process batch
results = processor.process_batch(items)

# Export to JSON
from examples.batch_search import export_to_json
export_to_json(results, "batch_search_results.json")
print("Results exported to batch_search_results.json")

# Export to CSV
from examples.batch_search import export_to_csv
export_to_csv(results, "batch_search_results.csv")
print("Results exported to batch_search_results.csv")

# Export summary to text
from examples.batch_search import export_summary_to_text
export_summary_to_text(results, "batch_search_summary.txt")
print("Summary exported to batch_search_summary.txt")
```

### Error Handling in Batch

Handle errors in batch operations:

```python
from examples.batch_search import BatchSearchProcessor, BatchSearchItem
from src.agent import WebSearchAgent

# Create agent and processor
agent = WebSearchAgent()
processor = BatchSearchProcessor(agent, max_workers=3)

# Define search items with some that will fail
items = [
    BatchSearchItem(id="valid1", query="artificial intelligence"),
    BatchSearchItem(id="invalid1", query="test", search_type="invalid_type"),  # Will fail
    BatchSearchItem(id="valid2", query="machine learning"),
    BatchSearchItem(id="invalid2", query="test", num_results=25),  # Will fail (too many results)
    BatchSearchItem(id="valid3", query="deep learning")
]

# Process batch
results = processor.process_batch(items)

# Display results
print(f"Processed {len(items)} searches with mixed success/failure:")

successful = 0
failed = 0

for result in results:
    if result.success:
        successful += 1
        print(f"  ✓ ID {result.item.id}: '{result.item.query}' - {len(result.results.results)} results")
    else:
        failed += 1
        print(f"  ✗ ID {result.item.id}: '{result.item.query}' - {result.error_message}")

print(f"\nSummary: {successful} successful, {failed} failed")

# Retry failed searches with corrected parameters
if failed > 0:
    print("\nRetrying failed searches with corrected parameters...")
    
    retry_items = []
    for result in results:
        if not result.success:
            item = result.item
            
            # Fix the issues
            if item.search_type == "invalid_type":
                item.search_type = "web"
            if item.num_results > 20:
                item.num_results = 10
            
            retry_items.append(item)
    
    # Retry the failed searches
    retry_results = processor.process_batch(retry_items)
    
    for result in retry_results:
        if result.success:
            print(f"  ✓ Retry ID {result.item.id}: '{result.item.query}' - {len(result.results.results)} results")
        else:
            print(f"  ✗ Retry ID {result.item.id}: '{result.item.query}' - {result.error_message}")
```

## Custom Agent Examples

### Basic Custom Agent

Use the custom agent with enhanced functionality:

```python
from examples.custom_agent import CustomWebSearchAgent

# Initialize the custom agent
agent = CustomWebSearchAgent()

# Perform an enhanced search
query = "artificial intelligence in healthcare"
enhanced_results, summary = agent.search_with_enhancement(query, num_results=5)

# Display summary
print(f"Search summary for '{query}':")
print(f"  Total results available: {summary.total_results}")
print(f"  Results returned: {summary.results_count}")
print(f"  Search time: {summary.search_time:.2f} seconds")
print(f"  Execution time: {summary.execution_time:.2f} seconds")
print(f"  Average word count: {summary.average_word_count:.0f}")
print(f"  Average reading time: {summary.average_reading_time:.1f} minutes")

# Display sentiment distribution
print(f"\nSentiment distribution:")
for sentiment, count in summary.sentiment_distribution.items():
    print(f"  {sentiment}: {count}")

# Display enhanced results
print(f"\nEnhanced results:")
for result in enhanced_results[:3]:
    print(f"\n  {result.title}")
    print(f"    URL: {result.url}")
    print(f"    Content type: {result.content_type}")
    print(f"    Credibility score: {result.credibility_score:.2f}")
    print(f"    Sentiment score: {result.sentiment_score:.2f}")
    print(f"    Reading time: {result.reading_time_minutes:.1f} minutes")
    print(f"    Key phrases: {', '.join(result.key_phrases[:3])}")
    print(f"    Snippet: {result.snippet[:100]}...")
```

### Sentiment-based Search

Search and filter results by sentiment:

```python
from examples.custom_agent import CustomWebSearchAgent

# Initialize the custom agent
agent = CustomWebSearchAgent()

query = "climate change"

# Search for positive sentiment results
print(f"Searching for positive sentiment results for '{query}':")
positive_results = agent.search_by_sentiment(query, sentiment="positive", num_results=3)

for result in positive_results:
    print(f"\n  {result.title}")
    print(f"    Sentiment score: {result.sentiment_score:.2f}")
    print(f"    Snippet: {result.snippet[:100]}...")

# Search for negative sentiment results
print(f"\nSearching for negative sentiment results for '{query}':")
negative_results = agent.search_by_sentiment(query, sentiment="negative", num_results=3)

for result in negative_results:
    print(f"\n  {result.title}")
    print(f"    Sentiment score: {result.sentiment_score:.2f}")
    print(f"    Snippet: {result.snippet[:100]}...")
```

### Credibility-based Search

Search and filter results by credibility score:

```python
from examples.custom_agent import CustomWebSearchAgent

# Initialize the custom agent
agent = CustomWebSearchAgent()

query = "medical research"

# Search for high credibility results
print(f"Searching for high credibility results for '{query}':")
credible_results = agent.search_by_credibility(query, min_credibility=0.8, num_results=5)

for result in credible_results:
    print(f"\n  {result.title}")
    print(f"    Domain: {result.domain}")
    print(f"    Credibility score: {result.credibility_score:.2f}")
    print(f"    Content type: {result.content_type}")
    print(f"    Snippet: {result.snippet[:100]}...")
```

### Query Comparison

Compare multiple queries:

```python
from examples.custom_agent import CustomWebSearchAgent

# Initialize the custom agent
agent = CustomWebSearchAgent()

# Define queries to compare
queries = [
    "artificial intelligence",
    "machine learning",
    "deep learning"
]

# Compare queries
comparison = agent.compare_queries(queries, num_results=5)

# Display comparison
for query, (results, summary) in comparison.items():
    print(f"\nQuery: '{query}'")
    print(f"  Results: {summary.results_count}")
    print(f"  Average reading time: {summary.average_reading_time:.1f} minutes")
    print(f"  Top domains: {', '.join([domain for domain, _ in summary.top_domains[:3]])}")
    print(f"  Key topics: {', '.join(summary.key_topics[:5])}")
    
    # Show sentiment distribution
    total = sum(summary.sentiment_distribution.values())
    if total > 0:
        positive_pct = summary.sentiment_distribution["positive"] / total * 100
        print(f"  Positive sentiment: {positive_pct:.0f}%")
```

### Custom Configuration

Use custom configuration with the custom agent:

```python
from examples.custom_agent import CustomWebSearchAgent
from src.agent import ZAIConfig

# Create custom configuration
config = ZAIConfig.from_env()

# Initialize the custom agent with custom settings
agent = CustomWebSearchAgent(
    config=config,
    max_retries=5,
    initial_backoff=1.5,
    max_backoff=30.0,
    rate_limit_requests=50,
    rate_limit_window=60
)

# Customize agent settings
agent.enable_result_enhancement = True
agent.enable_analytics = True
agent.reading_speed_wpm = 250  # Faster reading speed

# Add custom domain credibility scores
agent.domain_credibility.update({
    "custom-domain.com": 0.95,
    "another-domain.org": 0.80
})

# Perform search with custom configuration
query = "quantum computing"
enhanced_results, summary = agent.search_with_enhancement(query, num_results=3)

# Display results
print(f"Custom search for '{query}':")
print(f"  Custom reading speed: {agent.reading_speed_wpm} WPM")
print(f"  Results: {summary.results_count}")

for result in enhanced_results:
    print(f"\n  {result.title}")
    print(f"    Credibility score: {result.credibility_score:.2f}")
    print(f"    Reading time: {result.reading_time_minutes:.1f} minutes")
```

## Running the Examples

All example files can be run directly from the command line:

```bash
# Basic usage examples
python examples/basic_usage.py

# Async usage examples
python examples/async_usage.py

# Batch search examples
python examples/batch_search.py

# Custom agent examples
python examples/custom_agent.py
```

## Tips for Using Examples

1. **Set up API Key**: Make sure to set your `ZAI_API_KEY` in the `.env` file before running examples
2. **Review Output**: Examples print detailed output to help understand the API responses
3. **Modify Parameters**: Feel free to modify search parameters to explore different use cases
4. **Error Handling**: Pay attention to error handling patterns used in examples
5. **Performance**: Compare sequential vs concurrent performance for your use case
6. **Export Results**: Use the export functionality to save search results for further analysis
7. **Custom Extensions**: Use the custom agent example as a starting point for your own extensions