# Z.AI Web Search Agent 🔍

A Python client for interacting with the Z.AI web search API, providing a simple and powerful interface for performing web searches with advanced features like rate limiting, retry logic, and comprehensive error handling.

## ✨ Features

- **🎯 Simple API**: Easy-to-use interface for web searches
- **🔄 Multiple Search Types**: Support for web, news, and image searches
- **🎨 Advanced Filtering**: Include/exclude domains, language and region filtering
- **⚡ Rate Limiting**: Built-in token bucket algorithm for API rate limiting
- **🔁 Retry Logic**: Automatic retries with exponential backoff for failed requests
- **🛡️ Error Handling**: Comprehensive error handling with specific exception types
- **⚙️ Async Support**: Asyncio-compatible wrapper for concurrent operations
- **📦 Batch Processing**: Efficient processing of multiple search queries
- **🔌 Extensible**: Easy to extend with custom functionality
- **📝 YAML Configuration**: Configure through YAML files for easy integration
- **🌐 REST API**: Built-in REST API server for cross-language integration
- **💻 VS Code Integration**: Full VS Code support with tasks, debugging, and snippets
- **🎨 Kilo Code Ready**: Pre-configured for Kilo Code integration

## 📥 Installation

### Option 1: Standard Installation

1. Clone this repository:
```bash
git clone https://github.com/your-username/zai-web-search-agent.git
cd zai-web-search-agent
```

2. Install dependencies:
```bash
pip install -r requirements.txt
pip install -r requirements-yaml.txt  # For YAML support
```

### Option 2: VS Code Integration (Recommended)

1. **Open in VS Code**:
   ```bash
   code c:\zai-web-search-agent
   ```

2. **Install recommended extensions** (VS Code will prompt automatically)

3. **Install dependencies**:
   - Press `Ctrl+Shift+B`
   - Select "Install Dependencies"
   - Done!

4. **Set up API key**:
   Create `.env` file:
   ```env
   ZAI_API_KEY=your_api_key_here
   ```

5. **Test the integration**:
   - Press `Ctrl+Shift+B`
   - Select "Quick Search (Interactive)"
   - Enter a query and see results!

See [VSCODE_INTEGRATION.md](VSCODE_INTEGRATION.md) for complete VS Code setup guide.

### Option 3: Quick Setup Script

```powershell
# Windows PowerShell
cd c:\zai-web-search-agent
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt -r requirements-yaml.txt
echo "ZAI_API_KEY=your_key_here" > .env
```

3. Set up your environment variables:
```bash
cp .env.example .env
# Edit .env with your actual API credentials
```

## 🚀 Quick Start

### Method 1: Direct Python Usage

```python
from src.agent import WebSearchAgent

# Initialize the agent with default configuration
agent = WebSearchAgent()

# Perform a simple search
results = agent.search("latest developments in artificial intelligence")
print(f"Found {len(results.results)} results")

# Display first result
if results.results:
    result = results.results[0]
    print(f"Title: {result.title}")
    print(f"URL: {result.url}")
    print(f"Snippet: {result.snippet}")
```

### Method 2: YAML Configuration (Recommended for Kilo Code)

```python
from integrations.yaml_loader import load_agent_from_yaml

# Load agent from YAML config
agent = load_agent_from_yaml('config/kilo_code.yaml')

# Perform search
response = agent.search("Python programming", num_results=5)
for result in response.results:
    print(f"{result.title} - {result.url}")
```

### Method 3: Quick Functions

```python
from integrations import init_search, quick_search

# Initialize once
init_search()

# Use anywhere
results = quick_search("machine learning", num_results=5)
print(results)
```

### Method 4: REST API Server

```bash
# Start server
python integrations/kilo_code_api.py

# Make requests
curl -X POST http://localhost:5000/api/search \
     -H "Content-Type: application/json" \
     -d '{"query": "Python", "num_results": 5}'
```

## 💻 VS Code Integration

This project comes with full VS Code integration:

### Tasks (Ctrl+Shift+B)
- **Start Z.AI Search Agent** - Launch API server
- **Test Search Agent** - Run tests
- **Run Kilo Code Examples** - Run integration examples
- **Quick Search (Interactive)** - Interactive search in terminal
- **Install Dependencies** - Install all requirements

### Debug Configurations (F5)
- **Z.AI Search API Server** - Debug API server
- **Run Kilo Code Example** - Debug examples
- **Run Tests** - Debug tests
- **Run Current File** - Debug active file

### Code Snippets
- `zai-search` - Quick search template
- `zai-yaml` - YAML loader template
- `zai-integration` - Full integration template
- `zai-batch` - Batch search template
- `zai-config` - Config loader template
- `zai-test` - Test template

