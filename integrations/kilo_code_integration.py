"""
Интеграция Z.AI Web Search Agent с Kilo Code
============================================

Этот модуль предоставляет готовые функции для интеграции
поискового агента в проект Kilo Code.

Использование:
-------------
from integrations.kilo_code_integration import KiloSearchIntegration

# Создать экземпляр
search = KiloSearchIntegration()

# Выполнить поиск
results = search.search("ваш запрос")
"""

import os
import sys
import json
from typing import List, Dict, Any, Optional, Union
from dataclasses import dataclass, asdict

# Добавляем путь к модулям агента
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agent import (
    WebSearchAgent,
    ZAIConfig,
    SearchResult,
    SearchResponse,
    ZAIAuthenticationError,
    ZAIRateLimitError,
    ZAIInvalidRequestError,
    ZAIApiError
)


@dataclass
class KiloSearchResult:
    """
    Результат поиска в формате, удобном для Kilo Code
    """
    title: str
    url: str
    snippet: str
    position: int
    domain: str
    published_date: Optional[str] = None
    thumbnail_url: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Преобразовать в словарь"""
        return asdict(self)
    
    def to_json(self) -> str:
        """Преобразовать в JSON"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)


@dataclass
class KiloSearchResponse:
    """
    Ответ поиска в формате для Kilo Code
    """
    query: str
    results: List[KiloSearchResult]
    total_results: int
    search_time: float
    status: str = "success"
    error_message: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Преобразовать в словарь"""
        return {
            "query": self.query,
            "results": [r.to_dict() for r in self.results],
            "total_results": self.total_results,
            "search_time": self.search_time,
            "status": self.status,
            "error_message": self.error_message
        }
    
    def to_json(self) -> str:
        """Преобразовать в JSON"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)


