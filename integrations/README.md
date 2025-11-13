# Интеграция Z.AI Search Agent с Kilo Code

Этот модуль предоставляет простые способы интеграции Z.AI Web Search Agent в ваш проект Kilo Code.

## 📦 Компоненты

### 1. `kilo_code_integration.py`
Основной модуль интеграции с удобными классами и функциями.

### 2. `kilo_code_api.py`
REST API сервер для использования через HTTP запросы.

## 🚀 Быстрый старт

### Вариант 1: Через YAML конфигурацию (Рекомендуется для Kilo Code)

**Создайте файл `config/agent.yaml`:**

```yaml
api:
  api_key: ${ZAI_API_KEY}
  timeout: 30
  
search_defaults:
  language: "ru"
  num_results: 10
  
kilo_code:
  enabled: true
  api_port: 5000
```

**Используйте в коде:**

```python
from integrations.yaml_loader import load_agent_from_yaml

# Загрузить агента из YAML
agent = load_agent_from_yaml('config/agent.yaml')

# Использовать
response = agent.search("Python programming")
print(response.results)
```

**С профилями окружений:**

```python
# Development
agent = load_agent_from_yaml('config/agent.yaml', profile='development')

# Production
agent = load_agent_from_yaml('config/agent.yaml', profile='production')
```

### Вариант 2: Прямая интеграция (Python)

```python
from integrations.kilo_code_integration import KiloSearchIntegration

# Создать экземпляр
search = KiloSearchIntegration()

# Выполнить поиск
response = search.search("Python программирование", num_results=5)

# Использовать результаты
print(f"Найдено: {response.total_results}")
for result in response.results:
    print(f"{result.title} - {result.url}")
```

### Вариант 3: Через REST API

**Запустить сервер:**
```bash
cd c:\zai-web-search-agent\integrations
python kilo_code_api.py
```

**Выполнить запрос (curl):**
```bash
curl -X POST http://localhost:5000/api/search \
     -H "Content-Type: application/json" \
     -d '{"query": "искусственный интеллект", "num_results": 5}'
```

**Выполнить запрос (JavaScript):**
```javascript
fetch('http://localhost:5000/api/search', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    query: 'машинное обучение',
    num_results: 5,
    language: 'ru'
  })
})
.then(response => response.json())
.then(data => {
  console.log('Результаты:', data.results);
});
```

**Выполнить запрос (PowerShell):**
```powershell
$body = @{
    query = "Python программирование"
    num_results = 5
    language = "ru"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/api/search" `
                  -Method Post `
                  -ContentType "application/json" `
                  -Body $body
```

### Вариант 4: Быстрые функции

```python
from integrations.kilo_code_integration import init_search, quick_search

# Инициализировать один раз
init_search()

# Использовать в любом месте
results = quick_search("Python", num_results=3)
print(results)
```

## 📚 API Endpoints

### GET /api/health
Проверка работы сервера.

**Response:**
```json
{
  "status": "ok",
  "service": "Z.AI Search API",
  "ready": true,
  "error": null
}
```

### POST /api/search
Выполнить поиск.

**Request:**
```json
{
  "query": "поисковый запрос",
  "num_results": 10,
  "language": "ru",
  "region": "RU",
  "safe_search": "moderate"
}
```

**Response:**
```json
{
  "query": "поисковый запрос",
  "total_results": 1000,
  "results_count": 10,
  "search_time": 0.5,
  "status": "success",
  "results": [
    {
      "title": "Заголовок",
      "url": "https://example.com",
      "snippet": "Описание...",
      "position": 1,
      "domain": "example.com"
    }
  ]
}
```

### POST /api/search/batch
Пакетный поиск нескольких запросов.

**Request:**
```json
{
  "queries": ["запрос 1", "запрос 2", "запрос 3"],
  "num_results": 5
}
```

**Response:**
```json
[
  {
    "query": "запрос 1",
    "results": [...]
  },
  {
    "query": "запрос 2",
    "results": [...]
  }
]
```

### POST /api/search/filtered
Поиск с фильтрацией доменов.

**Request:**
```json
{
  "query": "Python tutorial",
  "num_results": 10,
  "include_domains": ["python.org"],
  "exclude_domains": ["spam.com"],
  "language": "en"
}
```

## 🔧 Настройка

### Переменные окружения

Создайте файл `.env` в корне проекта:
```env
ZAI_API_KEY=ваш_api_ключ
ZAI_API_BASE_URL=https://api.zai.com/v1
```

### Программная настройка

```python
from integrations.kilo_code_integration import KiloSearchIntegration

# С API ключом
search = KiloSearchIntegration(api_key="ваш_ключ")

# С кастомными настройками
search = KiloSearchIntegration(
    api_key="ваш_ключ",
    max_retries=5,
    timeout=60.0
)
```

## 💡 Примеры использования

### Пример 1: Базовый поиск
```python
from integrations.kilo_code_integration import KiloSearchIntegration

search = KiloSearchIntegration()
response = search.search("Python", num_results=5)

for result in response.results:
    print(f"{result.title}")
    print(f"  URL: {result.url}")
    print(f"  Snippet: {result.snippet}")
```

### Пример 2: JSON формат
```python
from integrations.kilo_code_integration import search_json

# Получить результаты в JSON
json_results = search_json("машинное обучение", num_results=3)
print(json_results)
```

### Пример 3: Поиск с фильтрами
```python
search = KiloSearchIntegration()

# Только образовательные сайты
response = search.search_with_filters(
    query="Python tutorial",
    include_domains=["python.org", "realpython.com"],
    num_results=5
)
```

### Пример 4: Множественный поиск
```python
search = KiloSearchIntegration()

queries = ["Python", "JavaScript", "Java"]
results = search.search_multiple(queries, num_results=3)

for response in results:
    print(f"\nЗапрос: {response.query}")
    print(f"Найдено: {response.total_results}")
```

## 🔌 Интеграция в Kilo Code

### Способ 1: Как модуль

Скопируйте файлы в ваш проект Kilo Code:
```
kilo-code/
├── integrations/
│   ├── __init__.py
│   ├── kilo_code_integration.py
│   └── kilo_code_api.py
```

Затем импортируйте:
```python
from integrations.kilo_code_integration import KiloSearchIntegration
```

### Способ 2: Как микросервис

Запустите API сервер отдельно и делайте HTTP запросы из Kilo Code:

```python
import requests

def search_from_kilo(query):
    response = requests.post(
        'http://localhost:5000/api/search',
        json={'query': query, 'num_results': 5}
    )
    return response.json()

# Использование
results = search_from_kilo("Python")
```

### Способ 3: Через CLI

Используйте из командной строки:
```bash
# Создайте wrapper скрипт
python -c "from integrations.kilo_code_integration import search_json; print(search_json('Python', 5))"
```

## 📋 Требования

- Python 3.7+
- Z.AI API ключ
- Зависимости:
  ```bash
  pip install requests python-dotenv
  pip install flask flask-cors  # Для API сервера
  ```

## 🐛 Устранение проблем

### Ошибка аутентификации
```python
search = KiloSearchIntegration()
if not search.is_ready():
    print(f"Ошибка: {search.get_error()}")
```

### Проверка статуса API
```bash
curl http://localhost:5000/api/health
```

### Логирование
```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Теперь увидите детали запросов
search = KiloSearchIntegration()
```

## 📞 Поддержка

При проблемах проверьте:
1. Правильность API ключа в `.env`
2. Доступность API сервера
3. Логи ошибок в консоли

## 📄 Лицензия

MIT License - свободно используйте в ваших проектах!