See [`.vscode/README.md`](.vscode/README.md) for details.

## 📝 Configuration

### Environment Variables

Create a `.env` file in the project root with the following variables:

```env
ZAI_API_KEY=your_api_key_here
ZAI_BASE_URL=https://api.z.ai/v1
ZAI_TIMEOUT=30
ZAI_MAX_RETRIES=3
```

### Programmatic Configuration

```python
from src.agent import WebSearchAgent, ZAIConfig, ZAIAuthenticator

# Create a custom configuration
config = ZAIConfig(
    api_key="your_api_key_here",
    base_url="https://api.z.ai/v1",
    timeout=30,
    max_retries=3
)

# Create an authenticator
authenticator = ZAIAuthenticator.from_config(config)

# Initialize the agent with custom configuration
agent = WebSearchAgent(
    config=config,
    authenticator=authenticator,
    max_retries=5,
    initial_backoff=1.5,
    max_backoff=30.0,
    rate_limit_requests=50,
    rate_limit_window=60
)
```

## API Reference

### WebSearchAgent

The main class for interacting with the Z.AI web search API.

#### Methods

##### `search(query, num_results=10, include_domains=None, exclude_domains=None, search_type="web", language=None, region=None, safe_search="moderate")`

Perform a web search with the specified parameters.

**Parameters:**
- `query` (str): Search query string (required)
- `num_results` (int): Number of results to return (1-20, default: 10)
- `include_domains` (list): List of domains to include in search results
- `exclude_domains` (list): List of domains to exclude from search results
- `search_type` (str): Type of search ("web", "news", "images", default: "web")
- `language` (str): Language code in ISO 639-1 format
- `region` (str): Region code in ISO 3166-1 format
- `safe_search` (str): Safe search level ("moderate", "strict", "off")

**Returns:** `SearchResponse` object containing the search results

##### `search_with_request(request)`

Perform a web search using a `SearchRequest` model.

**Parameters:**
- `request` (SearchRequest): SearchRequest model with all search parameters

**Returns:** `SearchResponse` object containing the search results

### Data Models

#### SearchRequest

Model for web search request parameters.

```python
from src.agent import SearchRequest

request = SearchRequest(
    query="machine learning applications",
    num_results=10,
    include_domains=["nature.com", "science.org"],
    search_type="web",
    language="en",
    safe_search="moderate"
)
```

#### SearchResponse

Model for the complete API response.

```python
# Accessing response data
response = agent.search("artificial intelligence")

print(f"Query: {response.query}")
print(f"Total results: {response.total_results}")
print(f"Search time: {response.search_time:.2f} seconds")

# Access individual results
for result in response.results:
    print(f"Title: {result.title}")
    print(f"URL: {result.url}")
    print(f"Snippet: {result.snippet}")
    print(f"Domain: {result.domain}")
```

#### SearchResult

Model for an individual search result.

```python
# Accessing result data
result = response.results[0]

print(f"Title: {result.title}")
print(f"URL: {result.url}")
print(f"Snippet: {result.snippet}")
print(f"Position: {result.position}")
print(f"Domain: {result.domain}")
print(f"Published date: {result.published_date}")
print(f"Thumbnail URL: {result.thumbnail_url}")
```

## Error Handling

The library provides specific exception types for different error scenarios:

```python
from src.agent import (
    WebSearchAgent,
    ZAIAuthenticationError,
    ZAIRateLimitError,
    ZAIInvalidRequestError,
    ZAIServerError,
    ZAIApiError
)

agent = WebSearchAgent()

try:
    results = agent.search("your query here")
except ZAIAuthenticationError as e:
    print(f"Authentication failed: {e.message}")
    print(f"Status code: {e.status_code}")
except ZAIRateLimitError as e:
    print(f"Rate limit exceeded: {e.message}")
    print(f"Retry after: {e.response_data.get('retry_after', 'unknown')}")
except ZAIInvalidRequestError as e:
    print(f"Invalid request: {e.message}")
except ZAIServerError as e:
    print(f"Server error: {e.message}")
    print(f"Status code: {e.status_code}")
except ZAIApiError as e:
    print(f"API error: {e.message}")
```

## Examples

The `examples/` directory contains comprehensive examples demonstrating various features:

### Basic Usage

```python
# examples/basic_usage.py
python examples/basic_usage.py
```

Demonstrates:
- Basic search functionality
- Advanced search with all parameters
- Error handling examples
- Configuration from environment variables
- Custom configuration creation

### Async Usage

```python
# examples/async_usage.py
python examples/async_usage.py
```

Demonstrates:
- Async search operations
- Concurrent searches
- Performance comparison (sequential vs concurrent)
- Error handling in async operations

### Batch Search