class KiloSearchIntegration:
    """
    Класс для интеграции Z.AI поиска в Kilo Code
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        config: Optional[ZAIConfig] = None,
        max_retries: int = 3,
        timeout: float = 30.0
    ):
        """
        Инициализация интеграции
        
        Args:
            api_key: API ключ Z.AI (если не указан, берётся из .env)
            config: Конфигурация Z.AI (опционально)
            max_retries: Максимальное количество повторных попыток
            timeout: Тайм-аут запросов в секундах
        """
        try:
            if config is None:
                if api_key:
                    config = ZAIConfig(api_key=api_key)
                else:
                    config = ZAIConfig.from_env()
            
            self.agent = WebSearchAgent(
                config=config,
                max_retries=max_retries,
                timeout=timeout
            )
            self._initialized = True
            
        except Exception as e:
            self._initialized = False
            self._init_error = str(e)
    
    def is_ready(self) -> bool:
        """Проверить готовность агента"""
        return self._initialized
    
    def get_error(self) -> Optional[str]:
        """Получить ошибку инициализации"""
        return getattr(self, '_init_error', None)
    
    def search(
        self,
        query: str,
        num_results: int = 10,
        language: str = "ru",
        region: str = "RU",
        safe_search: str = "moderate"
    ) -> KiloSearchResponse:
        """
        Выполнить простой поиск
        
        Args:
            query: Поисковый запрос
            num_results: Количество результатов
            language: Код языка (ru, en, etc.)
            region: Код региона (RU, US, etc.)
            safe_search: Уровень безопасного поиска
            
        Returns:
            KiloSearchResponse с результатами
        """
        if not self._initialized:
            return KiloSearchResponse(
                query=query,
                results=[],
                total_results=0,
                search_time=0.0,
                status="error",
                error_message=self._init_error
            )
        
        try:
            # Выполнить поиск через агента
            response = self.agent.search(
                query=query,
                num_results=num_results,
                language=language,
                region=region,
                safe_search=safe_search
            )
            
            # Преобразовать результаты
            kilo_results = [
                KiloSearchResult(
                    title=r.title,
                    url=r.url,
                    snippet=r.snippet,
                    position=r.position,
                    domain=r.domain,
                    published_date=r.published_date,
                    thumbnail_url=r.thumbnail_url
                )
                for r in response.results
            ]
            
            return KiloSearchResponse(
                query=response.query,
                results=kilo_results,
                total_results=response.total_results,
                search_time=response.search_time,
                status="success"
            )
            
        except ZAIAuthenticationError as e:
            return KiloSearchResponse(
                query=query,
                results=[],
                total_results=0,
                search_time=0.0,
                status="error",
                error_message=f"Ошибка аутентификации: {e.message}"
            )
        except ZAIRateLimitError as e:
            return KiloSearchResponse(
                query=query,
                results=[],
                total_results=0,
                search_time=0.0,
                status="error",
                error_message=f"Превышен лимит запросов: {e.message}"
            )
        except Exception as e:
            return KiloSearchResponse(
                query=query,
                results=[],
                total_results=0,
                search_time=0.0,
                status="error",
                error_message=str(e)
            )
    
    def search_multiple(
        self,
        queries: List[str],
        num_results: int = 10
    ) -> List[KiloSearchResponse]:
        """
        Выполнить несколько поисковых запросов
        
        Args:
            queries: Список запросов
            num_results: Количество результатов на запрос
            
        Returns:
            Список KiloSearchResponse
        """
        results = []
        for query in queries:
            response = self.search(query, num_results=num_results)
            results.append(response)
        return results
    
    def search_with_filters(
        self,
        query: str,
        num_results: int = 10,
        include_domains: Optional[List[str]] = None,
        exclude_domains: Optional[List[str]] = None,
        language: str = "ru"
    ) -> KiloSearchResponse:
        """
        Поиск с фильтрами доменов
        
        Args:
            query: Поисковый запрос
            num_results: Количество результатов
            include_domains: Список доменов для включения
            exclude_domains: Список доменов для исключения
            language: Код языка
            
        Returns:
            KiloSearchResponse с результатами
        """
        if not self._initialized:
            return KiloSearchResponse(
                query=query,
                results=[],
                total_results=0,
                search_time=0.0,
                status="error",
                error_message=self._init_error
            )
        
        try:
            response = self.agent.search(
                query=query,
                num_results=num_results,
                include_domains=include_domains,
                exclude_domains=exclude_domains,
                language=language
            )
            
            kilo_results = [
                KiloSearchResult(
                    title=r.title,
                    url=r.url,
                    snippet=r.snippet,
                    position=r.position,
                    domain=r.domain,
                    published_date=r.published_date,
                    thumbnail_url=r.thumbnail_url
                )
                for r in response.results
            ]
            
            return KiloSearchResponse(
                query=response.query,
                results=kilo_results,
                total_results=response.total_results,
                search_time=response.search_time,
                status="success"
            )
            
        except Exception as e:
            return KiloSearchResponse(
                query=query,
                results=[],
                total_results=0,
                search_time=0.0,
                status="error",
                error_message=str(e)
            )


# ===== ФУНКЦИИ-ХЕЛПЕРЫ ДЛЯ БЫСТРОЙ ИНТЕГРАЦИИ =====

_default_integration: Optional[KiloSearchIntegration] = None


def init_search(api_key: Optional[str] = None) -> KiloSearchIntegration:
    """
    Инициализировать глобальный экземпляр поиска
    
    Args:
        api_key: API ключ (опционально)
        
    Returns:
        Экземпляр KiloSearchIntegration
    """
    global _default_integration
    _default_integration = KiloSearchIntegration(api_key=api_key)
    return _default_integration


def quick_search(query: str, num_results: int = 5) -> Dict[str, Any]:
    """
    Быстрый поиск (использует глобальный экземпляр)
    
    Args:
        query: Поисковый запрос
        num_results: Количество результатов
        
    Returns:
        Словарь с результатами
    """
    global _default_integration
    
    if _default_integration is None:
        _default_integration = KiloSearchIntegration()
    
    response = _default_integration.search(query, num_results=num_results)
    return response.to_dict()


def search_json(query: str, num_results: int = 5) -> str:
    """
    Поиск с возвратом JSON
    
    Args:
        query: Поисковый запрос
        num_results: Количество результатов
        
    Returns:
        JSON строка с результатами
    """
    result = quick_search(query, num_results)
    return json.dumps(result, ensure_ascii=False, indent=2)


# ===== ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ =====

def example_basic_usage():
    """Базовый пример использования"""
    print("=== Базовое использование ===\n")
    
    # Создать экземпляр
    search = KiloSearchIntegration()
    
    if not search.is_ready():
        print(f"Ошибка инициализации: {search.get_error()}")
        return
    
    # Выполнить поиск
    response = search.search("Python программирование", num_results=3)
    
    # Вывести результаты
    print(f"Запрос: {response.query}")
    print(f"Найдено: {response.total_results}")
    print(f"Время: {response.search_time:.2f}s")
    print(f"Статус: {response.status}\n")
    
    for result in response.results:
        print(f"{result.position}. {result.title}")
        print(f"   {result.url}")
        print(f"   {result.snippet[:100]}...")
        print()


def example_json_output():
    """Пример с JSON выводом"""
    print("\n=== JSON формат ===\n")
    
    search = KiloSearchIntegration()
    response = search.search("искусственный интеллект", num_results=2)
    
    # Вывести как JSON
    print(response.to_json())


def example_quick_functions():
    """Пример быстрых функций"""
    print("\n=== Быстрые функции ===\n")
    
    # Инициализировать один раз
    init_search()
    
    # Использовать в любом месте кода
    result1 = quick_search("машинное обучение", num_results=2)
    print(f"Результат 1: {result1['total_results']} найдено")
    
    result2 = quick_search("глубокое обучение", num_results=2)
    print(f"Результат 2: {result2['total_results']} найдено")
    
    # JSON формат
    json_result = search_json("нейронные сети", num_results=2)
    print(f"\nJSON результат:\n{json_result[:200]}...")


def example_filtered_search():
    """Пример поиска с фильтрами"""
    print("\n=== Поиск с фильтрами ===\n")
    
    search = KiloSearchIntegration()
    
    # Поиск только на определённых сайтах
    response = search.search_with_filters(
        query="Python tutorial",
        num_results=3,
        include_domains=["python.org", "docs.python.org"],
        language="en"
    )
    
    print(f"Запрос: {response.query}")
    print(f"Результаты только с python.org:")
    for result in response.results:
        print(f"  - {result.title} ({result.domain})")


def main():
    """Запустить все примеры"""
    print("=" * 60)
    print("Z.AI Web Search Agent - Интеграция с Kilo Code")
    print("=" * 60)
    
    try:
        example_basic_usage()
        example_json_output()
        example_quick_functions()
        example_filtered_search()
    except Exception as e:
        print(f"\nОшибка: {e}")
        print("\nПроверьте настройки API ключа в .env файле")
    
    print("\n" + "=" * 60)
    print("Примеры завершены!")


if __name__ == "__main__":
    main()
