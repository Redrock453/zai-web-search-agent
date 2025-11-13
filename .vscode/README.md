# VS Code Integration для Z.AI Search Agent

## 🎯 Быстрый старт

### 1. Установка расширений

VS Code предложит установить рекомендуемые расширения автоматически. Или установите вручную:

- **Python** - Основная поддержка Python
- **Pylance** - IntelliSense и подсказки
- **Black Formatter** - Форматирование кода
- **YAML** - Поддержка YAML конфигураций
- **GitHub Copilot** - AI-помощник (опционально)

### 2. Настройка окружения

```powershell
# Создать виртуальное окружение
python -m venv .venv

# Активировать
.\.venv\Scripts\Activate.ps1

# Установить зависимости
pip install -r requirements.txt
pip install -r requirements-yaml.txt
```

### 3. Настройка API ключа

Создайте файл `.env` в корне проекта:
```env
ZAI_API_KEY=ваш_api_ключ_здесь
```

## 🚀 Использование

### Tasks (Задачи)

Нажмите `Ctrl+Shift+B` для выбора задачи:

- **Start Z.AI Search Agent** - Запустить API сервер
- **Test Search Agent** - Запустить тесты
- **Run Kilo Code Examples** - Примеры интеграции
- **Quick Search (Interactive)** - Интерактивный поиск
- **Install Dependencies** - Установить зависимости

### Debug Configurations (Отладка)

Нажмите `F5` или используйте панель Debug:

- **Z.AI Search API Server** - Запуск с отладкой
- **Run Kilo Code Example** - Примеры с отладкой
- **Run Current File** - Запустить текущий файл
- **Run Tests** - Тесты с отладкой

### Snippets (Сниппеты)

Начните печатать в Python файле:

- `zai-search` → Быстрый поиск
- `zai-yaml` → Загрузка из YAML
- `zai-integration` → Полная интеграция
- `zai-batch` → Пакетный поиск
- `zai-config` → Работа с конфигурацией
- `zai-test` → Шаблон теста

## 📁 Структура проекта в VS Code

```
zai-web-search-agent/
├── .vscode/              ← VS Code конфигурация
│   ├── tasks.json        ← Задачи (Ctrl+Shift+B)
│   ├── launch.json       ← Отладка (F5)
│   ├── settings.json     ← Настройки проекта
│   ├── extensions.json   ← Рекомендуемые расширения
│   └── snippets.code-snippets  ← Сниппеты
├── src/                  ← Исходный код агента
├── integrations/         ← Модули интеграции
├── config/               ← YAML конфигурации
├── examples/             ← Примеры использования
├── tests/                ← Тесты
└── docs/                 ← Документация
```

## 🔧 Полезные команды

### В терминале VS Code

```powershell
# Запустить API сервер
python integrations/kilo_code_api.py

# Быстрый поиск
python -c "from integrations import quick_search; print(quick_search('Python', 5))"

# Тесты
pytest tests/ -v

# Примеры
python examples/kilo_code_example.py
```

### Горячие клавиши

- `Ctrl+Shift+B` - Запустить задачу
- `F5` - Начать отладку
- `Ctrl+Shift+P` - Command Palette
- `Ctrl+` ` - Открыть терминал
- `Ctrl+Shift+X` - Расширения
- `Ctrl+Shift+E` - Explorer

## 🎨 IntelliSense и Autocomplete

VS Code автоматически предоставит:

- **Подсказки типов** для всех классов и методов
- **Автодополнение** для функций и параметров
- **Документацию** при наведении
- **Go to Definition** (F12)
- **Find References** (Shift+F12)

## 🧪 Тестирование

### Запуск тестов

1. **Через UI**: 
   - Откройте панель Testing (Ctrl+Shift+P → "Test: Focus on Test Explorer View")
   - Выберите и запустите тесты

2. **Через Task**:
   - Ctrl+Shift+B → "Test Search Agent"

3. **Через терминал**:
   ```powershell
   pytest tests/ -v --cov=src
   ```

### Отладка тестов

- Установите breakpoint в тесте
- Нажмите F5 → "Run Tests"
- Или используйте кнопку Debug на конкретном тесте

## 📝 YAML конфигурация

VS Code предоставляет:

- **Syntax highlighting** для YAML
- **Автодополнение** структуры
- **Валидация** схемы
- **Форматирование** при сохранении

Откройте `config/agent.yaml` или `config/kilo_code.yaml` для редактирования.

## 🔌 REST API в VS Code

### Запуск сервера

1. **Debug mode**: F5 → "Z.AI Search API Server"
2. **Task**: Ctrl+Shift+B → "Start Z.AI Search Agent"
3. **Terminal**: `python integrations/kilo_code_api.py`

### Тестирование API

Используйте расширение **REST Client** или **Thunder Client**:

```http
### Quick Search
POST http://localhost:5000/api/search
Content-Type: application/json

{
  "query": "Python programming",
  "num_results": 5
}

### Batch Search
POST http://localhost:5000/api/search/batch
Content-Type: application/json

{
  "queries": ["Python", "JavaScript", "Java"],
  "num_results": 3
}
```

## 🐛 Отладка

### Breakpoints

1. Кликните слева от номера строки
2. Запустите отладку (F5)
3. Используйте панель Debug для навигации

### Debug Console

Доступны все переменные:
```python
# В Debug Console
agent.config.api_key
response.results[0].title
```

### Логирование

Логи отображаются в:
- **Debug Console** при отладке
- **Terminal** при обычном запуске

## 💡 Советы

1. **Auto-save**: File → Auto Save (экономит время)
2. **Multi-cursor**: Alt+Click (редактирование в нескольких местах)
3. **Command Palette**: Ctrl+Shift+P (доступ ко всем командам)
4. **Integrated Terminal**: Ctrl+` (быстрый доступ)
5. **Git Integration**: Source Control панель (Ctrl+Shift+G)

## 🔄 Workflow

### Типичный workflow разработки:

1. **Открыть проект** в VS Code
2. **Активировать venv**: Terminal → `.\.venv\Scripts\Activate.ps1`
3. **Установить зависимости**: Ctrl+Shift+B → "Install Dependencies"
4. **Редактировать код** с IntelliSense
5. **Запустить тесты**: Ctrl+Shift+B → "Test Search Agent"
6. **Отладка**: F5 → выбрать конфигурацию
7. **Commit**: Source Control → Commit

## 📚 Дополнительные ресурсы

- [Python в VS Code](https://code.visualstudio.com/docs/python/python-tutorial)
- [Debugging](https://code.visualstudio.com/docs/editor/debugging)
- [Tasks](https://code.visualstudio.com/docs/editor/tasks)
- [Snippets](https://code.visualstudio.com/docs/editor/userdefinedsnippets)

---

**Готово к использованию!** 🎉

Нажмите `Ctrl+Shift+B` и выберите задачу для начала работы.
