"""
Примеры использования Z.AI Web Search Agent с Kilo Code
========================================================

Этот файл содержит примеры использования интеграции Z.AI
для поиска в интернете через Kilo Code.
"""

import os
import sys

# Добавляем путь к модулям
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ['ZAI_API_KEY'] = "dd54fffdba884bd09cf483bec7a2648b.RIzvuoiYh9iylV16"

from integrations import quick_search, KiloSearchIntegration

print("=" * 70)
print("ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ Z.AI WEB SEARCH")
print("=" * 70)

# =============================================================================
# ПРИМЕР 1: Быстрый поиск (quick_search)
# =============================================================================
print("\n" + "=" * 70)
print("ПРИМЕР 1: Быстрый поиск")
print("=" * 70)

results = quick_search("Python async programming", num_results=3)

print(f"\nНайдено {len(results)} результатов по запросу 'Python async programming':\n")
for result in results:
    print(f"{result.position}. {result.title}")
    print(f"   URL: {result.url}")
    print(f"   {result.snippet[:100]}...")
    print()

# =============================================================================
# ПРИМЕР 2: Поиск с фильтром по домену
# =============================================================================
print("=" * 70)
print("ПРИМЕР 2: Поиск с фильтром по домену")
print("=" * 70)

results = quick_search(
    "artificial intelligence", 
    num_results=3,
    domain_filter="wikipedia.org"
)

print(f"\nРезультаты с Wikipedia:\n")
for result in results:
    print(f"• {result.title}")
    print(f"  {result.url}\n")

# =============================================================================
# ПРИМЕР 3: Использование класса интеграции
# =============================================================================
print("=" * 70)
print("ПРИМЕР 3: Полная интеграция с KiloSearchIntegration")
print("=" * 70)

search = KiloSearchIntegration()

if search.is_ready():
    response = search.search("machine learning basics", num_results=3)
    
    print(f"\nСтатус: {response.status}")
    print(f"Запрос: {response.query}")
    print(f"Найдено: {response.total_results} результатов\n")
    
    for result in response.results:
        print(f"{result.position}. {result.title}")
        print(f"   Домен: {result.domain}")
        print(f"   {result.snippet[:80]}...\n")
else:
    print(f"Ошибка: {search.get_error()}")

# =============================================================================
# ПРИМЕР 4: Пакетный поиск
# =============================================================================
print("=" * 70)
print("ПРИМЕР 4: Пакетный поиск (несколько запросов)")
print("=" * 70)

queries = [
    "Python best practices",
    "JavaScript frameworks 2025",
    "Docker containers tutorial"
]

search = KiloSearchIntegration()
responses = search.batch_search(queries, num_results=2)

for response in responses:
    print(f"\n>> {response.query}")
    for result in response.results:
        print(f"   • {result.title}")

# =============================================================================
# ПРИМЕР 5: Экспорт в JSON
# =============================================================================
print("\n" + "=" * 70)
print("ПРИМЕР 5: Экспорт результатов в JSON")
print("=" * 70)

results = quick_search("TypeScript tutorial", num_results=2)

if results:
    print("\nJSON формат первого результата:")
    print(results[0].to_json())

print("\n" + "=" * 70)
print("✅ ВСЕ ПРИМЕРЫ ВЫПОЛНЕНЫ!")
print("=" * 70)
print("\nДля использования в вашем проекте:")
print("1. Установите API ключ: set ZAI_API_KEY=ваш_ключ")
print("2. Импортируйте: from integrations import quick_search")
print("3. Используйте: results = quick_search('query', num_results=5)")
print()
