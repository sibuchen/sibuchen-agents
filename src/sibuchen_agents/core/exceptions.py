# 异常体系

class SibuchenAgentsException(Exception):
    """SibuchenAgents基础异常类"""
    pass


class LLMException(SibuchenAgentsException):
    """LLM相关异常"""
    pass


class AgentException(SibuchenAgentsException):
    """Agent相关异常"""
    pass


class ConfigException(SibuchenAgentsException):
    """配置相关异常"""
    pass


class ToolException(SibuchenAgentsException):
    """工具相关异常"""
    pass
