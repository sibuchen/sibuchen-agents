# SibuchenAgents

<div align="center">

**Modular, Extensible Python AI Agent Framework**
<!-- Dynamic badges -->
[![PyPI version](https://img.shields.io/pypi/v/sibuchen-agents?label=Version&color=3775A9&logo=pypi&logoColor=3775A9)](https://pypi.org/project/sibuchen-agents/)
[![Python](https://img.shields.io/pypi/pyversions/sibuchen-agents?label=Python&color=3776AB&logo=python&logoColor=3776AB)](https://pypi.org/project/sibuchen-agents/)
<!-- Static badges https://img.shields.io/badge/<left>-<right>-<color> -->
[![License](https://img.shields.io/badge/License-GPLv3-D6336C.svg?logo=GPLv3&logoColor=BD0000)](https://www.gnu.org/licenses/gpl-3.0)
[![GitHub](https://img.shields.io/badge/GitHub-sibuchen--agents-181717?logo=github&logoColor=181717)](https://github.com/sibuchen/sibuchen-agents)
[![Author](https://img.shields.io/badge/Author-sibuchen-orange?logo=github&logoColor=181717)](https://github.com/sibuchen/)

</div>

<p align="center">
  <a href="./README.md">English</a> | <a href="./README_CN.md">简体中文</a> | <a href="./README_TC.md">繁體中文</a> | <a href="./README_JP.md">日本語</a> | <a href="./README_RU.md">Русский</a>
</p>

SibuchenAgents is a Python AI Agent framework for developers. It offers multiple reasoning paradigms, a rich set of built-in tools, an intelligent memory system, and multi-protocol communication capabilities to help you rapidly build production-ready AI Agent applications.

---

## Core Features

- **Multiple Reasoning Paradigms**: SimpleAgent, ReActAgent, FunctionCallAgent, ReflectionAgent, PlanAndSolveAgent, ToolAwareSimpleAgent
- **Multiple LLM Backends**: OpenAI, Google Gemini, DashScope (Alibaba Cloud), and any OpenAI-compatible endpoint
- **Rich Built-in Tools**: File operations, terminal execution, search engines, RAG retrieval, memory storage, task management, calculator, and 14+ more tools
- **Intelligent Memory System**: Conversation history management, vector storage (Qdrant), graph storage (Neo4j), RAG retrieval
- **Multi-Protocol Support**: MCP (Model Context Protocol), A2A (Agent-to-Agent), ANP (Agent Network Protocol)
- **Instant Messaging (IM)**: Built on NoneBot2, with support for Telegram and Feishu (Lark)
- **Observability**: Full trace logging with HTML report generation
- **Context Engineering**: Automatic context compression and intelligent summarization
- **Circuit Breaker**: Tool execution circuit breaker to prevent cascading failures
- **Streaming Output**: Supports LLM streaming responses
- **Skills System**: Hot-loading of external knowledge skill files

---

## Installation

### Core Installation (Minimal Dependencies)

```bash
pip install sibuchen-agents
```

### Install Optional Modules as Needed

```bash
# Search tools (Tavily, SerpApi, DuckDuckGo)
pip install "sibuchen-agents[search]"

# Memory system (Qdrant vector store + Neo4j graph database)
pip install "sibuchen-agents[memory]"

# RAG retrieval (transformers, sentence-transformers, PDF parsing)
pip install "sibuchen-agents[rag]"

# Communication protocols (MCP, A2A)
pip install "sibuchen-agents[protocols]"

# Instant messaging (NoneBot2 + Telegram/Feishu adapters)
pip install "sibuchen-agents[im]"

# Full installation
pip install "sibuchen-agents[all]"
```

---

## Quick Start

### 1. Configure Environment Variables

Copy and edit the `.env.example` file:

```bash
cp .env.example .env
```

Minimal configuration:

```env
LLM_BASE_URL=https://api.openai.com/v1
LLM_API_KEY=your-api-key
LLM_MODEL_ID=gpt-4o
```

### 2. Basic Usage

```python
import asyncio
from sibuchen_agents import SimpleAgent, SibuchenConfig

async def main():
    config = SibuchenConfig()  # Automatically reads .env
    agent = SimpleAgent(config=config)

    response = await agent.run("帮我写一首关于人工智能的诗。")
    print(response)

asyncio.run(main())
```

### 3. ReAct Agent with Tools

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

### 4. Function Call Agent (Native OpenAI Tool Calling)

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

### 5. Streaming Output

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

## Project Structure

```
src/sibuchen_agents/
├── __init__.py                              # Package initialization
├── agents
│   ├── __init__.py                          # Agent module initialization
│   ├── factory.py                           # Agent factory and instance creation logic
│   ├── function_call_agent.py               # Function Call Agent
│   ├── plan_solve_agent.py                  # Plan-and-Solve paradigm Agent
│   ├── react_agent.py                       # ReAct paradigm Agent
│   ├── reflection_agent.py                  # Reflection paradigm Agent
│   ├── simple_agent.py                      # Simple Agent
│   └── tool_aware_agent.py                  # Tool-Aware Agent
├── context
│   ├── __init__.py                          # Context module initialization
│   ├── builder.py                           # Prompt context builder
│   ├── history.py                           # Conversation history management
│   ├── token_counter.py                     # Token counting and calculation
│   └── truncator.py                         # Context trimming and truncation
├── core
│   ├── __init__.py                          # Core module initialization
│   ├── agent.py                             # Agent abstract base class
│   ├── config.py                            # Global configuration management
│   ├── exceptions.py                        # Custom exception definitions
│   ├── lifecycle.py                         # Agent lifecycle management
│   ├── llm_adapters.py                      # LLM multi-model adapters
│   ├── llm_client.py                        # LLM client wrapper
│   ├── llm_response.py                      # LLM response object definitions
│   ├── message.py                           # Message structure definitions
│   ├── session_store.py                     # Session storage
│   └── streaming.py                         # Streaming output handling
├── memory
│   ├── __init__.py                          # Memory module initialization
│   ├── base.py                              # Memory abstract base class
│   ├── embedding.py                         # Vector embedding processing
│   ├── manager.py                           # Memory manager
│   ├── rag
│   │   ├── __init__.py                      # RAG module initialization
│   │   ├── document.py                      # RAG document object definitions
│   │   └── pipeline.py                      # RAG retrieval-augmented generation pipeline
│   ├── storage
│   │   ├── __init__.py                      # Storage layer initialization
│   │   ├── document_store.py                # Document store implementation
│   │   ├── neo4j_store.py                   # Neo4j graph database storage
│   │   └── qdrant_store.py                  # Qdrant vector database storage
│   └── types
│       ├── __init__.py                      # Memory types initialization
│       ├── core_memory.py                   # Core memory structure
│       ├── long_term_memory.py              # Long-term memory implementation
│       ├── multimodal_memory.py             # Multimodal memory implementation
│       └── short_term_memory.py             # Short-term memory implementation
├── observability
│   ├── __init__.py                          # Observability module initialization
│   └── trace_logger.py                      # Trace logging
├── protocols
│   ├── __init__.py                          # Protocols module initialization
│   ├── a2a
│   │   ├── __init__.py                      # A2A protocol initialization
│   │   └── implementation.py                # A2A protocol implementation
│   ├── anp
│   │   ├── __init__.py                      # ANP protocol initialization
│   │   └── implementation.py                # ANP protocol implementation
│   ├── base.py                              # Protocol abstract base class
│   ├── im
│   │   ├── __init__.py                      # IM protocol initialization
│   │   ├── adapters                         # IM platform adapter directory
│   │   │   ├── __init__.py                  # IM adapter module initialization
│   │   │   ├── feishu_adapter.py            # Feishu IM platform adapter
│   │   │   ├── telegram_adapter.py          # Telegram IM platform adapter
│   │   │   └── *.py                         # Custom IM platform adapters
│   │   ├── plugin.py                        # IM plugin mechanism
│   │   ├── rate_limiter.py                  # Message rate limiting
│   │   ├── server.py                        # IM server implementation
│   │   └── session_manager.py               # IM session management
│   └── mcp
│       ├── __init__.py                      # MCP protocol initialization
│       ├── client.py                        # MCP client implementation
│       ├── server.py                        # MCP server implementation
│       └── utils.py                         # MCP utility functions
├── skills
│   ├── __init__.py                          # Skills module initialization
│   └── loader.py                            # Skills dynamic loader
├── tools
│   ├── __init__.py                          # Tools module initialization
│   ├── base.py                              # Tool abstract base class
│   ├── builtin
│   │   ├── __init__.py                      # Built-in tools initialization
│   │   ├── calculator_tool.py               # Calculator tool
│   │   ├── devlog_tool.py                   # Development log tool
│   │   ├── file_tools.py                    # File operations toolset
│   │   ├── mcp_wrapper_tool.py              # MCP tool wrapper
│   │   ├── memory_tool.py                   # Memory operations tool
│   │   ├── note_tool.py                     # Note management tool
│   │   ├── protocol_tools.py                # Protocol-related tools
│   │   ├── rag_tool.py                      # RAG retrieval tool
│   │   ├── search_tool.py                   # Search tool
│   │   ├── skill_tool.py                    # Skill invocation tool
│   │   ├── task_tool.py                     # Task management tool
│   │   ├── terminal_tool.py                 # Terminal execution tool
│   │   └── todowrite_tool.py                # Todo write tool
│   ├── circuit_breaker.py                   # Circuit breaker mechanism
│   ├── errors.py                            # Tool exception definitions
│   ├── registry.py                          # Tool registry
│   ├── response.py                          # Tool response structure
│   └── tool_filter.py                       # Tool permission filter
└── utils
    ├── __init__.py                          # Utils module initialization
    ├── helpers.py                           # Common helper functions
    ├── logging.py                           # Logging wrapper
    └── serialization.py                     # Serialization and deserialization utilities
```

---

## Supported Agent Paradigms

| Agent | Use Case | Tool Support |
|---|---|---|
| `SimpleAgent` | General conversation, text generation | Optional |
| `ReActAgent` | Reasoning tasks that require tool invocation | Yes |
| `FunctionCallAgent` | OpenAI Function Calling style | Yes |
| `ReflectionAgent` | Tasks that require self-correction | Optional |
| `PlanAndSolveAgent` | Complex multi-step planning tasks | Yes |
| `ToolAwareSimpleAgent` | Tool-aware enhanced conversation | Yes |

---

## Built-in Tool List

| Tool | Description | Optional Dependencies |
|---|---|---|
| `CalculatorTool` | Mathematical expression evaluation | -- |
| `FileReadTool` / `FileWriteTool` / ... | File read/write, directory operations, code search | -- |
| `TerminalTool` | Execute system terminal commands | -- |
| `SearchTool` | Multi-engine search (Tavily/SerpApi/DuckDuckGo) | `[search]` |
| `RAGTool` | Retrieval-augmented generation | `[rag]` |
| `MemoryTool` | Vector/graph memory storage and retrieval | `[memory]` |
| `NoteTool` | Persistent note management | -- |
| `TaskTool` | Task decomposition and progress tracking | -- |
| `TodoWriteTool` | Todo list management | -- |
| `DevLogTool` | Development log recording | -- |
| `SkillTool` | External skill file loading and execution | -- |
| `MCPWrapperTool` | MCP tool adapter wrapper | `[protocols]` |
| `ProtocolTools` | A2A/ANP protocol tools | `[protocols]` |

---

## Multi-LLM Backend Support

```python
from sibuchen_agents import SibuchenConfig

# OpenAI
config = SibuchenConfig(
    llm_base_url="https://api.openai.com/v1",
    llm_api_key="sk-...",
    llm_model_id="gpt-4o"
)

# Google Gemini (via google-genai SDK)
config = SibuchenConfig(
    llm_api_key="AIza...",
    llm_model_id="gemini-2.0-flash"
)

# DashScope (Alibaba Cloud)
config = SibuchenConfig(
    llm_base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    llm_api_key="sk-...",
    llm_model_id="qwen-max"
)

# Any OpenAI-compatible endpoint (Ollama, LM Studio, etc.)
config = SibuchenConfig(
    llm_base_url="http://localhost:11434/v1",
    llm_api_key="ollama",
    llm_model_id="llama3.2"
)
```

---

## Protocol Support

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

## Instant Messaging (IM)

Built on [NoneBot2](https://nonebot.dev/), with support for Telegram and Feishu (Lark) integration:

```env
# .env
IM_ENABLED=true
IM_AGENT_TYPE=function_call
IM_SESSION_ISOLATION=true
TELEGRAM_BOT_TOKEN=your_token
```

Install and start:

```bash
pip install "sibuchen-agents[im]"
python -m sibuchen_agents.protocols.im.server
```

---

## Observability

Each agent run automatically generates trace records:

```env
TRACE_ENABLED=True
TRACE_DIR=output/memory/traces
```

Trace files are saved in JSON and HTML formats, capturing the input, output, tool calls, and latency for every step.

---

## Configuration Reference

See [`.env.example`](.env.example) for the full list of configuration options. Configuration is supported via environment variables or a `.env` file. Main groups:

| Group | Description |
|---|---|
| `LLM_*` | Primary LLM service configuration |
| `SUMMARY_LLM_*` | Dedicated summarization LLM configuration |
| `CONTEXT_*` | Context compression settings |
| `TRACE_*` | Observability settings |
| `SESSION_*` | Session persistence settings |
| `MEMORY_*` / `QDRANT_*` / `NEO4J_*` | Memory system configuration |
| `EMBED_*` | Embedding model configuration |
| `IM_*` / `TELEGRAM_*` / `FEISHU_*` | Instant messaging configuration |
| `SUBAGENT_*` | Sub-agent configuration |

---

## Development and Testing

```bash
# Clone the repository
git clone https://github.com/sibuchen/sibuchen-agents.git
cd sibuchen-agents

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Code formatting
black src/
ruff check src/
```

---

## License

This project is licensed under the [GNU General Public License v3.0](LICENSE).

---

## Acknowledgements

This framework draws inspiration from the design philosophies of the following outstanding open-source projects:

- [LangChain](https://github.com/langchain-ai/langchain)
- [smolagents](https://github.com/huggingface/smolagents)
- [NoneBot2](https://github.com/nonebot/nonebot2)
- [Model Context Protocol](https://modelcontextprotocol.io/)
