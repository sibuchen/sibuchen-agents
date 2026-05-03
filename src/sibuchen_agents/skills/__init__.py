"""Skills 知识外化系统

Skills 是"知识外化"的核心实现，让模型按需加载领域知识，而不需要 fine-tuning。

特性：
- 渐进式披露：启动时仅加载元数据，按需加载完整内容
- 缓存友好：作为 tool_result 注入，不修改 system_prompt
- 人类可编辑：SKILL.md 文件，支持版本控制
- Token 节省：预期节省 85% Token（20 个 skills 场景）

"""

from .loader import SkillLoader, Skill

__all__ = [
    "SkillLoader",
    "Skill",
]
