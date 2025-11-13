"""
Пример использования Z.AI Search Agent в Kilo Code
===================================================

Этот скрипт демонстрирует различные способы использования
Z.AI Search Agent с YAML конфигурацией для интеграции в Kilo Code.
"""

import os
import sys

# Добавляем пути
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from integrations import (
    load_agent_from_yaml,
    load_config_from_yaml,
    KiloSearchIntegration,
    quick_search
)


def example_1_basic_yaml():
    """
    Пример 1: Базовое использование с YAML
    """
    print("=" * 60)
    print("ПРИМЕР 1: Базовое использование с YAML конфигурацией")
    print("=" * 60)
    
    try:
        # Загрузить агента из YAML файла
        agent = load_agent_from_yaml('config/kilo_code.yaml')
        
        # Выполнить поиск
        response = agent.search("Python программирование", num_results=5)
        
        print(f"\nЗапрос: {response.query}")
        print(f"Найдено: {response.total_results} результатов")
        print(f"Время поиска: {response.search_time:.2f}s")
        print(f"\nПервые 3 результата:")
        
        for result in response.results[:3]:
            print(f"\n{result.position}. {result.title}")
            print(f"   URL: {result.url}")
            print(f"   {result.snippet[:100]}...")
        
    except FileNotFoundError:
        print("\n⚠️ Файл config/kilo_code.yaml не найден")
        print("   Создайте его из шаблона config/agent.yaml")
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")


def example_2_with_profile():
    """
    Пример 2: Использование профилей окружений
    """
    print("\n\n" + "=" * 60)
    print("ПРИМЕР 2: Использование профилей окружений")
    print("=" * 60)
    
    try:
        # Development профиль
        print("\n--- Development профиль ---")
        agent_dev = load_agent_from_yaml('config/kilo_code.yaml', profile='development')
        print("✓ Development агент загружен")
        
        # Production профиль
        print("\n--- Production профиль ---")
        agent_prod = load_agent_from_yaml('config/kilo_code.yaml', profile='production')
        print("✓ Production агент загружен")
        
        # Показать различия в настройках
        config_dev = load_config_from_yaml('config/kilo_code.yaml', profile='development')
        config_prod = load_config_from_yaml('config/kilo_code.yaml', profile='production')
        
        print(f"\nDevelopment timeout: {config_dev['api']['timeout']}s")
        print(f"Production timeout: {config_prod['api']['timeout']}s")
        
    except FileNotFoundError:
        print("\n⚠️ Файл config/kilo_code.yaml не найден")
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")


def example_3_kilo_integration():
    """
    Пример 3: Интеграция с Kilo Code
    """
    print("\n\n" + "=" * 60)
    print("ПРИМЕР 3: Прямая интеграция с Kilo Code")
    print("=" * 60)
    
    try:
        # Создать интеграцию
        search = KiloSearchIntegration()
        
        if not search.is_ready():
            print(f"\n❌ Ошибка инициализации: {search.get_error()}")
            return
        
        # Выполнить поиск
        response = search.search(
            query="машинное обучение",
            num_results=3,
            language="ru"
        )
        
        # Вывести в формате для Kilo Code
        print(f"\nСтатус: {response.status}")
        print(f"Запрос: {response.query}")
        print(f"Результатов: {len(response.results)}")
        
        # JSON формат для Kilo Code API
        print(f"\nJSON ответ (первые 200 символов):")
        json_response = response.to_json()
        print(json_response[:200] + "...")
        
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")


def example_4_batch_search():
    """
    Пример 4: Пакетный поиск для Kilo Code
    """
    print("\n\n" + "=" * 60)
    print("ПРИМЕР 4: Пакетный поиск")
    print("=" * 60)
    
    try:
        search = KiloSearchIntegration()
        
        # Список запросов
        queries = [
            "Python программирование",
            "JavaScript разработка",
            "искусственный интеллект"
        ]
        
        # Выполнить пакетный поиск
        results = search.search_multiple(queries, num_results=2)
        
        print(f"\nВыполнено запросов: {len(results)}")
        
        for i, response in enumerate(results, 1):
            print(f"\n{i}. Запрос: '{response.query}'")
            print(f"   Статус: {response.status}")
            print(f"   Результатов: {len(response.results)}")
            if response.results:
                print(f"   Первый результат: {response.results[0].title[:50]}...")
        
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")


