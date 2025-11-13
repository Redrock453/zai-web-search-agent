"""
YAML Configuration Loader для Z.AI Web Search Agent
===================================================

Этот модуль загружает конфигурацию из YAML файла и создаёт
настроенный экземпляр агента.

Использование:
    from integrations.yaml_loader import load_agent_from_yaml
    
    agent = load_agent_from_yaml('config/agent.yaml')
    results = agent.search("Python")
"""

import os
import sys
import yaml
import re
from typing import Dict, Any, Optional
from pathlib import Path

# Добавляем путь к модулям
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agent import WebSearchAgent, ZAIConfig


class YAMLConfigLoader:
    """Загрузчик конфигурации из YAML файла"""
    
    def __init__(self, config_path: str):
        """
        Инициализация загрузчика
        
        Args:
            config_path: Путь к YAML файлу конфигурации
        """
        self.config_path = Path(config_path)
        self.config_data: Dict[str, Any] = {}
        self.active_profile: Optional[str] = None
    
    def load(self, profile: Optional[str] = None) -> Dict[str, Any]:
        """
        Загрузить конфигурацию из файла
        
        Args:
            profile: Имя профиля для использования (development, staging, production)
            
        Returns:
            Словарь с конфигурацией
        """
        # Проверить существование файла
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
        
        # Загрузить YAML
        with open(self.config_path, 'r', encoding='utf-8') as f:
            self.config_data = yaml.safe_load(f)
        
        # Подставить переменные окружения
        self.config_data = self._substitute_env_vars(self.config_data)
        
        # Применить профиль, если указан
        if profile:
            self._apply_profile(profile)
        elif 'AGENT_PROFILE' in os.environ:
            self._apply_profile(os.environ['AGENT_PROFILE'])
        
        return self.config_data
    
    def _substitute_env_vars(self, data: Any) -> Any:
        """
        Рекурсивно подставить переменные окружения в конфигурацию
        
        Args:
            data: Данные конфигурации
            
        Returns:
            Данные с подставленными переменными
        """
        if isinstance(data, dict):
            return {k: self._substitute_env_vars(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._substitute_env_vars(item) for item in data]
        elif isinstance(data, str):
            # Заменить ${VAR_NAME} на значение из окружения
            pattern = r'\$\{([^}]+)\}'
            
            def replace_var(match):
                var_name = match.group(1)
                return os.environ.get(var_name, match.group(0))
            
            return re.sub(pattern, replace_var, data)
        else:
            return data
    
    def _apply_profile(self, profile: str):
        """
        Применить профиль конфигурации
        
        Args:
            profile: Имя профиля
        """
        if 'profiles' not in self.config_data:
            return
        
        if profile not in self.config_data['profiles']:
            available = ', '.join(self.config_data['profiles'].keys())
            raise ValueError(f"Profile '{profile}' not found. Available: {available}")
        
        self.active_profile = profile
        profile_config = self.config_data['profiles'][profile]
        
        # Рекурсивно объединить профиль с основной конфигурацией
        self._deep_merge(self.config_data, profile_config)
    
    def _deep_merge(self, base: dict, override: dict):
        """
        Глубокое слияние словарей
        
        Args:
            base: Базовый словарь (изменяется)
            override: Словарь для слияния
        """
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._deep_merge(base[key], value)
            else:
                base[key] = value
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Получить значение из конфигурации по пути
        
        Args:
            key_path: Путь к значению, разделённый точками (например, "api.timeout")
            default: Значение по умолчанию
            
        Returns:
            Значение конфигурации или default
        """
        keys = key_path.split('.')
        value = self.config_data
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def create_zai_config(self) -> ZAIConfig:
        """
        Создать ZAIConfig из загруженной конфигурации
        
        Returns:
            Экземпляр ZAIConfig
        """
        api_config = self.config_data.get('api', {})
        
        # Получить API ключ из конфигурации или окружения
        api_key = api_config.get('api_key')
        if not api_key or api_key.startswith('${'):
            api_key = os.environ.get('ZAI_API_KEY')
        
        return ZAIConfig(
            api_key=api_key or "",
            base_url=api_config.get('base_url', 'https://api.z.ai/v1'),
            timeout=api_config.get('timeout', 30),
            max_retries=api_config.get('max_retries', 3)
        )
    
    def create_agent(self) -> WebSearchAgent:
        """
        Создать WebSearchAgent из загруженной конфигурации
        
        Returns:
            Настроенный экземпляр WebSearchAgent
        """
        # Создать ZAIConfig
        config = self.create_zai_config()
        
        # Получить настройки retry
        retry_config = self.config_data.get('retry', {})
        
        # Получить настройки rate limiting
        rate_limit = self.config_data.get('rate_limit', {})
        
        # Создать агента
        agent = WebSearchAgent(
            config=config,
            max_retries=config.max_retries,
            initial_backoff=retry_config.get('initial_backoff', 1.0),
            max_backoff=retry_config.get('max_backoff', 60.0),
            rate_limit_requests=rate_limit.get('requests', 100),
            rate_limit_window=rate_limit.get('window', 60)
        )
        
        return agent


def load_agent_from_yaml(
    config_path: str = "config/agent.yaml",
    profile: Optional[str] = None
) -> WebSearchAgent:
    """
    Загрузить и создать агента из YAML конфигурации
    
    Args:
        config_path: Путь к YAML файлу конфигурации
        profile: Профиль для использования (опционально)
        
    Returns:
        Настроенный экземпляр WebSearchAgent
    
    Example:
        >>> agent = load_agent_from_yaml('config/agent.yaml', profile='production')
        >>> results = agent.search("Python programming")
    """
    loader = YAMLConfigLoader(config_path)
    loader.load(profile=profile)
    return loader.create_agent()


def load_config_from_yaml(
    config_path: str = "config/agent.yaml",
    profile: Optional[str] = None
) -> Dict[str, Any]:
    """
    Загрузить конфигурацию из YAML файла
    
    Args:
        config_path: Путь к YAML файлу
        profile: Профиль для использования
        
    Returns:
        Словарь с конфигурацией
    """
    loader = YAMLConfigLoader(config_path)
    return loader.load(profile=profile)


# ===== ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ =====

def example_basic_yaml():
    """Базовый пример использования YAML конфигурации"""
    print("=== Загрузка агента из YAML ===\n")
    
    try:
        # Загрузить агента с профилем по умолчанию
        agent = load_agent_from_yaml('c:/zai-web-search-agent/config/agent.yaml')
        
        # Использовать агента
        response = agent.search("Python программирование", num_results=3)
        
        print(f"Запрос: {response.query}")
        print(f"Найдено: {response.total_results}")
        print(f"Время: {response.search_time:.2f}s\n")
        
        for result in response.results[:2]:
            print(f"{result.position}. {result.title}")
            print(f"   {result.url}")
            print()
            
    except FileNotFoundError as e:
        print(f"Ошибка: {e}")
    except Exception as e:
        print(f"Ошибка: {e}")


def example_profile_yaml():
    """Пример использования с профилем"""
    print("\n=== Использование профилей ===\n")
    
    try:
        # Загрузить с development профилем
        agent_dev = load_agent_from_yaml(
            'c:/zai-web-search-agent/config/agent.yaml',
            profile='development'
        )
        print("✓ Development профиль загружен")
        
        # Загрузить с production профилем
        agent_prod = load_agent_from_yaml(
            'c:/zai-web-search-agent/config/agent.yaml',
            profile='production'
        )
        print("✓ Production профиль загружен")
        
    except Exception as e:
        print(f"Ошибка: {e}")


def example_config_reading():
    """Пример чтения конфигурации"""
    print("\n=== Чтение конфигурации ===\n")
    
    try:
        loader = YAMLConfigLoader('c:/zai-web-search-agent/config/agent.yaml')
        config = loader.load()
        
        # Прочитать настройки
        print(f"API timeout: {loader.get('api.timeout')} секунд")
        print(f"Max retries: {loader.get('api.max_retries')}")
        print(f"Rate limit: {loader.get('rate_limit.requests')} req/{loader.get('rate_limit.window')}s")
        print(f"Default language: {loader.get('search_defaults.language')}")
        print(f"Default region: {loader.get('search_defaults.region')}")
        
        # Показать профили
        profiles = config.get('profiles', {})
        if profiles:
            print(f"\nДоступные профили: {', '.join(profiles.keys())}")
        
    except Exception as e:
        print(f"Ошибка: {e}")


def example_env_override():
    """Пример переопределения через переменные окружения"""
    print("\n=== Переопределение через ENV ===\n")
    
    # Установить переменные окружения
    os.environ['AGENT_PROFILE'] = 'development'
    os.environ['ZAI_API_KEY'] = 'test_api_key_from_env'
    
    try:
        loader = YAMLConfigLoader('c:/zai-web-search-agent/config/agent.yaml')
        config = loader.load()
        
        print(f"Активный профиль: {loader.active_profile}")
        print(f"API ключ из окружения: {os.environ.get('ZAI_API_KEY')[:20]}...")
        
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        # Очистить переменные
        os.environ.pop('AGENT_PROFILE', None)
        os.environ.pop('ZAI_API_KEY', None)


def main():
    """Запустить все примеры"""
    print("=" * 60)
    print("Z.AI Web Search Agent - YAML Configuration Loader")
    print("=" * 60)
    
    example_basic_yaml()
    example_profile_yaml()
    example_config_reading()
    example_env_override()
    
    print("\n" + "=" * 60)
    print("Примеры завершены!")
    print("\nДля использования в вашем коде:")
    print("  from integrations.yaml_loader import load_agent_from_yaml")
    print("  agent = load_agent_from_yaml('config/agent.yaml')")


if __name__ == "__main__":
    main()
