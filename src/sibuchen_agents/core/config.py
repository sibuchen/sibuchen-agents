# 配置管理

from pydantic import Field
from pydantic_settings import BaseSettings
from typing import Optional, Dict, Any
from dotenv import load_dotenv

# from pathlib import Path

# 程序启动时加载 .env 文件
load_dotenv(override=True)


class SibuchenConfig(BaseSettings):
    """
    项目配置类 - 自动从 env_file 文件和环境变量加载
    """

    # LLM 配置
    LLM_BASE_URL: str = Field(
        default=...,  # ... 必填项
        description="LLM 服务地址，例如 http://localhost:8888/v1"
    )
    LLM_API_KEY: str = Field(
        default=...,
        description="LLM 的 API Key"
    )
    LLM_MODEL_ID: str = Field(
        default=...,
        description="LLM 模型名称，例如 claude-4.6-opus"
    )
    LLM_TEMPERATURE: float = Field(
        default=0.7,
        ge=0.0,
        le=2.0,
        description="温度参数 [0.0,2.0]"
    )
    LLM_REQUEST_TIMEOUT: Optional[int] = Field(
        default=600,
        gt=0,
        description="请求超时时间（秒），(0,+∞)"
    )
    LLM_MAX_TOKENS: Optional[int] = Field(
        default=None,
        ge=1,
        description="最大生成 token 数，None 表示不限制"
    )

    # 系统 配置
    # BASE_DIR: Path = Field(
    #     default_factory=lambda: Path(__file__).resolve().parent.parent,
    #     description="项目根目录路径（基于当前文件向上两级）"
    # )

    DEBUG: bool = Field(
        default=False,
        description="是否开启调试模式"
    )
    LOG_LEVEL: str = Field(
        default="INFO",
        description="日志级别: DEBUG, INFO, WARNING, ERROR"
    )

    # 历史管理 配置
    MAX_HISTORY_LENGTH: int = Field(
        default=100,
        ge=10,
        le=1000,
        description="最大对话历史长度 [10,1000]"
    )

    # 上下文工程 配置
    CONTEXT_WINDOW: int = Field(
        default=128000,
        gt=0,
        description="上下文窗口大小（tokens）"
    )

    COMPRESSION_THRESHOLD: float = Field(
        default=0.8,
        ge=0.0,
        le=1.0,
        description="压缩阈值（0.8 = 80%时触发压缩）"
    )
    MIN_RETAIN_ROUNDS: int = Field(
        default=10,
        description="压缩时保留的最小完整轮次数"
    )
    ENABLE_SMART_COMPRESSION: bool = Field(
        default=False,
        description="是否启用智能摘要（需要额外LLM调用）"
    )

    # 智能摘要 配置
    SUMMARY_LLM_BASE_URL: str = Field(
        default=LLM_BASE_URL,
        description="摘要专用 LLM 服务地址，例如 http://localhost:8888/v1"
    )
    SUMMARY_LLM_API_KEY: str = Field(
        default=LLM_API_KEY,
        description="摘要专用 LLM 的 API Key"
    )
    SUMMARY_LLM_MODEL_ID: str = Field(
        default=LLM_MODEL_ID,
        description="摘要专用 LLM 模型名称，例如 claude-4.6-sonnet"
    )
    SUMMARY_LLM_TEMPERATURE: float = Field(
        default=0.3,
        ge=0.0,
        le=2.0,
        description="摘要 生成温度（更确定性）"
    )
    SUMMARY_LLM_REQUEST_TIMEOUT: Optional[int] = Field(
        default=600,
        gt=0,
        description="摘要 请求超时时间（秒），(0,+∞)"
    )
    SUMMARY_LLM_MAX_TOKENS: Optional[int] = Field(
        default=800,
        ge=1,
        description="摘要 最大 Token 数"
    )

    # 工具输出截断 配置
    TOOL_OUTPUT_MAX_LINES: int = Field(
        default=2000,
        description="工具输出最大行数"
    )
    TOOL_OUTPUT_MAX_BYTES: int = Field(
        default=51200,
        description="工具输出最大字节数（50KB）"
    )
    TOOL_OUTPUT_DIR: str = Field(
        default="output/tool-output",
        description="完整输出保存目录"
    )
    TOOL_OUTPUT_TRUNCATE_DIRECTION: str = Field(
        default="head",
        description="截断方向：head/tail/head_tail"
    )

    # 可观测性 配置
    TRACE_ENABLED: bool = Field(
        default=True,
        description="是否启用 Trace 记录"
    )
    TRACE_DIR: str = Field(
        default="output/memory/traces",
        description="Trace 文件保存目录"
    )
    TRACE_SANITIZE: bool = Field(
        default=True,
        description="是否脱敏敏感信息"
    )
    TRACE_HTML_INCLUDE_RAW_RESPONSE: bool = Field(
        default=False,
        description="HTML 是否包含原始响应"
    )

    # Skills 知识外化 配置
    SKILLS_ENABLED: bool = Field(
        default=True,
        description="是否启用 Skills 系统"
    )
    SKILLS_DIR: str = Field(
        default="skills",
        description="Skills 目录路径"
    )
    SKILLS_AUTO_REGISTER: bool = Field(
        default=True,
        description="是否自动注册 SkillTool"
    )

    # 熔断器 配置
    CIRCUIT_ENABLED: bool = Field(
        default=True,
        description="是否启用熔断器"
    )
    CIRCUIT_FAILURE_THRESHOLD: int = Field(
        default=3,
        description="连续失败多少次后熔断"
    )
    CIRCUIT_RECOVERY_TIMEOUT: int = Field(
        default=300,
        description="熔断后恢复时间（秒）"
    )

    # 会话持久化 配置
    SESSION_ENABLED: bool = Field(
        default=True,
        description="是否启用会话持久化"
    )
    SESSION_DIR: str = Field(
        default="output/memory/sessions",
        description="会话文件保存目录"
    )
    AUTO_SAVE_ENABLED: bool = Field(
        default=False,
        description="是否启用自动保存"
    )
    AUTO_SAVE_INTERVAL: int = Field(
        default=10,
        description="自动保存间隔（每N条消息）"
    )

    # 子代理机制 配置
    SUBAGENT_ENABLED: bool = Field(
        default=True,
        description="是否启用子代理机制"
    )
    SUBAGENT_MAX_STEPS: int = Field(
        default=15,
        description="子代理默认最大步数"
    )
    SUBAGENT_USE_LIGHT_LLM: bool = Field(
        default=False,
        description="是否使用轻量模型（默认关闭，避免破坏现有行为）"
    )
    SUBAGENT_LIGHT_LLM_BASE_URL: str = Field(
        default=LLM_BASE_URL,
        description="轻量 LLM 服务地址，例如 http://localhost:8888/v1"
    )
    SUBAGENT_LIGHT_LLM_API_KEY: str = Field(
        default=LLM_API_KEY,
        description="轻量 LLM 的 API Key"
    )
    SUBAGENT_LIGHT_LLM_MODEL_ID: str = Field(
        default=LLM_MODEL_ID,
        description="轻量 LLM 模型名称，例如 claude-4.6-haiku"
    )
    SUBAGENT_LIGHT_LLM_TEMPERATURE: float = Field(
        default=0.7,
        ge=0.0,
        le=2.0,
        description="轻量 温度参数 [0.0,2.0]"
    )
    SUBAGENT_LIGHT_LLM_REQUEST_TIMEOUT: Optional[int] = Field(
        default=600,
        gt=0,
        description="轻量 请求超时时间（秒），(0,+∞)"
    )
    SUBAGENT_LIGHT_LLM_MAX_TOKENS: Optional[int] = Field(
        default=None,
        ge=1,
        description="轻量 最大生成 token 数，None 表示不限制"
    )

    # TodoWrite 进度管理 配置
    TODOWRITE_ENABLED: bool = Field(
        default=True,
        description="是否启用 TodoWrite 工具"
    )
    TODOWRITE_PERSISTENCE_DIR: str = Field(
        default="output/memory/todos",
        description="任务列表持久化目录"
    )

    # DevLog 开发日志 配置
    DEVLOG_ENABLED: bool = Field(
        default=True,
        description="是否启用 DevLog 工具"
    )
    DEVLOG_PERSISTENCE_DIR: str = Field(
        default="output/memory/devlogs",
        description="开发日志持久化目录"
    )

    # 异步生命周期 配置
    ASYNC_ENABLED: bool = Field(
        default=True,
        description="是否启用异步执行"
    )
    MAX_CONCURRENT_TOOLS: int = Field(
        default=3,
        description="最大并发工具数"
    )
    HOOK_TIMEOUT_SECONDS: float = Field(
        default=5.0,
        gt=0.0,
        description="生命周期钩子超时时间（秒）"
    )
    LLM_ASYNC_TIMEOUT: int = Field(
        default=120,
        gt=0,
        description="LLM 异步调用超时时间（秒）"
    )
    TOOL_ASYNC_TIMEOUT: int = Field(
        default=30,
        gt=0,
        description="工具异步调用超时时间（秒）"
    )

    # 流式输出 配置
    STREAM_ENABLED: bool = Field(
        default=True,
        description="是否启用流式输出"
    )
    STREAM_BUFFER_SIZE: int = Field(
        default=100,
        description="流式缓冲区大小"
    )
    STREAM_INCLUDE_THINKING: bool = Field(
        default=True,
        description="是否包含思考过程"
    )
    STREAM_INCLUDE_TOOL_CALLS: bool = Field(
        default=True,
        description="是否包含工具调用"
    )

    # 工具 配置
    # ---搜索工具
    TAVILY_API_KEY: Optional[str] = Field(
        default=None,
        description="Tavily 搜索 API Key (https://tavily.com/)"
    )
    SERPAPI_API_KEY: Optional[str] = Field(
        default=None,
        description="SerpApi 搜索 API Key (https://serpapi.com/)"
    )
    PERPLEXITY_API_KEY: Optional[str] = Field(
        default=None,
        description="Perplexity 搜索 API Key 贵！ (https://www.perplexity.ai/api-platform)"
    )
    SEARXNG_URL: Optional[str] = Field(
        default="http://localhost:8888",
        description="SearXNG 搜索服务的URL （社区/自托管） "
    )

    # 嵌入（Embedding）模型 配置
    EMBED_MODEL_TYPE: str = Field(
        default="dashscope",
        description="嵌入模型类型：dashscope / local / tfidf "
    )
    EMBED_MODEL_BASE_URL: Optional[str] = Field(
        default=None,
        description="嵌入模型 Base URL（可选，自定义 endpoint 时使用）"
    )
    EMBED_MODEL_API_KEY: Optional[str] = Field(
        default=None,
        description="嵌入模型 API Key (https://dashscope.aliyun.com/)"
    )
    EMBED_MODEL_ID: str = Field(
        default="",
        description="嵌入模型名称（为空时，使用各类型默认模型）"
    )

    # GitHub API 配置
    GITHUB_PERSONAL_ACCESS_TOKEN: Optional[str] = Field(
        default=None,
        description="GitHub Personal Access Token（用于访问 GitHub API）(https://github.com/settings/tokens)"
    )

    # HuggingFace API 配置
    HF_TOKEN: Optional[str] = Field(
        default=None,
        description="HuggingFace Token（用于访问 gated datasets，如 GAIA）(https://huggingface.co/settings/tokens)"
    )

    # ==================== IM 配置（NoneBot2 多平台即时通讯）====================
    IM_ENABLED: bool = Field(
        default=False,
        description="是否启用 IM Bot Server（NoneBot2）"
    )
    IM_HOST: str = Field(
        default="0.0.0.0",
        description="IM Bot Server 监听地址"
    )
    IM_PORT: int = Field(
        default=8765,
        gt=0,
        lt=65536,
        description="IM Bot Server 监听端口"
    )
    IM_AGENT_TYPE: str = Field(
        default="function_call",
        description="IM 使用的 Agent 类型：react / reflection / plan / simple / function_call / tool_aware"
    )
    IM_SESSION_ISOLATION: bool = Field(
        default=True,
        description="是否为每个用户创建独立的 Agent 实例（True = 每用户独立历史）"
    )
    IM_WHITELIST: str = Field(
        default="",
        description="允许使用 Bot 的用户 ID 白名单，逗号分隔，留空表示不限制"
    )
    IM_RATE_LIMIT: int = Field(
        default=10,
        ge=0,
        description="每分钟每用户最大请求数（0 表示不限流）"
    )

    # Telegram 适配器配置
    TELEGRAM_BOT_TOKEN: Optional[str] = Field(
        default=None,
        description="Telegram Bot Token（来自 @BotFather）"
    )

    # 飞书（Feishu / Lark）适配器配置
    FEISHU_APP_ID: Optional[str] = Field(
        default=None,
        description="飞书应用 App ID"
    )
    FEISHU_APP_SECRET: Optional[str] = Field(
        default=None,
        description="飞书应用 App Secret"
    )
    FEISHU_VERIFICATION_TOKEN: Optional[str] = Field(
        default=None,
        description="飞书 Webhook Verification Token（推荐在生产环境配置）"
    )

    class Config:
        env_file = ".env"  # 指定要读取的环境变量文件
        env_prefix = ""  # 给所有环境变量加前缀（一般不用）
        extra = "ignore"  # env_file 中有多余的变量时如何处理
        case_sensitive = False  # 环境变量是否区分大小写

    def to_dict(self) -> Dict[str, Any]:
        """
        将配置转为字典
        """
        return self.model_dump()


