# Configuration Guide

This document provides detailed information about configuring the Z.AI Web Search Agent.

## Table of Contents

- [YAML Configuration](#yaml-configuration)
- [Environment Variables](#environment-variables)
- [Programmatic Configuration](#programmatic-configuration)
- [Configuration Options](#configuration-options)
- [API Key Management](#api-key-management)
- [Rate Limiting Configuration](#rate-limiting-configuration)
- [Retry Configuration](#retry-configuration)
- [Advanced Configuration](#advanced-configuration)

## YAML Configuration

The Z.AI Web Search Agent поддерживает конфигурацию через YAML файлы для удобной интеграции с Kilo Code и другими системами.

### Быстрый старт с YAML

Создайте файл `config/agent.yaml`:

```yaml
# Основные настройки API
api:
  api_key: ${ZAI_API_KEY}  # Из переменной окружения
  base_url: "https://api.z.ai/v1"
  timeout: 30
  max_retries: 3

# Настройки поиска по умолчанию
search_defaults:
  num_results: 10
  language: "ru"
  region: "RU"
  safe_search: "moderate"

# Интеграция с Kilo Code
kilo_code:
  enabled: true
  api_port: 5000
  enable_cors: true
```

### Загрузка агента из YAML

```python
from integrations.yaml_loader import load_agent_from_yaml

# Загрузить агента с конфигурацией из YAML
agent = load_agent_from_yaml('config/agent.yaml')

# Использовать агента
response = agent.search("Python programming")
```

### Использование профилей

YAML конфигурация поддерживает профили для разных окружений:

```yaml
profiles:
  development:
    api:
      timeout: 15
      max_retries: 1
    logging:
      level: "DEBUG"
  
  production:
    api:
      timeout: 45
      max_retries: 5
    logging:
      level: "WARNING"
```

Загрузка с профилем:

```python
# Development окружение
agent = load_agent_from_yaml('config/agent.yaml', profile='development')

# Production окружение
agent = load_agent_from_yaml('config/agent.yaml', profile='production')

# Или через переменную окружения
import os
os.environ['AGENT_PROFILE'] = 'production'
agent = load_agent_from_yaml('config/agent.yaml')
```

### Полная структура YAML конфигурации

См. пример файла `config/agent.yaml` в проекте для полной структуры со всеми доступными опциями:

- API настройки (ключ, URL, тайм-ауты)
- Retry логика (повторные попытки)
- Rate limiting (ограничение скорости)
- Настройки поиска по умолчанию
- Интеграция с Kilo Code
- Логирование
- Кэширование
- Фильтры
- Профили окружений
- И многое другое

## Environment Variables

The Z.AI Web Search Agent can be configured using environment variables. Create a `.env` file in the project root:

```env
# Required
ZAI_API_KEY=your_api_key_here

# Optional
ZAI_BASE_URL=https://api.z.ai/v1
ZAI_TIMEOUT=30
ZAI_MAX_RETRIES=3
```

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `ZAI_API_KEY` | Your Z.AI API key | `zai_1234567890abcdef1234567890abcdef` |

### Optional Variables

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `ZAI_BASE_URL` | Base URL for Z.AI API | `https://api.z.ai/v1` | `https://api.z.ai/v1` |
| `ZAI_TIMEOUT` | Request timeout in seconds | `30` | `45` |
| `ZAI_MAX_RETRIES` | Maximum number of retries for failed requests | `3` | `5` |

## Programmatic Configuration

You can also configure the agent programmatically:

### Using ZAIConfig

```python
from src.agent import ZAIConfig, WebSearchAgent

# Create configuration
config = ZAIConfig(
    api_key="your_api_key_here",
    base_url="https://api.z.ai/v1",
    timeout=30,
    max_retries=3
)

# Initialize agent with configuration
agent = WebSearchAgent(config=config)
```

### Loading from Environment

```python
from src.agent import ZAIConfig, WebSearchAgent

# Load configuration from environment variables
config = ZAIConfig.from_env()

# Or load from custom .env file
config = ZAIConfig.from_env("custom.env")

# Initialize agent
agent = WebSearchAgent(config=config)
```

### Using API Key Directly

```python
from src.agent import WebSearchAgent

# Initialize agent with API key directly
agent = WebSearchAgent(api_key="your_api_key_here")
```

## Configuration Options

### ZAIConfig

The `ZAIConfig` class provides the following configuration options:

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `api_key` | str | Yes | - | Z.AI API key |
| `base_url` | str | No | `https://api.z.ai/v1` | Base URL for Z.AI API |
| `timeout` | int | No | `30` | Request timeout in seconds |
| `max_retries` | int | No | `3` | Maximum number of retries for failed requests |

### WebSearchAgent

The `WebSearchAgent` class provides additional configuration options:

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `config` | ZAIConfig | No | `None` | ZAIConfig instance with API settings |
| `authenticator` | ZAIAuthenticator | No | `None` | ZAIAuthenticator instance for authentication |
| `api_key` | str | No | `None` | Z.AI API key (overrides config.api_key if provided) |
| `max_retries` | int | No | `3` | Maximum number of retry attempts for failed requests |
| `initial_backoff` | float | No | `1.0` | Initial backoff time in seconds for exponential backoff |
| `max_backoff` | float | No | `60.0` | Maximum backoff time in seconds for exponential backoff |
| `rate_limit_requests` | int | No | `100` | Maximum number of requests allowed in the time window |
| `rate_limit_window` | int | No | `60` | Time window in seconds for rate limiting |

## API Key Management

### API Key Format

Z.AI API keys follow this format: `zai_[a-zA-Z0-9]{32}`

Example: `zai_1234567890abcdef1234567890abcdef`

### Obtaining an API Key

1. Sign up for a Z.AI account at [https://z.ai](https://z.ai)
2. Navigate to your account settings
3. Generate a new API key
4. Copy the key and store it securely

### Securing Your API Key

- Never commit your API key to version control
- Use environment variables instead of hardcoding
- Restrict API key permissions to minimum required
- Regularly rotate your API keys
- Monitor API usage for unusual activity

### API Key Validation

The library validates API keys before use:

```python
from src.agent import ZAIAuthenticator, ZAIInvalidRequestError

try:
    # This will validate the API key format
    authenticator = ZAIAuthenticator.from_api_key("invalid_key")
except ZAIInvalidRequestError as e:
    print(f"Invalid API key: {e.message}")
```

## Rate Limiting Configuration

### Understanding Rate Limits

Z.AI API imposes rate limits to ensure fair usage. The library includes a built-in rate limiter using the token bucket algorithm.

### Configuring Rate Limiting

```python
from src.agent import WebSearchAgent

# Configure rate limiting
agent = WebSearchAgent(
    rate_limit_requests=50,  # 50 requests per window
    rate_limit_window=60     # 60 second window
)
```

### Rate Limiting Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `rate_limit_requests` | int | `100` | Maximum number of requests allowed in the time window |
| `rate_limit_window` | int | `60` | Time window in seconds for rate limiting |

### Rate Limiting Behavior

- The agent automatically handles rate limiting
- When rate limit is reached, the agent waits before making additional requests
- Exponential backoff is used for API rate limit errors
- The rate limiter is thread-safe for concurrent operations

## Retry Configuration

### Understanding Retry Logic

The library implements automatic retry logic with exponential backoff for failed requests.

### Configuring Retries

```python
from src.agent import WebSearchAgent

# Configure retry behavior
agent = WebSearchAgent(
    max_retries=5,          # Maximum retry attempts
    initial_backoff=2.0,     # Initial backoff time
    max_backoff=30.0         # Maximum backoff time
)
```

### Retry Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `max_retries` | int | `3` | Maximum number of retry attempts for failed requests |
| `initial_backoff` | float | `1.0` | Initial backoff time in seconds for exponential backoff |
| `max_backoff` | float | `60.0` | Maximum backoff time in seconds for exponential backoff |

### Retry Behavior

- Only retryable errors are retried (network errors, server errors, rate limits)
- Authentication errors and invalid requests are not retried
- Exponential backoff is used between retry attempts
- Maximum backoff time prevents excessive delays

## Advanced Configuration

### Custom Authentication

```python
from src.agent import WebSearchAgent, ZAIConfig, ZAIAuthenticator

# Create custom configuration
config = ZAIConfig(
    api_key="your_api_key_here",
    base_url="https://api.z.ai/v1",
    timeout=45
)

# Create custom authenticator
authenticator = ZAIAuthenticator.from_config(config)

# Initialize agent with custom components
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

### Environment-Specific Configuration

```python
import os
from src.agent import ZAIConfig, WebSearchAgent

def create_agent():
    # Get environment
    env = os.getenv("ENVIRONMENT", "development")
    
    if env == "production":
        config = ZAIConfig.from_env("production.env")
        return WebSearchAgent(
            config=config,
            max_retries=5,
            rate_limit_requests=100
        )
    elif env == "staging":
        config = ZAIConfig.from_env("staging.env")
        return WebSearchAgent(
            config=config,
            max_retries=3,
            rate_limit_requests=50
        )
    else:  # development
        config = ZAIConfig.from_env("development.env")
        return WebSearchAgent(
            config=config,
            max_retries=1,
            rate_limit_requests=10
        )

# Use environment-specific agent
agent = create_agent()
```

### Configuration Validation

The library validates configuration parameters:

```python
from src.agent import ZAIConfig, ZAIAuthenticator
from pydantic import ValidationError

try:
    # This will validate all parameters
    config = ZAIConfig(
        api_key="your_api_key_here",
        timeout=-1  # Invalid: timeout must be positive
    )
except ValidationError as e:
    print(f"Configuration error: {e}")

try:
    # This will validate API key format
    authenticator = ZAIAuthenticator.from_api_key("invalid_key")
except ZAIInvalidRequestError as e:
    print(f"Authentication error: {e.message}")
```

### Configuration Best Practices

1. **Use Environment Variables**: Store sensitive data like API keys in environment variables
2. **Separate Configurations**: Use different configurations for different environments
3. **Validate Configuration**: Validate configuration before use
4. **Document Configuration**: Document configuration options for your team
5. **Version Control**: Exclude sensitive configuration from version control
6. **Monitor Usage**: Monitor API usage and adjust rate limits accordingly

### Example Configuration Files

#### Development Environment (.env.development)

```env
# Development configuration
ZAI_API_KEY=zai_development_api_key_here
ZAI_BASE_URL=https://api-dev.z.ai/v1
ZAI_TIMEOUT=15
ZAI_MAX_RETRIES=1
```

#### Staging Environment (.env.staging)

```env
# Staging configuration
ZAI_API_KEY=zai_staging_api_key_here
ZAI_BASE_URL=https://api-staging.z.ai/v1
ZAI_TIMEOUT=30
ZAI_MAX_RETRIES=3
```

#### Production Environment (.env.production)

```env
# Production configuration
ZAI_API_KEY=zai_production_api_key_here
ZAI_BASE_URL=https://api.z.ai/v1
ZAI_TIMEOUT=45
ZAI_MAX_RETRIES=5
```

### Loading Environment-Specific Configuration

```python
import os
from src.agent import ZAIConfig, WebSearchAgent

def load_environment_config():
    env = os.getenv("ENVIRONMENT", "development")
    env_file = f".env.{env}"
    
    try:
        config = ZAIConfig.from_env(env_file)
        print(f"Loaded {env} configuration")
        return config
    except Exception as e:
        print(f"Failed to load {env} configuration: {e}")
        raise

# Usage
config = load_environment_config()
agent = WebSearchAgent(config=config)