```python
# examples/batch_search.py
python examples/batch_search.py
```

Demonstrates:
- Processing multiple searches
- Sequential vs concurrent batch processing
- Exporting results to different formats (JSON, CSV, text)
- Error handling in batch operations

### Custom Agent

```python
# examples/custom_agent.py
python examples/custom_agent.py
```

Demonstrates:
- Extending the base agent
- Adding custom functionality
- Sentiment analysis
- Credibility scoring
- Query comparison

## Advanced Usage

### Async Operations

For concurrent operations, use the provided async wrapper:

```python
import asyncio
from examples.async_usage import AsyncWebSearchAgent
from src.agent import WebSearchAgent

async def main():
    # Create agent and async wrapper
    agent = WebSearchAgent()
    async_agent = AsyncWebSearchAgent(agent)
    
    # Perform concurrent searches
    queries = ["AI research", "machine learning", "deep learning"]
    tasks = [async_agent.search(query) for query in queries]
    results = await asyncio.gather(*tasks)
    
    # Process results
    for query, result in zip(queries, results):
        print(f"Query: {query}, Results: {len(result.results)}")
    
    # Clean up
    async_agent.close()

# Run the async function
asyncio.run(main())
```

### Batch Processing

For processing multiple searches efficiently:

```python
from examples.batch_search import BatchSearchProcessor, BatchSearchItem
from src.agent import WebSearchAgent

# Create agent and processor
agent = WebSearchAgent()
processor = BatchSearchProcessor(agent, max_workers=5)

# Define search items
items = [
    BatchSearchItem(id="1", query="artificial intelligence"),
    BatchSearchItem(id="2", query="machine learning"),
    BatchSearchItem(id="3", query="deep learning")
]

# Process batch
results = processor.process_batch(items)

# Process results
for result in results:
    if result.success:
        print(f"ID {result.item.id}: {len(result.results.results)} results")
    else:
        print(f"ID {result.item.id}: Failed - {result.error_message}")
```

### Custom Agent Extension

Extend the base agent with custom functionality:

```python
from src.agent import WebSearchAgent, SearchResponse, SearchResult

class CustomWebSearchAgent(WebSearchAgent):
    def search_with_analysis(self, query, **kwargs):
        # Perform the search
        response = self.search(query, **kwargs)
        
        # Add custom analysis
        for result in response.results:
            result.word_count = len(result.snippet.split())
            result.reading_time = result.word_count / 200  # 200 WPM
        
        return response

# Use the custom agent
agent = CustomWebSearchAgent()
results = agent.search_with_analysis("artificial intelligence")
```

## Testing

Run the test suite:

```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=src

# Run specific test file
python -m pytest tests/test_web_search_agent.py
```

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for your changes
5. Run the test suite (`python -m pytest`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Add docstrings to all public functions and classes
- Include type hints where appropriate
- Write tests for new functionality
- Update documentation as needed

## Documentation

Additional documentation is available in the `docs/` directory:

- [API Reference](docs/api_reference.md) - Detailed API documentation
- [Configuration](docs/configuration.md) - Configuration options
- [Error Handling](docs/error_handling.md) - Error handling guide
- [Examples](docs/examples.md) - More detailed examples

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a list of changes and version history.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- Create an issue on GitHub for bug reports or feature requests
- Check the documentation for common questions
- Review the examples for usage patterns

## Project Structure

```
zai-web-search-agent/
├── src/
│   ├── __init__.py
│   └── agent/
│       ├── __init__.py
│       ├── web_search_agent.py    # Main WebSearchAgent class
│       ├── auth.py                # Authentication handling
│       ├── config.py              # Configuration management
│       ├── models.py              # Pydantic models
│       ├── exceptions.py          # Custom exceptions
│       └── rate_limiter.py       # Rate limiting implementation
├── examples/
│   ├── basic_usage.py             # Basic usage examples
│   ├── async_usage.py             # Async usage examples
│   ├── batch_search.py            # Batch processing examples
│   └── custom_agent.py            # Custom agent extension examples
├── tests/
│   ├── __init__.py
│   ├── test_web_search_agent.py
│   ├── test_auth.py
│   ├── test_config.py
│   ├── test_models.py
│   └── test_rate_limiter.py
├── docs/
│   ├── api_reference.md
│   ├── configuration.md
│   ├── error_handling.md
│   └── examples.md
├── requirements.txt
├── README.md
├── CHANGELOG.md
├── .env.example
└── pytest.ini
```

## Dependencies

- `requests` - HTTP client library
- `pydantic` - Data validation and settings management
- `python-dotenv` - Environment variable management
- `pytest` - Testing framework (development)
- `pytest-cov` - Coverage reporting (development)