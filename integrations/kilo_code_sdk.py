"""
Интеграция Z.AI Web Search с Kilo Code (официальный SDK)
========================================================

Использование официального Z.AI SDK для поиска.

Использование:
-------------
from integrations.kilo_code_sdk import quick_search, KiloSearchIntegration

# Быстрый поиск
results = quick_search("Python programming", num_results=5)

# Или создать экземпляр
search = KiloSearchIntegration(api_key="your_key")
response = search.search("query")
"""

import os
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
import json

try:
    from zai import ZaiClient
except ImportError:
    raise ImportError("Установите zai-sdk: pip install zai-sdk")


@dataclass
class KiloSearchResult:
    """Результат поиска в формате Kilo Code"""
    title: str
    url: str
    snippet: str
    position: int
    domain: str
    published_date: Optional[str] = None
    media: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)


@dataclass
class KiloSearchResponse:
    """Ответ поиска в формате Kilo Code"""
    query: str
    results: List[KiloSearchResult]
    total_results: int
    status: str = "success"
    error_message: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "query": self.query,
            "results": [r.to_dict() for r in self.results],
            "total_results": self.total_results,
            "status": self.status,
            "error_message": self.error_message
        }
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)


class KiloSearchIntegration:
    """
    Интеграция Z.AI поиска с Kilo Code (официальный SDK)
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Инициализация
        
        Args:
            api_key: API ключ Z.AI (если не указан, берётся из ZAI_API_KEY)
        """
        self.api_key = api_key or os.getenv('ZAI_API_KEY')
        
        if not self.api_key:
            self._initialized = False
            self._init_error = "API key не найден. Установите ZAI_API_KEY или передайте api_key"
        else:
            try:
                self.client = ZaiClient(api_key=self.api_key)
                self._initialized = True
                self._init_error = None
            except Exception as e:
                self._initialized = False
                self._init_error = str(e)
    
    def is_ready(self) -> bool:
        """Проверить готовность"""
        return self._initialized
    
    def get_error(self) -> Optional[str]:
        """Получить ошибку инициализации"""
        return self._init_error
    
    def search(
        self,
        query: str,
        num_results: int = 10,
        search_engine: str = "search-prime",
        domain_filter: Optional[str] = None,
        recency_filter: str = "noLimit"
    ) -> KiloSearchResponse:
        """
        Выполнить поиск
        
        Args:
            query: Поисковый запрос
            num_results: Количество результатов (1-50)
            search_engine: Поисковая система ("search-prime")
            domain_filter: Фильтр по домену (опционально)
            recency_filter: Фильтр по дате ("noLimit", "day", "week", "month", "year")
        
        Returns:
            KiloSearchResponse с результатами
        """
        if not self.is_ready():
            return KiloSearchResponse(
                query=query,
                results=[],
                total_results=0,
                status="error",
                error_message=self.get_error()
            )
        
        try:
            # Выполнить поиск через SDK
            response = self.client.web_search.web_search(
                search_engine=search_engine,
                search_query=query,
                count=min(num_results, 50),
                search_domain_filter=domain_filter,
                search_recency_filter=recency_filter
            )
            
            # Преобразовать результаты
            results = []
            search_results = response.search_result if hasattr(response, 'search_result') else []
            
            for idx, result in enumerate(search_results, 1):
                url = result.get('link', '')
                domain = url.split('/')[2] if '/' in url and len(url.split('/')) > 2 else ''
                
                results.append(KiloSearchResult(
                    title=result.get('title', ''),
                    url=url,
                    snippet=result.get('content', ''),
                    position=idx,
                    domain=domain,
                    published_date=result.get('publish_date'),
                    media=result.get('media')
                ))
            
            return KiloSearchResponse(
                query=query,
                results=results,
                total_results=len(results),
                status="success"
            )
            
        except Exception as e:
            return KiloSearchResponse(
                query=query,
                results=[],
                total_results=0,
                status="error",
                error_message=str(e)
            )
    
    def batch_search(self, queries: List[str], **kwargs) -> List[KiloSearchResponse]:
        """
        Выполнить множественный поиск
        
        Args:
            queries: Список запросов
            **kwargs: Параметры для search()
        
        Returns:
            Список KiloSearchResponse
        """
        return [self.search(query, **kwargs) for query in queries]


def quick_search(query: str, num_results: int = 10, **kwargs) -> List[KiloSearchResult]:
    """
    Быстрый поиск (helper функция)
    
    Args:
        query: Поисковый запрос
        num_results: Количество результатов
        **kwargs: Дополнительные параметры
    
    Returns:
        Список KiloSearchResult
    """
    search = KiloSearchIntegration()
    response = search.search(query, num_results=num_results, **kwargs)
    return response.results


def init_search(api_key: Optional[str] = None) -> KiloSearchIntegration:
    """
    Инициализировать поиск с API ключом
    
    Args:
        api_key: API ключ Z.AI
    
    Returns:
        KiloSearchIntegration
    """
    return KiloSearchIntegration(api_key=api_key)


__all__ = [
    'KiloSearchIntegration',
    'KiloSearchResult', 
    'KiloSearchResponse',
    'quick_search',
    'init_search'
]