def example_5_filtered_search():
    """
    Пример 5: Поиск с фильтрацией
    """
    print("\n\n" + "=" * 60)
    print("ПРИМЕР 5: Поиск с фильтрацией доменов")
    print("=" * 60)
    
    try:
        search = KiloSearchIntegration()
        
        # Поиск только на образовательных сайтах
        response = search.search_with_filters(
            query="Python tutorial",
            num_results=5,
            include_domains=["python.org", "docs.python.org", "realpython.com"],
            language="en"
        )
        
        print(f"\nЗапрос: {response.query}")
        print(f"Фильтр доменов: python.org, docs.python.org, realpython.com")
        print(f"Найдено: {len(response.results)} результатов")
        
        print(f"\nРезультаты:")
        for result in response.results:
            print(f"  • {result.title}")
            print(f"    {result.domain}")
        
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")


def example_6_quick_functions():
    """
    Пример 6: Быстрые функции-хелперы
    """
    print("\n\n" + "=" * 60)
    print("ПРИМЕР 6: Быстрые функции для Kilo Code")
    print("=" * 60)
    
    try:
        from integrations import init_search, search_json
        
        # Инициализировать один раз
        init_search()
        
        # Использовать быстрый поиск
        result1 = quick_search("нейронные сети", num_results=2)
        print(f"\nБыстрый поиск 1: {result1['query']}")
        print(f"Результатов: {result1['results_count']}")
        
        result2 = quick_search("глубокое обучение", num_results=2)
        print(f"\nБыстрый поиск 2: {result2['query']}")
        print(f"Результатов: {result2['results_count']}")
        
        # JSON формат
        print(f"\nJSON формат:")
        json_result = search_json("машинное обучение", num_results=1)
        print(json_result[:300] + "...")
        
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")


def example_7_config_reading():
    """
    Пример 7: Чтение конфигурации
    """
    print("\n\n" + "=" * 60)
    print("ПРИМЕР 7: Чтение и анализ конфигурации")
    print("=" * 60)
    
    try:
        from integrations.yaml_loader import YAMLConfigLoader
        
        # Загрузить конфигурацию
        loader = YAMLConfigLoader('config/kilo_code.yaml')
        config = loader.load()
        
        # Прочитать настройки Kilo Code
        print("\n📋 Настройки Kilo Code:")
        print(f"  Включено: {loader.get('kilo_code.enabled')}")
        print(f"  API порт: {loader.get('kilo_code.api_port')}")
        print(f"  API хост: {loader.get('kilo_code.api_host')}")
        print(f"  CORS: {loader.get('kilo_code.enable_cors')}")
        print(f"  Debug: {loader.get('kilo_code.debug')}")
        
        # Настройки поиска
        print("\n🔍 Настройки поиска:")
        print(f"  Язык: {loader.get('search_defaults.language')}")
        print(f"  Регион: {loader.get('search_defaults.region')}")
        print(f"  Результатов: {loader.get('search_defaults.num_results')}")
        
        # Доступные профили
        profiles = config.get('profiles', {})
        if profiles:
            print(f"\n🌍 Доступные профили: {', '.join(profiles.keys())}")
        
    except FileNotFoundError:
        print("\n⚠️ Файл config/kilo_code.yaml не найден")
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")


def main():
    """
    Запустить все примеры
    """
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║  Z.AI Search Agent - Примеры интеграции с Kilo Code     ║")
    print("╚" + "=" * 58 + "╝")
    
    # Проверить наличие API ключа
    if not os.environ.get('ZAI_API_KEY'):
        print("\n⚠️ ВНИМАНИЕ: Переменная окружения ZAI_API_KEY не установлена")
        print("   Некоторые примеры могут не работать")
        print("\n   Установите: export ZAI_API_KEY='ваш_ключ'")
        print("   или создайте файл .env с ZAI_API_KEY=ваш_ключ\n")
    
    # Запустить примеры
    example_1_basic_yaml()
    example_2_with_profile()
    example_3_kilo_integration()
    example_4_batch_search()
    example_5_filtered_search()
    example_6_quick_functions()
    example_7_config_reading()
    
    # Итоги
    print("\n\n" + "=" * 60)
    print("✅ ВСЕ ПРИМЕРЫ ЗАВЕРШЕНЫ!")
    print("=" * 60)
    
    print("\n📚 Для использования в Kilo Code:")
    print("   1. Создайте config/kilo_code.yaml из шаблона")
    print("   2. Установите ZAI_API_KEY")
    print("   3. Используйте:")
    print("      from integrations import load_agent_from_yaml")
    print("      agent = load_agent_from_yaml('config/kilo_code.yaml')")
    
    print("\n🌐 Для REST API:")
    print("   python integrations/kilo_code_api.py")
    print("   curl http://localhost:5000/api/search -d '{\"query\":\"test\"}'")
    
    print("\n")


if __name__ == "__main__":
    main()
