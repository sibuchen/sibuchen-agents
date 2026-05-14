# SibuchenAgents

<div align="center">

**モジュラーで拡張可能な Python AIエージェントフレームワーク**
<!-- 動的バッジ -->
[![PyPI version](https://img.shields.io/pypi/v/sibuchen-agents?label=Version&color=3775A9&logo=pypi&logoColor=3775A9)](https://pypi.org/project/sibuchen-agents/)
[![Python](https://img.shields.io/pypi/pyversions/sibuchen-agents?label=Python&color=3776AB&logo=python&logoColor=3776AB)](https://pypi.org/project/sibuchen-agents/)
<!-- 静的バッジ https://img.shields.io/badge/<左側テキスト>-<右側テキスト>-<色> -->
[![License](https://img.shields.io/badge/License-GPLv3-D6336C.svg?logo=GPLv3&logoColor=BD0000)](https://www.gnu.org/licenses/gpl-3.0)
[![GitHub](https://img.shields.io/badge/GitHub-sibuchen--agents-181717?logo=github&logoColor=181717)](https://github.com/sibuchen/sibuchen-agents)
[![Author](https://img.shields.io/badge/Author-sibuchen-orange?logo=github&logoColor=181717)](https://github.com/sibuchen/)

</div>

<p align="center">
  <a href="./README.md">English</a> | <a href="./README_CN.md">简体中文</a> | <a href="./README_TC.md">繁體中文</a> | <a href="./README_JP.md">日本語</a> | <a href="./README_RU.md">Русский</a>
</p>

SibuchenAgents は開発者向けの Python AIエージェントフレームワークです。多様な推論パラダイム、豊富な組み込みツール、インテリジェントなメモリシステム、複数プロトコルによる通信機能を提供し、本番環境対応の AIエージェントアプリケーションを迅速に構築できます。

---

## ✨ 主な特徴

- **多様な推論パラダイム**：SimpleAgent、ReActAgent、FunctionCallAgent、ReflectionAgent、PlanAndSolveAgent、ToolAwareSimpleAgent
- **複数LLMバックエンド**：OpenAI、Google Gemini、DashScope（Alibaba Cloud）、および任意の OpenAI 互換インターフェース
- **豊富な組み込みツール**：ファイル操作、ターミナル実行、検索エンジン、RAG検索、メモリストレージ、タスク管理、計算機など14種以上のツール
- **インテリジェントメモリシステム**：会話履歴管理、ベクトルストア（Qdrant）、グラフストア（Neo4j）、RAG検索
- **複数プロトコル対応**：MCP（Model Context Protocol）、A2A（Agent-to-Agent）、ANP（Agent Network Protocol）
- **インスタントメッセージング（IM）**：NoneBot2 ベース、Telegram、Feishu（飛書）対応
- **オブザーバビリティ**：完全なトレースチェーン記録と HTML レポート生成
- **コンテキストエンジニアリング**：自動コンテキスト圧縮とインテリジェントな要約
- **サーキットブレーカー**：ツール実行のサーキットブレーカーによりカスケード障害を防止
- **ストリーミング出力**：LLM ストリーミングレスポンスに対応
- **Skills システム**：外部知識スキルファイルのホットロード

---

## 📦 インストール

### コアインストール（最小依存）

```bash
pip install sibuchen-agents
```

### オプションモジュールのオンデマンドインストール

```bash
# 検索ツール（Tavily、SerpApi、DuckDuckGo）
pip install "sibuchen-agents[search]"

# メモリシステム（Qdrant ベクトルDB + Neo4j グラフDB）
pip install "sibuchen-agents[memory]"

# RAG検索（transformers、sentence-transformers、PDF 解析）
pip install "sibuchen-agents[rag]"

# 通信プロトコル（MCP、A2A）
pip install "sibuchen-agents[protocols]"

# インスタントメッセージング（NoneBot2 + Telegram/Feishu アダプター）
pip install "sibuchen-agents[im]"

# 全機能インストール
pip install "sibuchen-agents[all]"
```

---

## ⚡ クイックスタート

### 1. 環境変数の設定

`.env.example` ファイルをコピーして編集してください：

```bash
cp .env.example .env
```

最小構成：

```env
LLM_BASE_URL=https://api.openai.com/v1
LLM_API_KEY=your-api-key
LLM_MODEL_ID=gpt-4o
```

### 2. 基本的な使い方

```python
import asyncio
from sibuchen_agents import SimpleAgent, SibuchenConfig

async def main():
    config = SibuchenConfig()  # 自動的に .env を読み込みます
    agent = SimpleAgent(config=config)

    response = await agent.run("帮我写一首关于人工智能的诗。")
    print(response)

asyncio.run(main())
```

### 3. ツールを使用する ReAct Agent

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

### 4. Function Call Agent（OpenAI ネイティブツール呼び出し）

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

### 5. ストリーミング出力

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

## 🗂️ プロジェクト構成

```
src/sibuchen_agents/
├── __init__.py                              # パッケージ初期化ファイル
├── agents
│   ├── __init__.py                          # Agent モジュール初期化
│   ├── factory.py                           # Agent ファクトリーとインスタンス生成ロジック
│   ├── function_call_agent.py               # ツール呼び出し Agent
│   ├── plan_solve_agent.py                  # Plan-and-Solve パラダイム Agent
│   ├── react_agent.py                       # ReAct パラダイム Agent
│   ├── reflection_agent.py                  # Reflection パラダイム Agent
│   ├── simple_agent.py                      # シンプル Agent
│   └── tool_aware_agent.py                  # ツール認識 Agent
├── context
│   ├── __init__.py                          # コンテキストモジュール初期化
│   ├── builder.py                           # Prompt コンテキストビルダー
│   ├── history.py                           # 会話履歴管理
│   ├── token_counter.py                     # トークン統計と計算
│   └── truncator.py                         # コンテキストのトリミングと切り詰め
├── core
│   ├── __init__.py                          # コアモジュール初期化
│   ├── agent.py                             # Agent 抽象基底クラス定義
│   ├── config.py                            # グローバル設定管理
│   ├── exceptions.py                        # カスタム例外定義
│   ├── lifecycle.py                         # Agent ライフサイクル管理
│   ├── llm_adapters.py                      # LLM マルチモデルアダプター
│   ├── llm_client.py                        # LLM クライアントラッパー
│   ├── llm_response.py                      # LLM レスポンスオブジェクト定義
│   ├── message.py                           # メッセージ構造定義
│   ├── session_store.py                     # セッションストア
│   └── streaming.py                         # ストリーミング出力処理
├── memory
│   ├── __init__.py                          # メモリモジュール初期化
│   ├── base.py                              # メモリ抽象基底クラス
│   ├── embedding.py                         # ベクトル Embedding 処理
│   ├── manager.py                           # メモリマネージャー
│   ├── rag
│   │   ├── __init__.py                      # RAG モジュール初期化
│   │   ├── document.py                      # RAG ドキュメントオブジェクト定義
│   │   └── pipeline.py                      # RAG 検索生成パイプライン
│   ├── storage
│   │   ├── __init__.py                      # ストレージレイヤー初期化
│   │   ├── document_store.py                # ドキュメントストア実装
│   │   ├── neo4j_store.py                   # Neo4j グラフデータベースストア
│   │   └── qdrant_store.py                  # Qdrant ベクトルデータベースストア
│   └── types
│       ├── __init__.py                      # メモリ型初期化
│       ├── core_memory.py                   # コアメモリ構造
│       ├── long_term_memory.py              # 長期メモリ実装
│       ├── multimodal_memory.py             # マルチモーダルメモリ実装
│       └── short_term_memory.py             # 短期メモリ実装
├── observability
│   ├── __init__.py                          # オブザーバビリティモジュール初期化
│   └── trace_logger.py                      # トレースチェーンログ記録
├── protocols
│   ├── __init__.py                          # プロトコルモジュール初期化
│   ├── a2a
│   │   ├── __init__.py                      # A2A プロトコル初期化
│   │   └── implementation.py                # A2A プロトコル実装
│   ├── anp
│   │   ├── __init__.py                      # ANP プロトコル初期化
│   │   └── implementation.py                # ANP プロトコル実装
│   ├── base.py                              # プロトコル抽象基底クラス
│   ├── im
│   │   ├── __init__.py                      # IM プロトコル初期化
│   │   ├── adapters                         # IM プラットフォームアダプターディレクトリ
│   │   │   ├── __init__.py                  # IM Adapter モジュール初期化
│   │   │   ├── feishu_adapter.py            # Feishu（飛書）IM プラットフォームアダプター
│   │   │   ├── telegram_adapter.py          # Telegram IM プラットフォームアダプター
│   │   │   └── *.py                         # カスタム IM プラットフォームアダプター
│   │   ├── plugin.py                        # IM プラグイン機構
│   │   ├── rate_limiter.py                  # メッセージレート制限
│   │   ├── server.py                        # IM サーバー実装
│   │   └── session_manager.py               # IM セッション管理
│   └── mcp
│       ├── __init__.py                      # MCP プロトコル初期化
│       ├── client.py                        # MCP Client 実装
│       ├── server.py                        # MCP Server 実装
│       └── utils.py                         # MCP ユーティリティ関数
├── skills
│   ├── __init__.py                          # Skills モジュール初期化
│   └── loader.py                            # Skills 動的ローダー
├── tools
│   ├── __init__.py                          # Tools モジュール初期化
│   ├── base.py                              # Tool 抽象基底クラス
│   ├── builtin
│   │   ├── __init__.py                      # 組み込みツール初期化
│   │   ├── calculator_tool.py               # 計算機ツール
│   │   ├── devlog_tool.py                   # 開発ログツール
│   │   ├── file_tools.py                    # ファイル操作ツールセット
│   │   ├── mcp_wrapper_tool.py              # MCP Tool ラッパー
│   │   ├── memory_tool.py                   # メモリ操作ツール
│   │   ├── note_tool.py                     # ノート管理ツール
│   │   ├── protocol_tools.py                # プロトコル関連ツール
│   │   ├── rag_tool.py                      # RAG 検索ツール
│   │   ├── search_tool.py                   # 検索ツール
│   │   ├── skill_tool.py                    # Skill 呼び出しツール
│   │   ├── task_tool.py                     # タスク管理ツール
│   │   ├── terminal_tool.py                 # ターミナル実行ツール
│   │   └── todowrite_tool.py                # Todo 書き込みツール
│   ├── circuit_breaker.py                   # サーキットブレーカー機構実装
│   ├── errors.py                            # Tool 例外定義
│   ├── registry.py                          # Tool レジストリ
│   ├── response.py                          # Tool レスポンス構造
│   └── tool_filter.py                       # Tool 権限フィルター
└── utils
    ├── __init__.py                          # ユーティリティモジュール初期化
    ├── helpers.py                           # 汎用ヘルパー関数
    ├── logging.py                           # ロギングラッパー
    └── serialization.py                     # シリアライズとデシリアライズ
```

---

## 🤖 対応 Agent パラダイム

| Agent | 用途 | ツールサポート |
|---|---|---|
| `SimpleAgent` | 汎用対話、テキスト生成 | オプション |
| `ReActAgent` | ツール呼び出しを要する推論タスク | ✅ |
| `FunctionCallAgent` | OpenAI Function Calling スタイル | ✅ |
| `ReflectionAgent` | 自己修正が必要なタスク | オプション |
| `PlanAndSolveAgent` | 複雑なマルチステップ計画タスク | ✅ |
| `ToolAwareSimpleAgent` | ツール認識の強化対話 | ✅ |

---

## 🛠️ 組み込みツール一覧

| ツール | 機能 | オプション依存 |
|---|---|---|
| `CalculatorTool` | 数式計算 | — |
| `FileReadTool` / `FileWriteTool` / ... | ファイル読み書き、ディレクトリ操作、コード検索 | — |
| `TerminalTool` | システムターミナルコマンド実行 | — |
| `SearchTool` | マルチエンジン検索（Tavily/SerpApi/DuckDuckGo） | `[search]` |
| `RAGTool` | ドキュメント検索拡張生成 | `[rag]` |
| `MemoryTool` | ベクトル/グラフメモリストアと検索 | `[memory]` |
| `NoteTool` | 永続ノート管理 | — |
| `TaskTool` | タスク分割と進捗追跡 | — |
| `TodoWriteTool` | TODO管理 | — |
| `DevLogTool` | 開発ログ記録 | — |
| `SkillTool` | 外部 Skill ファイルのロードと実行 | — |
| `MCPWrapperTool` | MCP ツールアダプターラッパー | `[protocols]` |
| `ProtocolTools` | A2A/ANP プロトコルツール | `[protocols]` |

---

## 🔌 複数LLMバックエンドサポート

```python
from sibuchen_agents import SibuchenConfig

# OpenAI
config = SibuchenConfig(
    llm_base_url="https://api.openai.com/v1",
    llm_api_key="sk-...",
    llm_model_id="gpt-4o"
)

# Google Gemini（google-genai SDK 経由）
config = SibuchenConfig(
    llm_api_key="AIza...",
    llm_model_id="gemini-2.0-flash"
)

# DashScope（Alibaba Cloud）
config = SibuchenConfig(
    llm_base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    llm_api_key="sk-...",
    llm_model_id="qwen-max"
)

# 任意の OpenAI 互換インターフェース（Ollama、LM Studio 等）
config = SibuchenConfig(
    llm_base_url="http://localhost:11434/v1",
    llm_api_key="ollama",
    llm_model_id="llama3.2"
)
```

---

## 🔗 プロトコルサポート

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

## 💬 インスタントメッセージング（IM）

[NoneBot2](https://nonebot.dev/) ベースで、Telegram および Feishu（飛書）の接続に対応しています：

```env
# .env
IM_ENABLED=true
IM_AGENT_TYPE=function_call
IM_SESSION_ISOLATION=true
TELEGRAM_BOT_TOKEN=your_token
```

インストールと起動：

```bash
pip install "sibuchen-agents[im]"
python -m sibuchen_agents.protocols.im.server
```

---

## 📊 オブザーバビリティ

Agent の実行ごとにトレースレコードを自動生成します：

```env
TRACE_ENABLED=True
TRACE_DIR=output/memory/traces
```

トレースファイルは JSON および HTML 形式で保存され、各ステップの入力、出力、ツール呼び出し、処理時間を完全に記録します。

---

## ⚙️ 設定リファレンス

全設定項目は [`.env.example`](.env.example) を参照してください。環境変数または `.env` ファイルで設定可能です。主要な設定グループ：

| グループ | 説明 |
|---|---|
| `LLM_*` | メイン LLM サービス設定 |
| `SUMMARY_LLM_*` | 要約専用 LLM 設定 |
| `CONTEXT_*` | コンテキスト圧縮設定 |
| `TRACE_*` | オブザーバビリティ設定 |
| `SESSION_*` | セッション永続化設定 |
| `MEMORY_*` / `QDRANT_*` / `NEO4J_*` | メモリシステム設定 |
| `EMBED_*` | Embedding モデル設定 |
| `IM_*` / `TELEGRAM_*` / `FEISHU_*` | インスタントメッセージング設定 |
| `SUBAGENT_*` | サブエージェント設定 |

---

## 🧪 開発とテスト

```bash
# リポジトリのクローン
git clone https://github.com/sibuchen/sibuchen-agents.git
cd sibuchen-agents

# 開発依存のインストール
pip install -e ".[dev]"

# テストの実行
pytest

# コードフォーマット
black src/
ruff check src/
```

---

## 📄 ライセンス

本プロジェクトは [GNU General Public License v3.0](LICENSE) オープンソースライセンスを採用しています。

---

## 🙏 謝辞

本フレームワークは、以下の優れたオープンソースプロジェクトの設計思想を参考にしています：

- [LangChain](https://github.com/langchain-ai/langchain)
- [smolagents](https://github.com/huggingface/smolagents)
- [NoneBot2](https://github.com/nonebot/nonebot2)
- [Model Context Protocol](https://modelcontextprotocol.io/)
