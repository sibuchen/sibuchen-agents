"""IM 会话管理器

职责：
- 按 session_id（形如 "telegram:123456"）管理每个用户的 Agent 实例
- 首次访问时通过 agents.factory.create_agent() 创建新 Agent
- 利用 core.SessionStore 将历史持久化到本地 JSON
- 支持会话销毁与列举

设计原则：
- 每用户独立 Agent 实例 + 独立对话历史
- SessionStore 文件名 = "im-{safe_session_id}.json"，以便与主程序会话区分
- 线程安全（asyncio 场景下为单线程，Lock 保留以备混用）
"""

from __future__ import annotations

import logging
import re
from threading import Lock
from typing import Dict, List, Optional

from sibuchen_agents.core.agent import Agent
from sibuchen_agents.core.config import SibuchenConfig
from sibuchen_agents.core.llm_client import SibuchenAgentsLLMClient
from sibuchen_agents.core.session_store import SessionStore

logger = logging.getLogger(__name__)


class IMSessionManager:
    """每用户独立 Agent 会话管理器

    Args:
        config: SibuchenConfig 实例
        agent_type: 要创建的 Agent 类型，默认 "function_call"
        system_prompt: 注入给每个 Agent 的系统提示词（可选）
    """

    # session_id 允许的字符集（防止路径穿越）
    _SAFE_PATTERN = re.compile(r"[^a-zA-Z0-9_\-]")

    def __init__(
        self,
        config: Optional[SibuchenConfig] = None,
        agent_type: str = "function_call",
        system_prompt: Optional[str] = None,
    ) -> None:
        self._config = config or SibuchenConfig()
        self._agent_type = agent_type
        self._system_prompt = system_prompt

        # session_id -> Agent
        self._agents: Dict[str, Agent] = {}
        self._lock = Lock()

        # 持久化存储（复用现有 SessionStore）
        self._session_store = SessionStore(
            session_dir=self._config.session_dir
        ) if self._config.session_enabled else None

        # LLM 客户端（所有会话共享同一个 LLM 配置，各自维护历史）
        self._llm = SibuchenAgentsLLMClient(
            base_url=self._config.llm_base_url,
            api_key=self._config.llm_api_key,
            model=self._config.llm_model_id,
            temperature=self._config.llm_temperature,
            max_tokens=self._config.llm_max_tokens,
            timeout=self._config.llm_request_timeout,
        )

        logger.info(
            "✅ [IM/SessionManager] 初始化完成。"
            "agent_type=%s，session_dir=%s",
            self._agent_type,
            self._config.session_dir,
        )

    # ------------------------------------------------------------------
    # 公开接口
    # ------------------------------------------------------------------

    def get_or_create_agent(self, session_id: str) -> Agent:
        """获取或创建 Agent 实例

        - 若 session_id 已有 Agent，直接返回（热路径，O(1)）
        - 否则创建新 Agent，并尝试从 SessionStore 恢复历史

        Args:
            session_id: 会话唯一标识，形如 "telegram:123456789"

        Returns:
            配置好的 Agent 实例
        """
        with self._lock:
            if session_id in self._agents:
                return self._agents[session_id]

            agent = self._build_agent(session_id)
            self._agents[session_id] = agent
            logger.info("🆕 [IM/SessionManager] 新建会话: %s", session_id)
            return agent

    def destroy_session(self, session_id: str) -> bool:
        """销毁会话（从内存移除，但不删除持久化文件）

        Args:
            session_id: 会话唯一标识

        Returns:
            True 表示成功销毁，False 表示不存在
        """
        with self._lock:
            if session_id in self._agents:
                del self._agents[session_id]
                logger.info("🗑️  [IM/SessionManager] 会话已销毁: %s", session_id)
                return True
        return False

    def save_session(self, session_id: str) -> Optional[str]:
        """手动保存指定会话的历史到 SessionStore

        Args:
            session_id: 会话唯一标识

        Returns:
            保存的文件路径，若未启用持久化或会话不存在则返回 None
        """
        if not self._session_store:
            return None

        with self._lock:
            agent = self._agents.get(session_id)

        if agent is None:
            logger.warning(
                "⚠️  [IM/SessionManager] 会话不存在，无法保存: %s", session_id
            )
            return None

        safe_name = f"im-{self._safe_id(session_id)}"
        try:
            filepath = agent.save_session(safe_name)
            logger.info(
                "💾 [IM/SessionManager] 会话已保存: %s -> %s", session_id, filepath
            )
            return filepath
        except Exception as e:
            logger.error(
                "❌ [IM/SessionManager] 会话保存失败 [%s]: %s", session_id, e
            )
            return None

    def list_sessions(self) -> List[str]:
        """列出当前内存中活跃的 session_id 列表

        Returns:
            活跃会话 ID 列表
        """
        with self._lock:
            return list(self._agents.keys())

    def session_count(self) -> int:
        """返回当前内存中活跃会话数量"""
        with self._lock:
            return len(self._agents)

    # ------------------------------------------------------------------
    # 私有方法
    # ------------------------------------------------------------------

    def _build_agent(self, session_id: str) -> Agent:
        """创建新 Agent，并尝试从 SessionStore 恢复历史

        Args:
            session_id: 会话唯一标识

        Returns:
            初始化好的 Agent 实例
        """
        from sibuchen_agents.agents.factory import create_agent

        agent = create_agent(
            agent_type=self._agent_type,
            name=f"im-agent-{self._safe_id(session_id)}",
            llm=self._llm,
            config=self._config,
            system_prompt=self._system_prompt,
        )

        # 尝试恢复历史
        if self._session_store and self._config.session_enabled:
            self._try_restore(agent, session_id)

        return agent

    def _try_restore(self, agent: Agent, session_id: str) -> None:
        """从 SessionStore 恢复会话历史（静默失败）

        Args:
            agent: 目标 Agent 实例
            session_id: 会话唯一标识
        """
        import os
        from pathlib import Path

        safe_name = f"im-{self._safe_id(session_id)}.json"
        filepath = Path(self._config.session_dir) / safe_name

        if not filepath.exists():
            return  # 新用户，无需恢复

        try:
            agent.load_session(str(filepath), check_consistency=False)
            history_len = len(agent.get_history())
            logger.info(
                "♻️  [IM/SessionManager] 已恢复会话 [%s]，历史消息数: %d",
                session_id,
                history_len,
            )
        except Exception as e:
            logger.warning(
                "⚠️  [IM/SessionManager] 会话恢复失败 [%s]: %s（将从空历史开始）",
                session_id,
                e,
            )

    @classmethod
    def _safe_id(cls, session_id: str) -> str:
        """将 session_id 转为安全的文件名字符串

        Args:
            session_id: 原始会话 ID（如 "telegram:123456"）

        Returns:
            安全字符串（如 "telegram_123456"）
        """
        return cls._SAFE_PATTERN.sub("_", session_id)
