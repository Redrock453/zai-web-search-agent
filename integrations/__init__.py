"""
Модули интеграции Z.AI Web Search Agent
"""

from .kilo_code_integration import (
    KiloSearchIntegration,
    KiloSearchResult,
    KiloSearchResponse,
    init_search,
    quick_search,
    search_json
)

from .yaml_loader import (
    YAMLConfigLoader,
    load_agent_from_yaml,
    load_config_from_yaml
)

__all__ = [
    # Kilo Code интеграция
    'KiloSearchIntegration',
    'KiloSearchResult',
    'KiloSearchResponse',
    'init_search',
    'quick_search',
    'search_json',
    
    # YAML загрузчик
    'YAMLConfigLoader',
    'load_agent_from_yaml',
    'load_config_from_yaml',
]
