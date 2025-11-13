"""
REST API для интеграции с Kilo Code
===================================

Простой Flask API сервер для использования Z.AI Search Agent
в Kilo Code через HTTP запросы.

Установка зависимостей:
    pip install flask flask-cors

Запуск:
    python kilo_code_api.py

API Endpoints:
    GET  /api/health          - Проверка работы
    POST /api/search          - Поиск
    POST /api/search/batch    - Пакетный поиск
"""

import os
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS
from typing import Dict, Any, List

# Добавляем путь к модулям
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from integrations.kilo_code_integration import KiloSearchIntegration


# Создать Flask приложение
app = Flask(__name__)
CORS(app)  # Разрешить CORS для кросс-доменных запросов

# Глобальный экземпляр поиска
search_integration: KiloSearchIntegration = None


@app.before_request
def initialize_search():
    """Инициализировать поиск перед первым запросом"""
    global search_integration
    if search_integration is None:
        search_integration = KiloSearchIntegration()


@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Проверка работы API
    
    Returns:
        JSON с информацией о статусе
    """
    return jsonify({
        'status': 'ok',
        'service': 'Z.AI Search API',
        'ready': search_integration.is_ready() if search_integration else False,
        'error': search_integration.get_error() if search_integration else None
    })


@app.route('/api/search', methods=['POST'])
def search():
    """
    Выполнить поиск
    
    Request JSON:
        {
            "query": "поисковый запрос",
            "num_results": 10,
            "language": "ru",
            "region": "RU",
            "safe_search": "moderate"
        }
    
    Returns:
        JSON с результатами поиска
    """
    try:
        # Получить параметры запроса
        data = request.get_json()
        
        if not data or 'query' not in data:
            return jsonify({
                'error': 'Missing required parameter: query'
            }), 400
        
        query = data['query']
        num_results = data.get('num_results', 10)
        language = data.get('language', 'ru')
        region = data.get('region', 'RU')
        safe_search = data.get('safe_search', 'moderate')
        
        # Выполнить поиск
        response = search_integration.search(
            query=query,
            num_results=num_results,
            language=language,
            region=region,
            safe_search=safe_search
        )
        
        # Вернуть результаты
        return jsonify(response.to_dict())
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500


@app.route('/api/search/batch', methods=['POST'])
def search_batch():
    """
    Выполнить пакетный поиск
    
    Request JSON:
        {
            "queries": ["запрос 1", "запрос 2", ...],
            "num_results": 10
        }
    
    Returns:
        JSON массив с результатами для каждого запроса
    """
    try:
        # Получить параметры
        data = request.get_json()
        
        if not data or 'queries' not in data:
            return jsonify({
                'error': 'Missing required parameter: queries'
            }), 400
        
        queries = data['queries']
        num_results = data.get('num_results', 10)
        
        if not isinstance(queries, list):
            return jsonify({
                'error': 'queries must be an array'
            }), 400
        
        # Выполнить поиск для каждого запроса
        results = search_integration.search_multiple(
            queries=queries,
            num_results=num_results
        )
        
        # Вернуть результаты
        return jsonify([r.to_dict() for r in results])
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500


@app.route('/api/search/filtered', methods=['POST'])
def search_filtered():
    """
    Поиск с фильтрацией доменов
    
    Request JSON:
        {
            "query": "поисковый запрос",
            "num_results": 10,
            "include_domains": ["domain1.com", "domain2.com"],
            "exclude_domains": ["spam.com"],
            "language": "ru"
        }
    
    Returns:
        JSON с отфильтрованными результатами
    """
    try:
        data = request.get_json()
        
        if not data or 'query' not in data:
            return jsonify({
                'error': 'Missing required parameter: query'
            }), 400
        
        query = data['query']
        num_results = data.get('num_results', 10)
        include_domains = data.get('include_domains')
        exclude_domains = data.get('exclude_domains')
        language = data.get('language', 'ru')
        
        # Выполнить поиск с фильтрами
        response = search_integration.search_with_filters(
            query=query,
            num_results=num_results,
            include_domains=include_domains,
            exclude_domains=exclude_domains,
            language=language
        )
        
        return jsonify(response.to_dict())
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500


def main():
    """Запустить API сервер"""
    print("=" * 60)
    print("Z.AI Search API для Kilo Code")
    print("=" * 60)
    print()
    print("Сервер запускается на http://localhost:5000")
    print()
    print("Доступные endpoints:")
    print("  GET  /api/health          - Проверка работы")
    print("  POST /api/search          - Поиск")
    print("  POST /api/search/batch    - Пакетный поиск")
    print("  POST /api/search/filtered - Поиск с фильтрами")
    print()
    print("Примеры запросов:")
    print()
    print("  curl -X POST http://localhost:5000/api/search \\")
    print("       -H 'Content-Type: application/json' \\")
    print("       -d '{\"query\": \"Python\", \"num_results\": 5}'")
    print()
    print("=" * 60)
    print()
    
    # Запустить сервер
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )


if __name__ == "__main__":
    main()
