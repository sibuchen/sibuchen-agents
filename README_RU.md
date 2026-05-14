# SibuchenAgents

<div align="center">

**Модульный, расширяемый фреймворк AI-агентов на Python**
<!-- Динамические бейджи -->
[![PyPI version](https://img.shields.io/pypi/v/sibuchen-agents?label=Version&color=3775A9&logo=pypi&logoColor=3775A9)](https://pypi.org/project/sibuchen-agents/)
[![Python](https://img.shields.io/pypi/pyversions/sibuchen-agents?label=Python&color=3776AB&logo=python&logoColor=3776AB)](https://pypi.org/project/sibuchen-agents/)
<!-- Статические бейджи https://img.shields.io/badge/<左侧文字>-<右侧文字>-<颜色> -->
[![License](https://img.shields.io/badge/License-GPLv3-D6336C.svg?logo=GPLv3&logoColor=BD0000)](https://www.gnu.org/licenses/gpl-3.0)
[![GitHub](https://img.shields.io/badge/GitHub-sibuchen--agents-181717?logo=github&logoColor=181717)](https://github.com/sibuchen/sibuchen-agents)
[![Author](https://img.shields.io/badge/Author-sibuchen-orange?logo=github&logoColor=181717)](https://github.com/sibuchen/)

</div>

<p align="center">
  <a href="./README.md">English</a> | <a href="./README_CN.md">简体中文</a> | <a href="./README_TC.md">繁體中文</a> | <a href="./README_JP.md">日本語</a> | <a href="./README_RU.md">Русский</a>
</p>

SibuchenAgents -- это фреймворк AI-агентов на Python для разработчиков, предлагающий множество парадигм рассуждений, богатый набор встроенных инструментов, интеллектуальную систему памяти и многопротокольные коммуникационные возможности, позволяющие быстро создавать готовые к продакшену приложения на базе AI-агентов.

---

## Основные возможности

- **Множественные парадигмы рассуждений**: SimpleAgent、ReActAgent、FunctionCallAgent、ReflectionAgent、PlanAndSolveAgent、ToolAwareSimpleAgent
- **Поддержка нескольких LLM-бэкендов**: OpenAI、Google Gemini、DashScope (Alibaba Cloud) и любые OpenAI-совместимые интерфейсы
- **Богатый набор встроенных инструментов**: работа с файлами, выполнение терминальных команд, поисковые системы, RAG-извлечение, хранение памяти, управление задачами, калькулятор и ещё 14+ инструментов
- **Интеллектуальная система памяти**: управление историей диалога, векторное хранение (Qdrant), графовое хранение (Neo4j), RAG-извлечение
- **Поддержка нескольких протоколов**: MCP (Model Context Protocol)、A2A (Agent-to-Agent)、ANP (Agent Network Protocol)
- **Мгновенные сообщения (IM)**: на базе NoneBot2, поддержка Telegram, Feishu
- **Наблюдаемость**: полная запись цепочки трассировки и генерация HTML-отчётов
- **Инженерия контекста**: автоматическое сжатие контекста и интеллектуальная суммаризация
- **Механизм автоматического выключателя**: автоматический выключатель выполнения инструментов, предотвращение каскадных сбоев
- **Потоковый вывод**: поддержка потоковых ответов LLM
- **Система Skills**: горячая загрузка файлов внешних навыков и знаний

---

## Установка

### Основная установка (минимальные зависимости)

```bash
pip install sibuchen-agents
```

### Установка дополнительных модулей по необходимости

```bash
# 搜索工具（Tavily、SerpApi、DuckDuckGo）
pip install "sibuchen-agents[search]"

# 记忆系统（Qdrant 向量库 + Neo4j 图数据库）
pip install "sibuchen-agents[memory]"

# RAG 检索（transformers、sentence-transformers、PDF 解析）
pip install "sibuchen-agents[rag]"

# 通信协议（MCP、A2A）
pip install "sibuchen-agents[protocols]"

# 即时通讯（NoneBot2 + Telegram/飞书适配器）
pip install "sibuchen-agents[im]"

# 全功能安装
pip install "sibuchen-agents[all]"
```

---

## Быстрый старт

### 1. Настройка переменных окружения

Скопируйте и отредактируйте файл `.env.example`:

```bash
cp .env.example .env
```

Минимальная конфигурация:

```env
LLM_BASE_URL=https://api.openai.com/v1
LLM_API_KEY=your-api-key
LLM_MODEL_ID=gpt-4o
```

### 2. Базовое использование

```python
import asyncio
from sibuchen_agents import SimpleAgent, SibuchenConfig

async def main():
    config = SibuchenConfig()  # 自动读取 .env
    agent = SimpleAgent(config=config)

    response = await agent.run("帮我写一首关于人工智能的诗。")
    print(response)

asyncio.run(main())
```

### 3. ReAct Agent с инструментами

```python
import asyncio
from sibuchen_agents import ReActAgent, SibuchenConfig
from sibuchen_agents.tools.builtin import CalculatorTool, SearchTool

async def main():
    config = SibuchenConfig()
    agent = ReActAgent(config=config)
    agent.add_tool(CalculatorTool())
    agent.add_tool(SearchTool())

    response = await agent.run("今天是哪年？用2026减去这个年份等于多少？")
    print(response)

asyncio.run(main())
```

### 4. Function Call Agent (нативный вызов инструментов OpenAI)

```python
import asyncio
from sibuchen_agents import FunctionCallAgent, SibuchenConfig
from sibuchen_agents.tools.builtin import FileReadTool, TerminalTool

async def main():
    config = SibuchenConfig()
    agent = FunctionCallAgent(config=config)
    agent.add_tool(FileReadTool())
    agent.add_tool(TerminalTool())

    response = await agent.run("列出当前目录的文件，并读取 README.md 的前10行。")
    print(response)

asyncio.run(main())
```

### 5. Потоковый вывод

```python
import asyncio
from sibuchen_agents import SimpleAgent, SibuchenConfig

async def main():
    config = SibuchenConfig()
    agent = SimpleAgent(config=config)

    async for chunk in agent.run_stream("用中文介绍一下量子计算。"):
        print(chunk, end="", flush=True)

asyncio.run(main())
```

---

## Структура проекта

```
src/sibuchen_agents/
├── __init__.py                              # 初始化 пакета
├── agents
│   ├── __init__.py                          # Инициализация модуля Agent
│   ├── factory.py                           # Фабрика агентов и логика создания экземпляров
│   ├── function_call_agent.py               # Агент с вызовом инструментов
│   ├── plan_solve_agent.py                  # Агент с парадигмой Plan-and-Solve
│   ├── react_agent.py                       # Агент с парадигмой ReAct
│   ├── reflection_agent.py                  # Агент с парадигмой Reflection
│   ├── simple_agent.py                      # Простой агент
│   └── tool_aware_agent.py                  # Инструментально-осведомлённый агент
├── context
│   ├── __init__.py                          # Инициализация модуля контекста
│   ├── builder.py                           # Конструктор контекста промпта
│   ├── history.py                           # Управление историей диалога
│   ├── token_counter.py                     # Подсчёт и расчёт токенов
│   └── truncator.py                         # Обрезка и усечение контекста
├── core
│   ├── __init__.py                          # Инициализация основного модуля
│   ├── agent.py                             # Абстрактный базовый класс Agent
│   ├── config.py                            # Управление глобальной конфигурацией
│   ├── exceptions.py                        # Пользовательские исключения
│   ├── lifecycle.py                         # Управление жизненным циклом агента
│   ├── llm_adapters.py                      # Мульти-модельные адаптеры LLM
│   ├── llm_client.py                        # Обёртка LLM-клиента
│   ├── llm_response.py                      # Определение объекта ответа LLM
│   ├── message.py                           # Определение структуры сообщения
│   ├── session_store.py                     # Хранилище сессий
│   └── streaming.py                         # Обработка потокового вывода
├── memory
│   ├── __init__.py                          # Инициализация модуля памяти
│   ├── base.py                              # Абстрактный базовый класс памяти
│   ├── embedding.py                         # Обработка векторных Embedding
│   ├── manager.py                           # Менеджер памяти
│   ├── rag
│   │   ├── __init__.py                      # Инициализация модуля RAG
│   │   ├── document.py                      # Определение объекта документа RAG
│   │   └── pipeline.py                      # Конвейер генерации на основе извлечения RAG
│   ├── storage
│   │   ├── __init__.py                      # Инициализация уровня хранения
│   │   ├── document_store.py                # Реализация хранилища документов
│   │   ├── neo4j_store.py                   # Хранилище графовой базы данных Neo4j
│   │   └── qdrant_store.py                  # Хранилище векторной базы данных Qdrant
│   └── types
│       ├── __init__.py                      # Инициализация типов памяти
│       ├── core_memory.py                   # Структура основной памяти
│       ├── long_term_memory.py              # Реализация долгосрочной памяти
│       ├── multimodal_memory.py             # Реализация мультимодальной памяти
│       └── short_term_memory.py             # Реализация краткосрочной памяти
├── observability
│   ├── __init__.py                          # Инициализация модуля наблюдаемости
│   └── trace_logger.py                      # Логирование цепочки трассировки
├── protocols
│   ├── __init__.py                          # Инициализация модуля протоколов
│   ├── a2a
│   │   ├── __init__.py                      # Инициализация протокола A2A
│   │   └── implementation.py                # Реализация протокола A2A
│   ├── anp
│   │   ├── __init__.py                      # Инициализация протокола ANP
│   │   └── implementation.py                # Реализация протокола ANP
│   ├── base.py                              # Абстрактный базовый класс протокола
│   ├── im
│   │   ├── __init__.py                      # Инициализация протокола IM
│   │   ├── adapters                         # Каталог адаптеров платформ IM
│   │   │   ├── __init__.py                  # Инициализация модуля IM Adapter
│   │   │   ├── feishu_adapter.py            # Адаптер платформы IM Feishu
│   │   │   ├── telegram_adapter.py          # Адаптер платформы IM Telegram
│   │   │   └── *.py                         # Пользовательские адаптеры платформ IM
│   │   ├── plugin.py                        # Механизм плагинов IM
│   │   ├── rate_limiter.py                  # Контроль ограничения частоты сообщений
│   │   ├── server.py                        # Реализация сервера IM
│   │   └── session_manager.py               # Управление сессиями IM
│   └── mcp
│       ├── __init__.py                      # Инициализация протокола MCP
│       ├── client.py                        # Реализация MCP Client
│       ├── server.py                        # Реализация MCP Server
│       └── utils.py                         # Утилиты MCP
├── skills
│   ├── __init__.py                          # Инициализация модуля Skills
│   └── loader.py                            # Динамический загрузчик Skills
├── tools
│   ├── __init__.py                          # Инициализация модуля инструментов
│   ├── base.py                              # Абстрактный базовый класс Tool
│   ├── builtin
│   │   ├── __init__.py                      # Инициализация встроенных инструментов
│   │   ├── calculator_tool.py               # Инструмент-калькулятор
│   │   ├── devlog_tool.py                   # Инструмент журнала разработки
│   │   ├── file_tools.py                    # Набор инструментов для работы с файлами
│   │   ├── mcp_wrapper_tool.py              # Обёртка инструмента MCP
│   │   ├── memory_tool.py                   # Инструмент операций с памятью
│   │   ├── note_tool.py                     # Инструмент управления заметками
│   │   ├── protocol_tools.py                # Инструменты работы с протоколами
│   │   ├── rag_tool.py                      # Инструмент извлечения RAG
│   │   ├── search_tool.py                   # Инструмент поиска
│   │   ├── skill_tool.py                    # Инструмент вызова Skill
│   │   ├── task_tool.py                     # Инструмент управления задачами
│   │   ├── terminal_tool.py                 # Инструмент выполнения терминальных команд
│   │   └── todowrite_tool.py                # Инструмент записи задач Todo
│   ├── circuit_breaker.py                   # Реализация механизма автоматического выключателя
│   ├── errors.py                            # Определение исключений Tool
│   ├── registry.py                          # Реестр инструментов
│   ├── response.py                          # Структура ответа Tool
│   └── tool_filter.py                       # Фильтр прав доступа к инструментам
└── utils
    ├── __init__.py                          # Инициализация модуля утилит
    ├── helpers.py                           # Общие вспомогательные функции
    ├── logging.py                           # Обёртка логирования
    └── serialization.py                     # Утилиты сериализации и десериализации
```

---

## Поддерживаемые парадигмы агентов

| Агент | Применение | Поддержка инструментов |
|---|---|---|
| `SimpleAgent` | Общий диалог, генерация текста | Опционально |
| `ReActAgent` | Задачи с рассуждениями, требующие вызова инструментов | ✅ |
| `FunctionCallAgent` | Стиль Function Calling от OpenAI | ✅ |
| `ReflectionAgent` | Задачи, требующие самокоррекции | Опционально |
| `PlanAndSolveAgent` | Сложные многошаговые задачи планирования | ✅ |
| `ToolAwareSimpleAgent` | Улучшенный диалог с учётом инструментов | ✅ |

---

## Встроенные инструменты

| Инструмент | Функция | Опциональные зависимости |
|---|---|---|
| `CalculatorTool` | Вычисление математических выражений | -- |
| `FileReadTool` / `FileWriteTool` / ... | Чтение и запись файлов, операции с каталогами, поиск кода | -- |
| `TerminalTool` | Выполнение системных команд терминала | -- |
| `SearchTool` | Мульти-поисковой движок (Tavily/SerpApi/DuckDuckGo) | `[search]` |
| `RAGTool` | Генерация на основе извлечения из документов | `[rag]` |
| `MemoryTool` | Хранение и извлечение векторной/графовой памяти | `[memory]` |
| `NoteTool` | Управление постоянными заметками | -- |
| `TaskTool` | Разбиение задач и отслеживание прогресса | -- |
| `TodoWriteTool` | Управление списком задач | -- |
| `DevLogTool` | Ведение журнала разработки | -- |
| `SkillTool` | Загрузка и выполнение внешних файлов Skill | -- |
| `MCPWrapperTool` | Адаптивная обёртка инструментов MCP | `[protocols]` |
| `ProtocolTools` | Инструменты протоколов A2A/ANP | `[protocols]` |

---

## Поддержка нескольких LLM-бэкендов

```python
from sibuchen_agents import SibuchenConfig

# OpenAI
config = SibuchenConfig(
    llm_base_url="https://api.openai.com/v1",
    llm_api_key="sk-...",
    llm_model_id="gpt-4o"
)

# Google Gemini（通过 google-genai SDK）
config = SibuchenConfig(
    llm_api_key="AIza...",
    llm_model_id="gemini-2.0-flash"
)

# DashScope（阿里云）
config = SibuchenConfig(
    llm_base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    llm_api_key="sk-...",
    llm_model_id="qwen-max"
)

# 任意 OpenAI 兼容接口（Ollama、LM Studio 等）
config = SibuchenConfig(
    llm_base_url="http://localhost:11434/v1",
    llm_api_key="ollama",
    llm_model_id="llama3.2"
)
```

---

## Поддержка протоколов

### MCP (Model Context Protocol)

```python
from sibuchen_agents.protocols.mcp import MCPClient

async with MCPClient(server_url="http://localhost:8000/mcp") as client:
    tools = await client.list_tools()
    result = await client.call_tool("tool_name", {"param": "value"})
```

### A2A (Agent-to-Agent)

```python
from sibuchen_agents.protocols.a2a import A2AClient

client = A2AClient(agent_url="http://localhost:9000")
response = await client.send_task("帮我分析这段数据...")
```

---

## Мгновенные сообщения (IM)

На базе [NoneBot2](https://nonebot.dev/) с поддержкой Telegram и Feishu:

```env
# .env
IM_ENABLED=true
IM_AGENT_TYPE=function_call
IM_SESSION_ISOLATION=true
TELEGRAM_BOT_TOKEN=your_token
```

Установка и запуск:

```bash
pip install "sibuchen-agents[im]"
python -m sibuchen_agents.protocols.im.server
```

---

## Наблюдаемость

При каждом запуске агента автоматически генерируется запись трассировки:

```env
TRACE_ENABLED=True
TRACE_DIR=output/memory/traces
```

Файлы трассировки сохраняются в форматах JSON и HTML, полностью фиксируя входные данные, результаты, вызовы инструментов и время выполнения каждого шага.

---

## Справочник по конфигурации

Полный перечень параметров конфигурации см. в [`.env.example`](.env.example). Конфигурация поддерживается через переменные окружения или файл `.env`. Основные группы:

| Группа | Описание |
|---|---|
| `LLM_*` | Конфигурация основного LLM-сервиса |
| `SUMMARY_LLM_*` | Конфигурация LLM для суммаризации |
| `CONTEXT_*` | Конфигурация сжатия контекста |
| `TRACE_*` | Конфигурация наблюдаемости |
| `SESSION_*` | Конфигурация хранения сессий |
| `MEMORY_*` / `QDRANT_*` / `NEO4J_*` | Конфигурация системы памяти |
| `EMBED_*` | Конфигурация модели эмбеддингов |
| `IM_*` / `TELEGRAM_*` / `FEISHU_*` | Конфигурация мгновенных сообщений |
| `SUBAGENT_*` | Конфигурация подчинённых агентов |

---

## Разработка и тестирование

```bash
# Клонирование репозитория
git clone https://github.com/sibuchen/sibuchen-agents.git
cd sibuchen-agents

# Установка зависимостей для разработки
pip install -e ".[dev]"

# Запуск тестов
pytest

# Форматирование кода
black src/
ruff check src/
```

---

## Лицензия

Проект распространяется под лицензией [GNU General Public License v3.0](LICENSE).

---

## Благодарности

При разработке данного фреймворка были использованы идеи и наработки следующих выдающихся проектов с открытым исходным кодом:

- [LangChain](https://github.com/langchain-ai/langchain)
- [smolagents](https://github.com/huggingface/smolagents)
- [NoneBot2](https://github.com/nonebot/nonebot2)
- [Model Context Protocol](https://modelcontextprotocol.io/)
