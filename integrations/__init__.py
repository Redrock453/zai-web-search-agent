"""
Модули интеграции Z.AI Web Search Agent
"""

from .kilo_code_sdk import (
    KiloSearchIntegration,
    KiloSearchResult,
    KiloSearchResponse,
    init_search,
    quick_search
)

from .yaml_loader import (
    YAMLConfigLoader,
    load_agent_from_yaml,
    load_config_from_yaml
)

__all__ = [
    # Kilo Code интеграция (SDK)
    'KiloSearchIntegration',
    'KiloSearchResult',
    'KiloSearchResponse',
    'init_search',
    'quick_search',
    
    # YAML загрузчик
    'YAMLConfigLoader',
    'load_agent_from_yaml',
    'load_config_from_yaml',
]

