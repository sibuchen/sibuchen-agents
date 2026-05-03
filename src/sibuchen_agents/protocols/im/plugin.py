"""NoneBot2 消息处理插件（Agent 桥接核心）

架构说明：
    NoneBot2 接收到消息后，调用此插件的 handle_message() 处理器。
    处理器从 IMSessionManager 获取对应用户的 Agent，发起 arun()，
    最后将 Agent 回复发回给用户。

安全控制：
    - 白名单（IM_WHITELIST）：仅允许白名单内的用户 ID，空表示不限制
    - 速率限制（IM_RATE_LIMIT）：每分钟最多 N 条消息/用户

此模块在 IMServer.setup() 中通过 nonebot.load_plugin() 加载。
"""

from __future__ import annotations

import logging
from typing import Optional

logger = logging.getLogger(__name__)

# 以下两个对象由 IMServer.setup() 在加载插件前注入
# 不直接导入以避免循环依赖
_session_manager = None
_rate_limiter = None
_whitelist: set[str] = set()


def _init_plugin(session_manager, rate_limiter, whitelist: set[str]) -> None:
    """由 IMServer 在加载插件后调用，注入运行时依赖

    Args:
        session_manager: IMSessionManager 实例
        rate_limiter: RateLimiter 实例
        whitelist: 允许的用户 ID 集合（空集合表示不限制）
    """
    global _session_manager, _rate_limiter, _whitelist
    _session_manager = session_manager
    _rate_limiter = rate_limiter
    _whitelist = whitelist
    logger.info(
        "✅ [IM/Plugin] 插件已初始化。白名单大小=%d，限流已%s",
        len(whitelist),
        "启用" if rate_limiter else "禁用",
    )


# ------------------------------------------------------------------
# NoneBot2 事件响应器定义
# ------------------------------------------------------------------

def _register_handlers() -> None:
    """注册 NoneBot2 事件响应器（延迟导入，避免在未安装 nonebot2 时报错）"""
    try:
        from nonebot import on_message
        from nonebot.adapters import Bot, Event
        from nonebot.rule import to_me
    except ImportError as e:
        raise ImportError(
            "未安装 nonebot2，请执行：pip install nonebot2[fastapi]"
        ) from e

    # 监听所有平台的消息事件（私聊 + 群聊@机器人）
    # to_me() 规则：私聊直接触发，群聊需 @机器人
    message_handler = on_message(priority=10, block=True)

    @message_handler.handle()
    async def handle_message(bot: Bot, event: Event) -> None:  # type: ignore[reportUnusedFunction]
        """主消息处理器：校验 -> 路由到 Agent -> 回复"""
        # 1. 构建平台无关的会话 ID
        platform = bot.adapter.get_name().lower().replace(" ", "_")
        user_id = event.get_user_id()
        session_id = f"{platform}:{user_id}"

        # 2. 白名单校验
        if _whitelist and user_id not in _whitelist:
            logger.info(
                "🚫 [IM/Plugin] 用户不在白名单，已拒绝。session=%s", session_id
            )
            await bot.send(event, "抱歉，您没有使用权限。如需开通，请联系管理员。")
            return

        # 3. 速率限制
        if _rate_limiter and not _rate_limiter.allow(session_id):
            remaining_s = _rate_limiter._window
            logger.info(
                "⏱️  [IM/Plugin] 触发限流。session=%s", session_id
            )
            await bot.send(
                event,
                f"您的请求过于频繁，请 {remaining_s} 秒后再试。"
            )
            return

        # 4. 获取纯文本消息
        try:
            user_text = event.get_plaintext().strip()
        except Exception:
            user_text = str(event.get_message()).strip()

        if not user_text:
            await bot.send(event, "抱歉，暂不支持非文字消息，请发送文字提问。")
            return

        logger.info(
            "💬 [IM/Plugin] 收到消息 [%s]: %s", session_id, user_text[:80]
        )

        # 5. 获取/创建用户 Agent 并执行
        if _session_manager is None:
            await bot.send(event, "服务初始化中，请稍后再试。")
            return

        agent = _session_manager.get_or_create_agent(session_id)

        try:
            await bot.send(event, "⏳ 正在思考中，请稍候……")
            reply: str = await agent.arun(user_text)
        except Exception as e:
            logger.error(
                "❌ [IM/Plugin] Agent 执行异常 [%s]: %s", session_id, e,
                exc_info=True,
            )
            await bot.send(event, f"抱歉，处理您的请求时发生了错误：{type(e).__name__}")
            return

        # 6. 回复用户（Telegram 单条消息最长 4096 字符，自动分段）
        for chunk in _split_message(reply):
            await bot.send(event, chunk)

        # 7. 自动持久化（如果启用）
        if _session_manager._config.auto_save_enabled:
            _session_manager.save_session(session_id)

        logger.info(
            "✅ [IM/Plugin] 回复已发送 [%s]，长度=%d 字符", session_id, len(reply)
        )


def _split_message(text: str, max_len: int = 4000) -> list[str]:
    """将长文本按最大长度分割为多段

    Args:
        text: 原始文本
        max_len: 单段最大字符数（Telegram 上限 4096，保留余量）

    Returns:
        文本段列表
    """
    if len(text) <= max_len:
        return [text]

    chunks = []
    while text:
        chunks.append(text[:max_len])
        text = text[max_len:]
    return chunks
