# ⌨️ VS Code - Горячие клавиши для Z.AI Agent

## 🎯 Главные команды

| Комбинация | Действие | Описание |
|------------|----------|----------|
| `Ctrl+Shift+B` | **Build Tasks** | Показать все задачи проекта |
| `F5` | **Start Debugging** | Запустить отладку |
| `Ctrl+Shift+P` | **Command Palette** | Все команды VS Code |
| `Ctrl+` ` | **Terminal** | Открыть/закрыть терминал |

## 🚀 Задачи (Ctrl+Shift+B)

После нажатия выберите:

1. **Start Z.AI Search Agent** 
   - Запускает REST API сервер
   - `http://localhost:5000`

2. **Test Search Agent**
   - Запускает все тесты
   - Показывает coverage

3. **Run Kilo Code Examples**
   - Демонстрация всех возможностей
   - Интеграция с Kilo Code

4. **Quick Search (Interactive)**
   - Интерактивный поиск в терминале
   - Введите запрос → получите результаты

5. **Install Dependencies**
   - Установка всех зависимостей
   - requirements.txt + requirements-yaml.txt

## 🐛 Отладка (F5)

После нажатия выберите:

1. **Z.AI Search API Server**
   - Отладка API сервера
   - Breakpoints в API endpoints

2. **Run Kilo Code Example**
   - Отладка примеров интеграции
   - Пошаговое выполнение

3. **Run Current File**
   - Отладка активного файла
   - Универсальная конфигурация

4. **Run Tests**
   - Отладка тестов
   - С coverage

5. **Debug Test File**
   - Отладка одного тестового файла
   - Для быстрой проверки

## ✂️ Сниппеты

В любом `.py` файле печатайте:

### `zai-search` + Tab
```python
from integrations import quick_search

results = quick_search("query", num_results=5)
for result in results['results']:
    print(f"{result['title']} - {result['url']}")
```

### `zai-yaml` + Tab
```python
from integrations.yaml_loader import load_agent_from_yaml

agent = load_agent_from_yaml('config/kilo_code.yaml')
response = agent.search("query", num_results=10)

for result in response.results:
    print(f"{result.title} - {result.url}")
```

### `zai-integration` + Tab
```python
from integrations import KiloSearchIntegration

search = KiloSearchIntegration()

if search.is_ready():
    response = search.search("query", num_results=10)
    # ... полный шаблон
```

### `zai-batch` + Tab
```python
from integrations import KiloSearchIntegration

search = KiloSearchIntegration()
queries = ["query1", "query2", "query3"]

results = search.search_multiple(queries, num_results=5)
# ... полный шаблон
```

### `zai-config` + Tab
```python
from integrations.yaml_loader import YAMLConfigLoader

loader = YAMLConfigLoader('config/agent.yaml')
config = loader.load()
# ... полный шаблон
```

### `zai-test` + Tab
```python
import pytest
from integrations import KiloSearchIntegration

def test_search_functionality():
    """Test description"""
    # Arrange, Act, Assert шаблон
```

## 🔍 Навигация

| Комбинация | Действие |
|------------|----------|
| `Ctrl+P` | Быстрый поиск файлов |
| `Ctrl+Shift+F` | Поиск в проекте |
| `F12` | Перейти к определению |
| `Alt+F12` | Peek определение |
| `Shift+F12` | Найти все ссылки |
| `Ctrl+Shift+O` | Символы в файле |
| `Ctrl+T` | Символы в workspace |

## ✏️ Редактирование

| Комбинация | Действие |
|------------|----------|
| `Alt+Click` | Добавить курсор |
| `Ctrl+D` | Выбрать следующее вхождение |
| `Ctrl+Shift+L` | Выбрать все вхождения |
| `Alt+↑/↓` | Переместить строку |
| `Shift+Alt+↑/↓` | Копировать строку |
| `Ctrl+/` | Закомментировать |
| `Ctrl+Shift+K` | Удалить строку |
| `Ctrl+Enter` | Вставить строку ниже |
| `Ctrl+Shift+Enter` | Вставить строку выше |

## 📂 Explorer

| Комбинация | Действие |
|------------|----------|
| `Ctrl+Shift+E` | Открыть Explorer |
| `Ctrl+K Ctrl+E` | Фокус на Explorer |
| `Ctrl+B` | Toggle sidebar |

## 🔬 Testing

| Комбинация | Действие |
|------------|----------|
| `Ctrl+Shift+P` → Test | Открыть Test Explorer |
| Кликните ▶️ | Запустить тест |
| Кликните 🐛 | Отладить тест |

## 🌐 Terminal

| Комбинация | Действие |
|------------|----------|
| `Ctrl+` ` | Открыть/закрыть |
| `Ctrl+Shift+` ` | Новый терминал |
| `Ctrl+PgUp/PgDn` | Переключить терминал |

## 🎨 Интерфейс

| Комбинация | Действие |
|------------|----------|
| `Ctrl+K Z` | Zen Mode |
| `F11` | Fullscreen |
| `Ctrl+=/-` | Zoom |
| `Ctrl+B` | Toggle Sidebar |
| `Ctrl+J` | Toggle Panel |

## 🔧 Git

| Комбинация | Действие |
|------------|----------|
| `Ctrl+Shift+G` | Открыть Source Control |
| `Ctrl+Shift+P` → Git | Git команды |

## 💾 Файлы

| Комбинация | Действие |
|------------|----------|
| `Ctrl+N` | Новый файл |
| `Ctrl+O` | Открыть файл |
| `Ctrl+S` | Сохранить |
| `Ctrl+Shift+S` | Сохранить как |
| `Ctrl+W` | Закрыть файл |
| `Ctrl+K W` | Закрыть все |

## 🎯 Быстрые действия

### Запустить поиск сейчас

```
Ctrl+Shift+B → "Quick Search (Interactive)" → Enter
```

### Отладить пример

```
F5 → "Run Kilo Code Example" → Enter
```

### Тесты с coverage

```
Ctrl+Shift+B → "Test Search Agent" → Enter
```

### API сервер

```
Ctrl+Shift+B → "Start Z.AI Search Agent" → Enter
```

### Новый код с сниппетом

```
Ctrl+N → печатайте "zai-yaml" → Tab → заполните → F5
```

## 📚 Ресурсы

- **Справка по клавишам**: `Ctrl+K Ctrl+R`
- **Keyboard Shortcuts**: `Ctrl+K Ctrl+S`
- **Command Palette**: `Ctrl+Shift+P`

## 💡 Pro Tips

1. **Мультикурсор**: Выделите текст → `Ctrl+D` несколько раз
2. **Переименование**: `F2` на символе
3. **Format**: `Shift+Alt+F` (или авто при сохранении)
4. **Quick Fix**: `Ctrl+.` на ошибке
5. **IntelliSense**: `Ctrl+Space`

---

**Распечатайте эту шпаргалку и держите под рукой!** 📎
