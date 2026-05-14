# SibuchenAgents

<div align="center">

**模块化、可扩展的 Python AI Agent 框架**
<!-- 动态徽章 -->
[![PyPI version](https://img.shields.io/pypi/v/sibuchen-agents?label=Version&color=3775A9&logo=pypi&logoColor=3775A9)](https://pypi.org/project/sibuchen-agents/)
[![Python](https://img.shields.io/pypi/pyversions/sibuchen-agents?label=Python&color=3776AB&logo=python&logoColor=3776AB)](https://pypi.org/project/sibuchen-agents/)
<!-- 静态徽章 https://img.shields.io/badge/<左侧文字>-<右侧文字>-<颜色> -->
[![License](https://img.shields.io/badge/License-GPLv3-D6336C.svg?logo=GPLv3&logoColor=BD0000)](https://www.gnu.org/licenses/gpl-3.0)
[![GitHub](https://img.shields.io/badge/GitHub-sibuchen--agents-181717?logo=github&logoColor=181717)](https://github.com/sibuchen/sibuchen-agents)
[![Author](https://img.shields.io/badge/Author-sibuchen-orange?logo=github&logoColor=181717)](https://github.com/sibuchen/)

</div>

<p align="center">
  <a href="./README.md">English</a> | <a href="./README_CN.md">简体中文</a> | <a href="./README_TC.md">繁體中文</a> | <a href="./README_JP.md">日本語</a> | <a href="./README_RU.md">Русский</a>
</p>

SibuchenAgents 是一个面向开发者的 Python AI Agent 框架，提供多种推理范式、丰富的内置工具、智能记忆系统与多协议通信能力，帮助你快速构建可用于生产的 AI Agent 应用。

---

## ✨ 核心特性

- **多推理范式**：SimpleAgent、ReActAgent、FunctionCallAgent、ReflectionAgent、PlanAndSolveAgent、ToolAwareSimpleAgent
- **多 LLM 后端**：OpenAI、Google Gemini、DashScope（阿里云）及任意 OpenAI 兼容接口
- **丰富内置工具**：文件操作、终端执行、搜索引擎、RAG 检索、记忆存储、任务管理、计算器等 14+ 工具
- **智能记忆系统**：对话历史管理、向量存储（Qdrant）、图谱存储（Neo4j）、RAG 检索
- **多协议支持**：MCP（Model Context Protocol）、A2A（Agent-to-Agent）、ANP（Agent Network Protocol）
- **即时通讯（IM）**：基于 NoneBot2，支持 Telegram、飞书（Feishu）
- **可观测性**：完整的 Trace 链路记录与 HTML 报告生成
- **上下文工程**：自动上下文压缩与智能摘要
- **熔断机制**：工具执行熔断器，防止级联失败
- **流式输出**：支持 LLM 流式响应
- **Skills 系统**：外部知识技能文件热加载

---

## 📦 安装

### 核心安装（最小依赖）

```bash
pip install sibuchen-agents
```

### 按需安装可选模块

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

## ⚡ 快速开始

### 1. 配置环境变量

复制并编辑 `.env.example` 文件：

```bash
cp .env.example .env
```

最小配置：

```env
LLM_BASE_URL=https://api.openai.com/v1
LLM_API_KEY=your-api-key
LLM_MODEL_ID=gpt-4o
```

### 2. 基础用法

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

### 3. 使用工具的 ReAct Agent

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

### 4. Function Call Agent（OpenAI 原生工具调用）

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

### 5. 流式输出

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

## 🗂️ 项目结构

```
src/sibuchen_agents/
├── __init__.py                              # 包初始化文件
├── agents
│   ├── __init__.py                          # Agent 模块初始化
│   ├── factory.py                           # Agent 工厂与实例创建逻辑
│   ├── function_call_agent.py               # 工具调用 Agent
│   ├── plan_solve_agent.py                  # Plan-and-Solve 范式 Agent
│   ├── react_agent.py                       # ReAct 范式 Agent
│   ├── reflection_agent.py                  # Reflection 范式 Agent
│   ├── simple_agent.py                      # 简单 Agent
│   └── tool_aware_agent.py                  # 工具感知 Agent
├── context
│   ├── __init__.py                          # 上下文模块初始化
│   ├── builder.py                           # Prompt 上下文构建器
│   ├── history.py                           # 对话历史管理
│   ├── token_counter.py                     # Token 统计与计算
│   └── truncator.py                         # 上下文裁剪与截断
├── core
│   ├── __init__.py                          # 核心模块初始化
│   ├── agent.py                             # Agent 抽象基类定义
│   ├── config.py                            # 全局配置管理
│   ├── exceptions.py                        # 自定义异常定义
│   ├── lifecycle.py                         # Agent 生命周期管理
│   ├── llm_adapters.py                      # LLM 多模型适配器
│   ├── llm_client.py                        # LLM 客户端封装
│   ├── llm_response.py                      # LLM 响应对象定义
│   ├── message.py                           # 消息结构定义
│   ├── session_store.py                     # Session 会话存储
│   └── streaming.py                         # 流式输出处理
├── memory
│   ├── __init__.py                          # Memory 模块初始化
│   ├── base.py                              # Memory 抽象基类
│   ├── embedding.py                         # 向量 Embedding 处理
│   ├── manager.py                           # Memory 管理器
│   ├── rag
│   │   ├── __init__.py                      # RAG 模块初始化
│   │   ├── document.py                      # RAG 文档对象定义
│   │   └── pipeline.py                      # RAG 检索生成流水线
│   ├── storage
│   │   ├── __init__.py                      # 存储层初始化
│   │   ├── document_store.py                # 文档存储实现
│   │   ├── neo4j_store.py                   # Neo4j 图数据库存储
│   │   └── qdrant_store.py                  # Qdrant 向量数据库存储
│   └── types
│       ├── __init__.py                      # Memory 类型初始化
│       ├── core_memory.py                   # 核心记忆结构
│       ├── long_term_memory.py              # 长期记忆实现
│       ├── multimodal_memory.py             # 多模态记忆实现
│       └── short_term_memory.py             # 短期记忆实现
├── observability
│   ├── __init__.py                          # 可观测性模块初始化
│   └── trace_logger.py                      # Trace 链路日志记录
├── protocols
│   ├── __init__.py                          # 协议模块初始化
│   ├── a2a
│   │   ├── __init__.py                      # A2A 协议初始化
│   │   └── implementation.py                # A2A 协议实现
│   ├── anp
│   │   ├── __init__.py                      # ANP 协议初始化
│   │   └── implementation.py                # ANP 协议实现
│   ├── base.py                              # 协议抽象基类
│   ├── im
│   │   ├── __init__.py                      # IM 协议初始化
│   │   ├── adapters                         # IM 平台适配器目录
│   │   │   ├── __init__.py                  # IM Adapter 模块初始化
│   │   │   ├── feishu_adapter.py            # 飞书 IM 平台适配器
│   │   │   ├── telegram_adapter.py          # Telegram IM 平台适配器
│   │   │   └── *.py                         # 自定义 IM 平台适配器
│   │   ├── plugin.py                        # IM 插件机制
│   │   ├── rate_limiter.py                  # 消息限流控制
│   │   ├── server.py                        # IM 服务端实现
│   │   └── session_manager.py               # IM 会话管理
│   └── mcp
│       ├── __init__.py                      # MCP 协议初始化
│       ├── client.py                        # MCP Client 实现
│       ├── server.py                        # MCP Server 实现
│       └── utils.py                         # MCP 工具函数
├── skills
│   ├── __init__.py                          # Skills 模块初始化
│   └── loader.py                            # Skills 动态加载器
├── tools
│   ├── __init__.py                          # Tools 模块初始化
│   ├── base.py                              # Tool 抽象基类
│   ├── builtin
│   │   ├── __init__.py                      # 内置工具初始化
│   │   ├── calculator_tool.py               # 计算器工具
│   │   ├── devlog_tool.py                   # 开发日志工具
│   │   ├── file_tools.py                    # 文件操作工具集
│   │   ├── mcp_wrapper_tool.py              # MCP Tool 包装器
│   │   ├── memory_tool.py                   # Memory 操作工具
│   │   ├── note_tool.py                     # 笔记管理工具
│   │   ├── protocol_tools.py                # 协议相关工具
│   │   ├── rag_tool.py                      # RAG 检索工具
│   │   ├── search_tool.py                   # 搜索工具
│   │   ├── skill_tool.py                    # Skill 调用工具
│   │   ├── task_tool.py                     # 任务管理工具
│   │   ├── terminal_tool.py                 # 终端执行工具
│   │   └── todowrite_tool.py                # Todo 写入工具
│   ├── circuit_breaker.py                   # 熔断器机制实现
│   ├── errors.py                            # Tool 异常定义
│   ├── registry.py                          # Tool 注册中心
│   ├── response.py                          # Tool 响应结构
│   └── tool_filter.py                       # Tool 权限过滤器
└── utils
    ├── __init__.py                          # 工具模块初始化
    ├── helpers.py                           # 通用辅助函数
    ├── logging.py                           # 日志封装工具
    └── serialization.py                     # 序列化与反序列化工具
```

---

## 🤖 支持的 Agent 范式

| Agent | 适用场景 | 工具支持 |
|---|---|---|
| `SimpleAgent` | 通用对话、文本生成 | 可选 |
| `ReActAgent` | 需要工具调用的推理任务 | ✅ |
| `FunctionCallAgent` | OpenAI Function Calling 风格 | ✅ |
| `ReflectionAgent` | 需要自我校正的任务 | 可选 |
| `PlanAndSolveAgent` | 复杂多步骤规划任务 | ✅ |
| `ToolAwareSimpleAgent` | 工具感知的增强对话 | ✅ |

---

## 🛠️ 内置工具列表

| 工具 | 功能 | 可选依赖 |
|---|---|---|
| `CalculatorTool` | 数学表达式计算 | — |
| `FileReadTool` / `FileWriteTool` / ... | 文件读写、目录操作、代码搜索 | — |
| `TerminalTool` | 执行系统终端命令 | — |
| `SearchTool` | 多引擎搜索（Tavily/SerpApi/DuckDuckGo） | `[search]` |
| `RAGTool` | 文档检索增强生成 | `[rag]` |
| `MemoryTool` | 向量/图谱记忆存储与检索 | `[memory]` |
| `NoteTool` | 持久化笔记管理 | — |
| `TaskTool` | 任务拆解与进度追踪 | — |
| `TodoWriteTool` | 待办事项管理 | — |
| `DevLogTool` | 开发日志记录 | — |
| `SkillTool` | 外部 Skill 文件加载执行 | — |
| `MCPWrapperTool` | MCP 工具适配包装 | `[protocols]` |
| `ProtocolTools` | A2A/ANP 协议工具 | `[protocols]` |

---

## 🔌 多 LLM 后端支持

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

## 🔗 协议支持

### MCP（Model Context Protocol）

```python
from sibuchen_agents.protocols.mcp import MCPClient

async with MCPClient(server_url="http://localhost:8000/mcp") as client:
    tools = await client.list_tools()
    result = await client.call_tool("tool_name", {"param": "value"})
```

### A2A（Agent-to-Agent）

```python
from sibuchen_agents.protocols.a2a import A2AClient

client = A2AClient(agent_url="http://localhost:9000")
response = await client.send_task("帮我分析这段数据...")
```

---

## 💬 即时通讯（IM）

基于 [NoneBot2](https://nonebot.dev/)，支持 Telegram 和飞书（Feishu）接入：

```env
# .env
IM_ENABLED=true
IM_AGENT_TYPE=function_call
IM_SESSION_ISOLATION=true
TELEGRAM_BOT_TOKEN=your_token
```

安装并启动：

```bash
pip install "sibuchen-agents[im]"
python -m sibuchen_agents.protocols.im.server
```

---

## 📊 可观测性

每次 Agent 运行自动生成 Trace 记录：

```env
TRACE_ENABLED=True
TRACE_DIR=output/memory/traces
```

Trace 文件以 JSON 和 HTML 格式保存，完整记录每步的输入、输出、工具调用与耗时。

---

## ⚙️ 配置参考

完整配置项见 [`.env.example`](.env.example)，支持通过环境变量或 `.env` 文件配置。主要分组：

| 分组 | 说明 |
|---|---|
| `LLM_*` | 主 LLM 服务配置 |
| `SUMMARY_LLM_*` | 摘要专用 LLM 配置 |
| `CONTEXT_*` | 上下文压缩配置 |
| `TRACE_*` | 可观测性配置 |
| `SESSION_*` | 会话持久化配置 |
| `MEMORY_*` / `QDRANT_*` / `NEO4J_*` | 记忆系统配置 |
| `EMBED_*` | 嵌入模型配置 |
| `IM_*` / `TELEGRAM_*` / `FEISHU_*` | 即时通讯配置 |
| `SUBAGENT_*` | 子代理配置 |

---

## 🧪 开发与测试

```bash
# 克隆仓库
git clone https://github.com/sibuchen/sibuchen-agents.git
cd sibuchen-agents

# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest

# 代码格式化
black src/
ruff check src/
```

---

## 📄 许可证

本项目采用 [GNU General Public License v3.0](LICENSE) 开源协议。

---

## 🙏 致谢

本框架参考并借鉴了以下优秀开源项目的设计理念：

- [LangChain](https://github.com/langchain-ai/langchain)
- [smolagents](https://github.com/huggingface/smolagents)
- [NoneBot2](https://github.com/nonebot/nonebot2)
- [Model Context Protocol](https://modelcontextprotocol.io/)
