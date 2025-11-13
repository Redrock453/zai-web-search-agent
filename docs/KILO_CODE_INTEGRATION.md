# Интеграция Z.AI Search Agent с Kilo Code через YAML

## 🎯 Быстрая интеграция (3 шага)

### Шаг 1: Создать конфигурационный файл

Создайте `config/kilo_code.yaml` в вашем проекте:

```yaml
api:
  api_key: ${ZAI_API_KEY}  # Из переменной окружения
  base_url: "https://api.z.ai/v1"
  timeout: 30

search_defaults:
  language: "ru"
  num_results: 10

kilo_code:
  enabled: true
  api_port: 5000
```

### Шаг 2: Установить зависимости

```bash
pip install PyYAML requests python-dotenv
```

### Шаг 3: Использовать в коде

```python
from integrations.yaml_loader import load_agent_from_yaml

# Загрузить агента
agent = load_agent_from_yaml('config/kilo_code.yaml')

# Выполнить поиск
response = agent.search("Python programming")

# Использовать результаты
for result in response.results:
    print(f"{result.title} - {result.url}")
```

## 📋 Полный пример конфигурации

См. файл `config/kilo_code.yaml` для полной конфигурации со всеми опциями.

## 🌍 Профили окружений

Используйте разные настройки для development/production:

```yaml
profiles:
  development:
    api:
      timeout: 15
    logging:
      level: "DEBUG"
  
  production:
    api:
      timeout: 45
    logging:
      level: "WARNING"
```

Загрузка с профилем:

```python
# Development
agent = load_agent_from_yaml('config/kilo_code.yaml', profile='development')

# Production  
agent = load_agent_from_yaml('config/kilo_code.yaml', profile='production')
```

## 🔌 Варианты интеграции

### 1. Прямая интеграция (Python)

```python
from integrations import load_agent_from_yaml

agent = load_agent_from_yaml('config/kilo_code.yaml')
results = agent.search("query")
```

### 2. REST API сервер

```bash
# Запустить сервер
python integrations/kilo_code_api.py

# Использовать
curl -X POST http://localhost:5000/api/search \
     -H "Content-Type: application/json" \
     -d '{"query": "Python", "num_results": 5}'
```

### 3. Быстрые функции

```python
from integrations import init_search, quick_search

init_search()
results = quick_search("Python", num_results=5)
```

### 4. JSON формат

```python
from integrations import search_json

json_results = search_json("Python", num_results=5)
print(json_results)
```

## 📖 Примеры

Запустите примеры:

```bash
python examples/kilo_code_example.py
```

## 🛠️ Настройка

### Переменные окружения

```bash
# Linux/Mac
export ZAI_API_KEY="ваш_api_ключ"

# Windows PowerShell
$env:ZAI_API_KEY="ваш_api_ключ"

# Или создайте .env файл
echo "ZAI_API_KEY=ваш_api_ключ" > .env
```

### Выбор профиля через переменную

```bash
export AGENT_PROFILE="production"
```

## 📚 Документация

- **Полная документация**: `docs/configuration.md`
- **Примеры использования**: `examples/kilo_code_example.py`
- **Конфигурация**: `config/kilo_code.yaml`
- **Интеграция**: `integrations/README.md`

## 🔧 Устранение проблем

### Ошибка: "Config file not found"

```bash
# Убедитесь, что файл существует
ls config/kilo_code.yaml

# Или создайте из шаблона
cp config/agent.yaml config/kilo_code.yaml
```

### Ошибка аутентификации

```bash
# Проверьте API ключ
echo $ZAI_API_KEY

# Установите если не установлен
export ZAI_API_KEY="ваш_ключ"
```

### Проверка конфигурации

```python
from integrations.yaml_loader import load_config_from_yaml

config = load_config_from_yaml('config/kilo_code.yaml')
print(config)
```

## 💡 Советы

1. **Безопасность**: Никогда не храните API ключи в YAML файлах - используйте переменные окружения
2. **Профили**: Используйте разные профили для dev/staging/prod
3. **Кэширование**: Включите кэширование для часто повторяющихся запросов
4. **Логирование**: Настройте уровень логов в зависимости от окружения

## 🚀 Готовые скрипты

### Запуск API сервера

```bash
python integrations/kilo_code_api.py
```

### Тестирование конфигурации

```bash
python -c "from integrations import load_agent_from_yaml; \
           agent = load_agent_from_yaml('config/kilo_code.yaml'); \
           print('✓ Конфигурация загружена успешно')"
```

### Быстрый поиск из командной строки

```bash
python -c "from integrations import quick_search; \
           import json; \
           print(json.dumps(quick_search('Python'), indent=2))"
```

## 📞 Поддержка

При проблемах проверьте:
1. ✅ Файл конфигурации существует
2. ✅ API ключ установлен в переменной окружения
3. ✅ Зависимости установлены (PyYAML, requests)
4. ✅ Логи для деталей ошибок

---

**Готово к использованию!** 🎉

Начните с запуска примеров:
```bash
python examples/kilo_code_example.py
```
