# Z.AI Search Agent - Краткая справка 🚀

## Быстрый старт в VS Code

### 1. Откройте проект
```
File → Open Folder → c:\zai-web-search-agent
```

### 2. Установите расширения
VS Code предложит автоматически. Или:
- Ctrl+Shift+X → Поиск "Python" → Install

### 3. Настройте API ключ
Создайте `.env`:
```env
ZAI_API_KEY=ваш_ключ
```

### 4. Используйте!

## ⚡ Горячие клавиши

| Комбинация | Действие |
|------------|----------|
| `Ctrl+Shift+B` | **Задачи** (Build Tasks) |
| `F5` | **Отладка** (Start Debugging) |
| `Ctrl+Shift+P` | **Command Palette** |
| `Ctrl+` ` | **Терминал** |
| `Ctrl+Shift+E` | **Explorer** |
| `Ctrl+Shift+X` | **Расширения** |
| `Ctrl+Shift+G` | **Git** |

## 🎯 Основные задачи

### Запустить API сервер
```
Ctrl+Shift+B → "Start Z.AI Search Agent"
```
Или в терминале:
```powershell
python integrations/kilo_code_api.py
```

### Запустить примеры
```
Ctrl+Shift+B → "Run Kilo Code Examples"
```

### Запустить тесты
```
Ctrl+Shift+B → "Test Search Agent"
```

### Интерактивный поиск
```
Ctrl+Shift+B → "Quick Search (Interactive)"
```

## 📝 Code Snippets

В любом `.py` файле начните печатать:

### `zai-search` - Быстрый поиск
```python
from integrations import quick_search

results = quick_search("query", num_results=5)
for result in results['results']:
    print(f"{result['title']} - {result['url']}")
```

### `zai-yaml` - Из YAML
```python
from integrations.yaml_loader import load_agent_from_yaml

agent = load_agent_from_yaml('config/kilo_code.yaml')
response = agent.search("query", num_results=10)

for result in response.results:
    print(f"{result.title} - {result.url}")
```

### `zai-integration` - Полная интеграция
```python
from integrations import KiloSearchIntegration

search = KiloSearchIntegration()

if search.is_ready():
    response = search.search("query", num_results=10)
    
    if response.status == 'success':
        for result in response.results:
            print(f"{result.title} - {result.url}")
```

## 🔧 Часто используемые команды

### В терминале (Ctrl+`)

```powershell
# Активировать venv
.\.venv\Scripts\Activate.ps1

# Запустить API
python integrations/kilo_code_api.py

# Тесты
pytest tests/ -v

# Примеры
python examples/kilo_code_example.py

# Быстрый поиск
python -c "from integrations import quick_search; print(quick_search('Python', 3))"
```

## 🐛 Отладка

### Breakpoint
1. Кликните слева от номера строки (появится красная точка)
2. F5 → Выберите конфигурацию
3. Используйте панель Debug для навигации

### Debug Console
При отладке доступны все переменные:
```python
agent.config.api_key
response.results[0].title
```

## 📚 Файлы конфигурации

### `.vscode/tasks.json` - Задачи
Определяет задачи (Ctrl+Shift+B)

### `.vscode/launch.json` - Отладка  
Определяет конфигурации отладки (F5)

### `.vscode/settings.json` - Настройки
Настройки проекта (Python interpreter, форматирование)

### `.vscode/snippets.code-snippets` - Сниппеты
Шаблоны кода (начните печатать `zai-`)

## 🌐 REST API endpoints

После запуска сервера (`Ctrl+Shift+B → "Start Z.AI Search Agent"`):

```http
GET  http://localhost:5000/api/health
POST http://localhost:5000/api/search
POST http://localhost:5000/api/search/batch
POST http://localhost:5000/api/search/filtered
```

### Пример запроса (PowerShell):
```powershell
$body = @{
    query = "Python"
    num_results = 5
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/api/search" `
                  -Method Post `
                  -ContentType "application/json" `
                  -Body $body
```

## 📖 Документация

- **Главная**: `README.md`
- **VS Code**: `.vscode/README.md`
- **Kilo Code**: `docs/KILO_CODE_INTEGRATION.md`
- **Конфигурация**: `docs/configuration.md`
- **Примеры**: `examples/`

## 💡 Советы

1. **Auto-save**: File → Auto Save
2. **Format on Save**: Автоматически (уже настроено)
3. **Multi-cursor**: Alt+Click
4. **Duplicate Line**: Shift+Alt+↓
5. **Move Line**: Alt+↓
6. **Comment**: Ctrl+/

## 🚦 Workflow

1. Откройте файл (Ctrl+P → имя файла)
2. Редактируйте с IntelliSense
3. Сохраните (Ctrl+S) - автоформатирование
4. Запустите/Отладьте (F5)
5. Тесты (Ctrl+Shift+B → "Test")
6. Commit (Ctrl+Shift+G)

## ✅ Checklist для начала

- [ ] Открыть проект в VS Code
- [ ] Установить рекомендуемые расширения
- [ ] Создать `.env` с API ключом
- [ ] Активировать venv
- [ ] Установить зависимости (Ctrl+Shift+B → "Install Dependencies")
- [ ] Запустить примеры (Ctrl+Shift+B → "Run Kilo Code Examples")
- [ ] Попробовать интерактивный поиск (Ctrl+Shift+B → "Quick Search")

## 🎓 Ресурсы

- [VS Code Python Tutorial](https://code.visualstudio.com/docs/python/python-tutorial)
- [Debugging](https://code.visualstudio.com/docs/editor/debugging)
- [Tasks](https://code.visualstudio.com/docs/editor/tasks)

---

**Готово! Нажмите `Ctrl+Shift+B` для начала работы** 🎉
