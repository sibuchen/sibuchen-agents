"""智能体通信协议模块

本模块提供四种主要的智能体通信协议：
- MCP (Model Context Protocol): 模型上下文协议
- A2A (Agent-to-Agent Protocol): 智能体间通信协议
- ANP (Agent Network Protocol): 智能体网络协议
- IM (Instant Messaging Protocol): 即时通讯协议
"""

from .base import Protocol

# MCP 协议 - 导出所有常用类（可选，需要 fastmcp）
try:
    from .mcp import (
        MCPClient,
        MCPServer,
        create_context,
        parse_context,
    )
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False
    # 提供占位符
    class MCPClient:
        def __init__(self, *args, **kwargs):
            raise ImportError("MCP requires fastmcp: pip install fastmcp")
    class MCPServer:
        def __init__(self, *args, **kwargs):
            raise ImportError("MCP requires fastmcp: pip install fastmcp")
    def create_context(*args, **kwargs):
        raise ImportError("MCP requires fastmcp: pip install fastmcp")
    def parse_context(*args, **kwargs):
        raise ImportError("MCP requires fastmcp: pip install fastmcp")

# A2A 协议 - 导出所有常用类
from .a2a import (
    A2AAgent,
    A2AServer,
    A2AClient,
    AgentNetwork,
    AgentRegistry,
    A2AMessage,
    MessageType,
    create_message,
    parse_message,
)

# ANP 协议 - 导出所有常用类
from .anp import (
    ANPDiscovery,
    ANPNetwork,
    ServiceInfo,
    register_service,
    discover_service,
)

# IM 协议 - 基于 NoneBot2 的多平台即时通讯（可选，需要 nonebot2）
try:
    from .im import IMServer, IMSessionManager, start_im_server
    IM_AVAILABLE = True
except ImportError:
    IM_AVAILABLE = False
    # 提供占位符

    class IMServer:  # type: ignore[no-redef]
        def __init__(self, *args, **kwargs):
            raise ImportError(
                "IM 功能需要 nonebot2，请执行：pip install nonebot2[fastapi]"
            )

    class IMSessionManager:  # type: ignore[no-redef]
        def __init__(self, *args, **kwargs):
            raise ImportError(
                "IM 功能需要 nonebot2，请执行：pip install nonebot2[fastapi]"
            )

    def start_im_server(*args, **kwargs):  # type: ignore[no-redef]
        raise ImportError(
            "IM 功能需要 nonebot2，请执行：pip install nonebot2[fastapi]"
        )


__all__ = [
    # 基础协议
    "Protocol",

    # MCP 协议（可选）
    "MCPClient",
    "MCPServer",
    "create_context",
    "parse_context",

    # A2A 协议（可选）
    "A2AAgent",
    "A2AServer",
    "A2AClient",
    "AgentNetwork",
    "AgentRegistry",
    "A2AMessage",
    "MessageType",
    "create_message",
    "parse_message",

    # ANP 协议
    "ANPDiscovery",
    "ANPNetwork",
    "ServiceInfo",
    "register_service",
    "discover_service",

    # IM 协议（可选，需要 nonebot2）
    "IMServer",
    "IMSessionManager",
    "start_im_server",
    "IM_AVAILABLE",
]
