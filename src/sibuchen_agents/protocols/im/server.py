"""IM Server - NoneBot2 服务封装

职责：
- 读取 .env 中的 IM_* 配置
- 初始化 NoneBot2（init、注册适配器、加载插件）
- 启动 uvicorn ASGI 服务器（阻塞）

典型用法（通过 im_server.py 入口）：
    server = IMServer()
    server.setup()
    server.start()  # 阻塞

支持的平台：
    - Telegram（TELEGRAM_BOT_TOKEN）
    - 飞书 Feishu（FEISHU_APP_ID + FEISHU_APP_SECRET）
"""

from __future__ import annotations

import logging
import os
from typing import Optional

logger = logging.getLogger(__name__)


class IMServer:
    """NoneBot2 IM Bot Server 封装类

    Args:
        config: SibuchenConfig 实例（为 None 时从环境变量加载）
    """

    def __init__(self, config=None) -> None:
        if config is None:
            from sibuchen_agents.core.config import SibuchenConfig
            config = SibuchenConfig()
        self._config = config
        self._nb_app = None  # ASGI app（setup() 后赋值）

    # ------------------------------------------------------------------
    # 公开方法
    # ------------------------------------------------------------------

    def setup(self) -> None:
        """初始化 NoneBot2，注册适配器，加载 Agent 插件

        此方法 **不** 启动服务器，仅完成初始化配置。
        在 start() 之前必须调用。

        Raises:
            ImportError: 未安装 nonebot2 或必要的适配器包
            RuntimeError: IM 功能未在配置中启用
        """
        if not self._config.im_enabled:
            raise RuntimeError(
                "IM 功能未启用。请在 .env 中设置 IM_ENABLED=true"
            )

        try:
            import nonebot
        except ImportError as e:
            raise ImportError(
                "未安装 nonebot2，请执行：\n"
                "  pip install nonebot2[fastapi]"
            ) from e

        logger.info(
            "🚀 [IM/Server] 初始化 NoneBot2 Bot Server... "
            "host=%s, port=%d",
            self._config.im_host,
            self._config.im_port,
        )

        # 1. 初始化 NoneBot2
        #    NoneBot2 通过环境变量自动读取适配器配置，
        #    我们在 os.environ 中提前写入必要的 token/key
        self._inject_adapter_env()

        nonebot.init(
            host=self._config.im_host,
            port=self._config.im_port,
            # 关闭 NoneBot2 自身的 superusers 功能（由白名单替代）
            superusers=set(),
            # 日志级别
            log_level=self._config.log_level,
        )

        # 2. 注册适配器
        driver = nonebot.get_driver()
        self._registered_platforms: list[str] = []

        from .adapters.telegram_adapter import setup_telegram
        from .adapters.feishu_adapter import setup_feishu

        if setup_telegram(driver, self._config.telegram_bot_token):
            self._registered_platforms.append("Telegram")

        if setup_feishu(
            driver,
            self._config.feishu_app_id,
            self._config.feishu_app_secret,
            self._config.feishu_verification_token,
        ):
            self._registered_platforms.append("Feishu")

        if not self._registered_platforms:
            logger.warning(
                "⚠️  [IM/Server] 没有任何平台适配器被成功注册！"
                "请至少配置 TELEGRAM_BOT_TOKEN 或 FEISHU_APP_ID/SECRET。"
            )

        # 3. 初始化 IMSessionManager 和 RateLimiter
        from .session_manager import IMSessionManager
        from .rate_limiter import RateLimiter

        session_manager = IMSessionManager(
            config=self._config,
            agent_type=self._config.im_agent_type,
            system_prompt=self._build_system_prompt(),
        )

        rate_limiter: Optional[RateLimiter] = None
        if self._config.im_rate_limit > 0:
            rate_limiter = RateLimiter(
                max_requests=self._config.im_rate_limit,
                window_seconds=60,
            )

        # 白名单：逗号分隔字符串 -> set
        whitelist: set[str] = set()
        raw_whitelist = self._config.im_whitelist or ""
        if raw_whitelist.strip():
            whitelist = {uid.strip() for uid in raw_whitelist.split(",") if uid.strip()}
            logger.info("🔒 [IM/Server] 白名单已启用，共 %d 个用户。", len(whitelist))

        # 4. 加载插件（必须在 nonebot.init() 之后、run() 之前）
        nonebot.load_plugin("protocols.im.plugin")

        # 注入运行时依赖到插件
        from . import plugin as _plugin_module
        _plugin_module._init_plugin(session_manager, rate_limiter, whitelist)

        # 注册消息响应器
        _plugin_module._register_handlers()

        # 5. 获取 ASGI app（供外部集成，如嵌入现有 FastAPI）
        self._nb_app = nonebot.get_asgi()

        logger.info(
            "✅ [IM/Server] 初始化完成。已注册平台: %s",
            ", ".join(self._registered_platforms) or "无",
        )

    def start(self) -> None:
        """启动 NoneBot2 服务（阻塞）

        必须在 setup() 之后调用。

        Raises:
            RuntimeError: setup() 尚未调用
        """
        if self._nb_app is None:
            raise RuntimeError("请先调用 setup() 完成初始化，再调用 start()。")

        logger.info(
            "🌐 [IM/Server] IM Bot Server 正在启动，监听 %s:%d...",
            self._config.im_host,
            self._config.im_port,
        )
        logger.info(
            "📱 [IM/Server] 已启用平台: %s",
            ", ".join(self._registered_platforms) or "无",
        )

        try:
            import nonebot
            nonebot.run()  # 阻塞
        except KeyboardInterrupt:
            logger.info("⛔ [IM/Server] 收到停止信号，Bot Server 已关闭。")

    @property
    def asgi_app(self):
        """返回 NoneBot2 的 ASGI app（用于嵌入外部 ASGI 框架）

        Returns:
            ASGI application，或 None（setup() 未调用时）
        """
        return self._nb_app

    # ------------------------------------------------------------------
    # 私有方法
    # ------------------------------------------------------------------

    def _inject_adapter_env(self) -> None:
        """将适配器所需的凭据注入到 os.environ

        NoneBot2 的 Telegram 适配器通过 TELEGRAM_BOT_TOKEN 环境变量读取 Token；
        飞书适配器通过 FEISHU_APP_ID / FEISHU_APP_SECRET 读取。
        这里确保配置类的值被正确写入环境变量（防止 .env 顺序问题）。
        """
        if self._config.telegram_bot_token:
            os.environ.setdefault(
                "TELEGRAM_BOT_TOKEN", self._config.telegram_bot_token
            )
        if self._config.feishu_app_id:
            os.environ.setdefault("FEISHU_APP_ID", self._config.feishu_app_id)
        if self._config.feishu_app_secret:
            os.environ.setdefault(
                "FEISHU_APP_SECRET", self._config.feishu_app_secret
            )
        if self._config.feishu_verification_token:
            os.environ.setdefault(
                "FEISHU_VERIFICATION_TOKEN",
                self._config.feishu_verification_token,
            )

    @staticmethod
    def _build_system_prompt() -> str:
        """构建 IM 场景专用的系统提示词

        Returns:
            系统提示词字符串
        """
        return (
            "你是一个智能助手，通过即时通讯平台与用户对话。\n\n"
            "行为准则：\n"
            "- 回复应简洁友好，适合即时通讯场景\n"
            "- 复杂问题可分步回答，保持每次回复清晰易读\n"
            "- 如果需要使用工具获取最新信息，请告知用户正在查询\n"
            "- 遇到无法处理的请求，礼貌说明并给出替代建议\n"
            "- 不透露内部实现细节（如模型名称、工具列表等）\n"
        )
