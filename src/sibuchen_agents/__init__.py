"""
SibuchenAgents - 模块化、可扩展的 Python AI Agent 框架

公共 API 导出，用户只需：
    from sibuchen_agents import SimpleAgent, SibuchenConfig, SibuchenAgentsLLMClient
"""

from sibuchen_agents.core.agent import Agent
from sibuchen_agents.core.llm_client import SibuchenAgentsLLMClient
from sibuchen_agents.core.message import SibuchenMessage
from sibuchen_agents.core.config import SibuchenConfig
from sibuchen_agents.core.exceptions import SibuchenAgentsException
from sibuchen_agents.core.llm_response import LLMResponse, StreamStats

from sibuchen_agents.agents.simple_agent import SimpleAgent
from sibuchen_agents.agents.react_agent import ReActAgent
from sibuchen_agents.agents.plan_solve_agent import PlanAndSolveAgent
from sibuchen_agents.agents.reflection_agent import ReflectionAgent
from sibuchen_agents.agents.function_call_agent import FunctionCallAgent
from sibuchen_agents.agents.tool_aware_agent import ToolAwareSimpleAgent
from sibuchen_agents.agents.factory import create_agent, default_subagent_factory

from sibuchen_agents.tools.registry import ToolRegistry
from sibuchen_agents.tools.base import Tool
from sibuchen_agents.tools.response import ToolResponse, ToolStatus

__version__ = "0.1.0"
__author__ = "sibuchen"
__email__ = ""
__description__ = "模块化、可扩展的 Python AI Agent 框架"

__all__ = [
    # 核心组件
    "Agent",
    "SibuchenAgentsLLMClient",
    "SibuchenMessage",
    "SibuchenConfig",
    "SibuchenAgentsException",
    "LLMResponse",
    "StreamStats",

    # Agent 范式
    "SimpleAgent",
    "ReActAgent",
    "PlanAndSolveAgent",
    "ReflectionAgent",
    "FunctionCallAgent",
    "ToolAwareSimpleAgent",
    "create_agent",
    "default_subagent_factory",

    # 工具系统
    "ToolRegistry",
    "Tool",
    "ToolResponse",
    "ToolStatus",

    # 版本信息
    "__version__",
]