class QdrantConfig(BaseSettings):
    """Qdrant 向量数据库 配置"""
    QDRANT_URL: str = Field(
        default=None,
        description="Qdrant 服务地址（云服务或本地），例如 https://your-cluster.qdrant.tech:6333 或 http://localhost:6333"
    )
    QDRANT_API_KEY: Optional[str] = Field(
        default=None,
        description="Qdrant API Key（云服务必填，本地可为空） API Key (https://cloud.qdrant.io/)"
    )
    QDRANT_COLLECTION_NAME: str = Field(
        default="sibuchen_agents_vectors",
        description="Qdrant 向量集合名称"
    )
    QDRANT_VECTOR_SIZE: int = Field(
        default=384,
        gt=0,
        description="向量维度大小"
    )
    QDRANT_DISTANCE: str = Field(
        default="cosine",
        description="向量距离度量方式：cosine / euclidean / dot"
    )
    QDRANT_TIMEOUT: int = Field(
        default=30,
        gt=0,
        description="Qdrant 请求超时时间（秒）"
    )

    class Config:
        env_file = ".env"  # 指定要读取的环境变量文件
        env_prefix = ""  # 给所有环境变量加前缀（一般不用）
        extra = "ignore"  # env_file 中有多余的变量时如何处理
        case_sensitive = False  # 环境变量是否区分大小写

    def get_qdrant_config(self) -> Dict[str, Any]:
        """
        将配置转为字典
        """
        return self.model_dump(exclude_none=True)


