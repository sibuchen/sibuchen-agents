# SibuchenAgents

<div align="center">

**模組化、可擴展的 Python AI Agent 框架**
<!-- 動態徽章 -->
[![PyPI version](https://img.shields.io/pypi/v/sibuchen-agents?label=Version&color=3775A9&logo=pypi&logoColor=3775A9)](https://pypi.org/project/sibuchen-agents/)
[![Python](https://img.shields.io/pypi/pyversions/sibuchen-agents?label=Python&color=3776AB&logo=python&logoColor=3776AB)](https://pypi.org/project/sibuchen-agents/)
<!-- 靜態徽章 https://img.shields.io/badge/<左側文字>-<右側文字>-<顏色> -->
[![License](https://img.shields.io/badge/License-GPLv3-D6336C.svg?logo=GPLv3&logoColor=BD0000)](https://www.gnu.org/licenses/gpl-3.0)
[![GitHub](https://img.shields.io/badge/GitHub-sibuchen--agents-181717?logo=github&logoColor=181717)](https://github.com/sibuchen/sibuchen-agents)
[![Author](https://img.shields.io/badge/Author-sibuchen-orange?logo=github&logoColor=181717)](https://github.com/sibuchen/)

</div>

<p align="center">
  <a href="./README.md">English</a> | <a href="./README_CN.md">简体中文</a> | <a href="./README_TC.md">繁體中文</a> | <a href="./README_JP.md">日本語</a> | <a href="./README_RU.md">Русский</a>
</p>

SibuchenAgents 是一個面向開發者的 Python AI Agent 框架，提供多種推理範式、豐富的內建工具、智慧記憶系統與多協議通訊能力，幫助你快速構建可用於生產環境的 AI Agent 應用。

---

## ✨ 核心特性

- **多推理範式**：SimpleAgent、ReActAgent、FunctionCallAgent、ReflectionAgent、PlanAndSolveAgent、ToolAwareSimpleAgent
- **多 LLM 後端**：OpenAI、Google Gemini、DashScope（阿里雲）及任意 OpenAI 兼容介面
- **豐富內建工具**：檔案操作、終端執行、搜尋引擎、RAG 檢索、記憶儲存、任務管理、計算機等 14+ 工具
- **智慧記憶系統**：對話歷史管理、向量儲存（Qdrant）、圖譜儲存（Neo4j）、RAG 檢索
- **多協議支援**：MCP（Model Context Protocol）、A2A（Agent-to-Agent）、ANP（Agent Network Protocol）
- **即時通訊（IM）**：基於 NoneBot2，支援 Telegram、飛書（Feishu）
- **可觀測性**：完整的 Trace 鏈路記錄與 HTML 報告生成
- **上下文工程**：自動上下文壓縮與智慧摘要
- **熔斷機制**：工具執行熔斷器，防止級聯失敗
- **串流輸出**：支援 LLM 串流回應
- **Skills 系統**：外部知識技能檔案熱載入

---

## 📦 安裝

### 核心安裝（最小依賴）

```bash
pip install sibuchen-agents
```

### 按需安裝可選模組

```bash
# 搜尋工具（Tavily、SerpApi、DuckDuckGo）
pip install "sibuchen-agents[search]"

# 記憶系統（Qdrant 向量庫 + Neo4j 圖資料庫）
pip install "sibuchen-agents[memory]"

# RAG 檢索（transformers、sentence-transformers、PDF 解析）
pip install "sibuchen-agents[rag]"

# 通訊協議（MCP、A2A）
pip install "sibuchen-agents[protocols]"

# 即時通訊（NoneBot2 + Telegram/飛書適配器）
pip install "sibuchen-agents[im]"

# 全功能安裝
pip install "sibuchen-agents[all]"
```

---

## ⚡ 快速開始

### 1. 配置環境變數

複製並編輯 `.env.example` 檔案：

```bash
cp .env.example .env
```

最小配置：

```env
LLM_BASE_URL=https://api.openai.com/v1
LLM_API_KEY=your-api-key
LLM_MODEL_ID=gpt-4o
```

### 2. 基礎用法

```python
import asyncio
from sibuchen_agents import SimpleAgent, SibuchenConfig

async def main():
    config = SibuchenConfig()  # 自動讀取 .env
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

### 4. Function Call Agent（OpenAI 原生工具調用）

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

### 5. 串流輸出

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

## 🗂️ 專案結構

```
src/sibuchen_agents/
├── __init__.py                              # 套件初始化檔案
├── agents
│   ├── __init__.py                          # Agent 模組初始化
│   ├── factory.py                           # Agent 工廠與實例建立邏輯
│   ├── function_call_agent.py               # 工具調用 Agent
│   ├── plan_solve_agent.py                  # Plan-and-Solve 範式 Agent
│   ├── react_agent.py                       # ReAct 範式 Agent
│   ├── reflection_agent.py                  # Reflection 範式 Agent
│   ├── simple_agent.py                      # 簡單 Agent
│   └── tool_aware_agent.py                  # 工具感知 Agent
├── context
│   ├── __init__.py                          # 上下文模組初始化
│   ├── builder.py                           # Prompt 上下文構建器
│   ├── history.py                           # 對話歷史管理
│   ├── token_counter.py                     # Token 統計與計算
│   └── truncator.py                         # 上下文裁剪與截斷
├── core
│   ├── __init__.py                          # 核心模組初始化
│   ├── agent.py                             # Agent 抽象基類定義
│   ├── config.py                            # 全域配置管理
│   ├── exceptions.py                        # 自訂異常定義
│   ├── lifecycle.py                         # Agent 生命週期管理
│   ├── llm_adapters.py                      # LLM 多模型適配器
│   ├── llm_client.py                        # LLM 客戶端封裝
│   ├── llm_response.py                      # LLM 回應物件定義
│   ├── message.py                           # 訊息結構定義
│   ├── session_store.py                     # Session 會話儲存
│   └── streaming.py                         # 串流輸出處理
├── memory
│   ├── __init__.py                          # Memory 模組初始化
│   ├── base.py                              # Memory 抽象基類
│   ├── embedding.py                         # 向量 Embedding 處理
│   ├── manager.py                           # Memory 管理器
│   ├── rag
│   │   ├── __init__.py                      # RAG 模組初始化
│   │   ├── document.py                      # RAG 文件物件定義
│   │   └── pipeline.py                      # RAG 檢索生成流水線
│   ├── storage
│   │   ├── __init__.py                      # 儲存層初始化
│   │   ├── document_store.py                # 文件儲存實作
│   │   ├── neo4j_store.py                   # Neo4j 圖資料庫儲存
│   │   └── qdrant_store.py                  # Qdrant 向量資料庫儲存
│   └── types
│       ├── __init__.py                      # Memory 類型初始化
│       ├── core_memory.py                   # 核心記憶結構
│       ├── long_term_memory.py              # 長期記憶實作
│       ├── multimodal_memory.py             # 多模態記憶實作
│       └── short_term_memory.py             # 短期記憶實作
├── observability
│   ├── __init__.py                          # 可觀測性模組初始化
│   └── trace_logger.py                      # Trace 鏈路日誌記錄
├── protocols
│   ├── __init__.py                          # 協議模組初始化
│   ├── a2a
│   │   ├── __init__.py                      # A2A 協議初始化
│   │   └── implementation.py                # A2A 協議實作
│   ├── anp
│   │   ├── __init__.py                      # ANP 協議初始化
│   │   └── implementation.py                # ANP 協議實作
│   ├── base.py                              # 協議抽象基類
│   ├── im
│   │   ├── __init__.py                      # IM 協議初始化
│   │   ├── adapters                         # IM 平台適配器目錄
│   │   │   ├── __init__.py                  # IM Adapter 模組初始化
│   │   │   ├── feishu_adapter.py            # 飛書 IM 平台適配器
│   │   │   ├── telegram_adapter.py          # Telegram IM 平台適配器
│   │   │   └── *.py                         # 自訂 IM 平台適配器
│   │   ├── plugin.py                        # IM 插件機制
│   │   ├── rate_limiter.py                  # 訊息限流控制
│   │   ├── server.py                        # IM 伺服器實作
│   │   └── session_manager.py               # IM 會話管理
│   └── mcp
│       ├── __init__.py                      # MCP 協議初始化
│       ├── client.py                        # MCP Client 實作
│       ├── server.py                        # MCP Server 實作
│       └── utils.py                         # MCP 工具函式
├── skills
│   ├── __init__.py                          # Skills 模組初始化
│   └── loader.py                            # Skills 動態載入器
├── tools
│   ├── __init__.py                          # Tools 模組初始化
│   ├── base.py                              # Tool 抽象基類
│   ├── builtin
│   │   ├── __init__.py                      # 內建工具初始化
│   │   ├── calculator_tool.py               # 計算機工具
│   │   ├── devlog_tool.py                   # 開發日誌工具
│   │   ├── file_tools.py                    # 檔案操作工具集
│   │   ├── mcp_wrapper_tool.py              # MCP Tool 包裝器
│   │   ├── memory_tool.py                   # Memory 操作工具
│   │   ├── note_tool.py                     # 筆記管理工具
│   │   ├── protocol_tools.py                # 協議相關工具
│   │   ├── rag_tool.py                      # RAG 檢索工具
│   │   ├── search_tool.py                   # 搜尋工具
│   │   ├── skill_tool.py                    # Skill 調用工具
│   │   ├── task_tool.py                     # 任務管理工具
│   │   ├── terminal_tool.py                 # 終端執行工具
│   │   └── todowrite_tool.py                # Todo 寫入工具
│   ├── circuit_breaker.py                   # 熔斷器機制實作
│   ├── errors.py                            # Tool 異常定義
│   ├── registry.py                          # Tool 註冊中心
│   ├── response.py                          # Tool 回應結構
│   └── tool_filter.py                       # Tool 權限過濾器
└── utils
    ├── __init__.py                          # 工具模組初始化
    ├── helpers.py                           # 通用輔助函式
    ├── logging.py                           # 日誌封裝工具
    └── serialization.py                     # 序列化與反序列化工具
```

---

## 🤖 支援的 Agent 範式

| Agent | 適用場景 | 工具支援 |
|---|---|---|
| `SimpleAgent` | 通用對話、文字生成 | 可選 |
| `ReActAgent` | 需要工具調用的推理任務 | ✅ |
| `FunctionCallAgent` | OpenAI Function Calling 風格 | ✅ |
| `ReflectionAgent` | 需要自我校正的任務 | 可選 |
| `PlanAndSolveAgent` | 複雜多步驟規劃任務 | ✅ |
| `ToolAwareSimpleAgent` | 工具感知的增強對話 | ✅ |

---

## 🛠️ 內建工具列表

| 工具 | 功能 | 可選依賴 |
|---|---|---|
| `CalculatorTool` | 數學表達式計算 | — |
| `FileReadTool` / `FileWriteTool` / ... | 檔案讀寫、目錄操作、程式碼搜尋 | — |
| `TerminalTool` | 執行系統終端命令 | — |
| `SearchTool` | 多引擎搜尋（Tavily/SerpApi/DuckDuckGo） | `[search]` |
| `RAGTool` | 文件檢索增強生成 | `[rag]` |
| `MemoryTool` | 向量/圖譜記憶儲存與檢索 | `[memory]` |
| `NoteTool` | 持久化筆記管理 | — |
| `TaskTool` | 任務拆解與進度追蹤 | — |
| `TodoWriteTool` | 待辦事項管理 | — |
| `DevLogTool` | 開發日誌記錄 | — |
| `SkillTool` | 外部 Skill 檔案載入執行 | — |
| `MCPWrapperTool` | MCP 工具適配包裝 | `[protocols]` |
| `ProtocolTools` | A2A/ANP 協議工具 | `[protocols]` |

---

## 🔌 多 LLM 後端支援

```python
from sibuchen_agents import SibuchenConfig

# OpenAI
config = SibuchenConfig(
    llm_base_url="https://api.openai.com/v1",
    llm_api_key="sk-...",
    llm_model_id="gpt-4o"
)

# Google Gemini（通過 google-genai SDK）
config = SibuchenConfig(
    llm_api_key="AIza...",
    llm_model_id="gemini-2.0-flash"
)

# DashScope（阿里雲）
config = SibuchenConfig(
    llm_base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    llm_api_key="sk-...",
    llm_model_id="qwen-max"
)

# 任意 OpenAI 兼容介面（Ollama、LM Studio 等）
config = SibuchenConfig(
    llm_base_url="http://localhost:11434/v1",
    llm_api_key="ollama",
    llm_model_id="llama3.2"
)
```

---

## 🔗 協議支援

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

## 💬 即時通訊（IM）

基於 [NoneBot2](https://nonebot.dev/)，支援 Telegram 和飛書（Feishu）接入：

```env
# .env
IM_ENABLED=true
IM_AGENT_TYPE=function_call
IM_SESSION_ISOLATION=true
TELEGRAM_BOT_TOKEN=your_token
```

安裝並啟動：

```bash
pip install "sibuchen-agents[im]"
python -m sibuchen_agents.protocols.im.server
```

---

## 📊 可觀測性

每次 Agent 執行自動生成 Trace 記錄：

```env
TRACE_ENABLED=True
TRACE_DIR=output/memory/traces
```

Trace 檔案以 JSON 和 HTML 格式儲存，完整記錄每步的輸入、輸出、工具調用與耗時。

---

## ⚙️ 配置參考

完整配置項見 [`.env.example`](.env.example)，支援透過環境變數或 `.env` 檔案配置。主要分組：

| 分組 | 說明 |
|---|---|
| `LLM_*` | 主 LLM 服務配置 |
| `SUMMARY_LLM_*` | 摘要專用 LLM 配置 |
| `CONTEXT_*` | 上下文壓縮配置 |
| `TRACE_*` | 可觀測性配置 |
| `SESSION_*` | 會話持久化配置 |
| `MEMORY_*` / `QDRANT_*` / `NEO4J_*` | 記憶系統配置 |
| `EMBED_*` | 嵌入模型配置 |
| `IM_*` / `TELEGRAM_*` / `FEISHU_*` | 即時通訊配置 |
| `SUBAGENT_*` | 子代理配置 |

---

## 🧪 開發與測試

```bash
# 複製倉庫
git clone https://github.com/sibuchen/sibuchen-agents.git
cd sibuchen-agents

# 安裝開發依賴
pip install -e ".[dev]"

# 執行測試
pytest

# 程式碼格式化
black src/
ruff check src/
```

---

## 📄 授權條款

本專案採用 [GNU General Public License v3.0](LICENSE) 開源協議。

---

## 🙏 致謝

本框架參考並借鑑了以下優秀開源專案的設計理念：

- [LangChain](https://github.com/langchain-ai/langchain)
- [smolagents](https://github.com/huggingface/smolagents)
- [NoneBot2](https://github.com/nonebot/nonebot2)
- [Model Context Protocol](https://modelcontextprotocol.io/)