class Neo4jConfig(BaseSettings):
    """Neo4j 图数据库 配置"""
    NEO4J_URI: str = Field(
        default=None,
        description="Neo4j 连接 URI（Aura 云 或 本地 bolt 协议），"
                    "例如 neo4j+s://your-instance.databases.neo4j.io 或 bolt://localhost:7687"
    )
    NEO4J_API_KEY: Optional[str] = Field(
        default=None,
        description="Qdrant API Key（云服务必填，本地可为空） API Key (https://neo4j.com/cloud/aura/)"
    )
    NEO4J_USERNAME: str = Field(
        default="sibuchen",
        description="Neo4j 用户名"
    )
    NEO4J_PASSWORD: str = Field(
        default="sibuchenagnets-neo4j-password",
        description="Neo4j 密码"
    )
    NEO4J_DATABASE: str = Field(
        default="neo4j",
        description="Neo4j 数据库名称"
    )
    NEO4J_MAX_CONNECTION_LIFETIME: int = Field(
        default=3600,
        gt=0,
        description="Neo4j 最大连接生命周期（秒）"
    )
    NEO4J_MAX_CONNECTION_POOL_SIZE: int = Field(
        default=50,
        gt=0,
        description="Neo4j 最大连接池大小"
    )
    NEO4J_CONNECTION_TIMEOUT: int = Field(
        default=60,
        gt=0,
        description="Neo4j 连接超时时间（秒）"
    )

    class Config:
        env_file = ".env"  # 指定要读取的环境变量文件
        env_prefix = ""  # 给所有环境变量加前缀（一般不用）
        extra = "ignore"  # env_file 中有多余的变量时如何处理
        case_sensitive = False  # 环境变量是否区分大小写

    def get_neo4j_config(self) -> Dict[str, Any]:
        """
        将配置转为字典
        """
        return self.model_dump()


# 初始化配置并验证
config = SibuchenConfig()
qdrant_config = QdrantConfig()
neo4j_config = Neo4jConfig()
