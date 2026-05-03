"""Telegram 适配器初始化封装

负责：
- 验证必要配置（TELEGRAM_BOT_TOKEN）
- 将 nonebot-adapter-telegram 注册到 NoneBot2 Driver
- 根据配置选择 Polling（本地开发）或 Webhook（生产）模式

依赖：
    pip install nonebot-adapter-telegram
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from nonebot import Driver

logger = logging.getLogger(__name__)

# NoneBot2 Telegram 适配器的环境变量名
_TOKEN_ENV = "TELEGRAM_BOT_TOKEN"


def setup_telegram(driver: "Driver", bot_token: str | None) -> bool:
    """注册 Telegram 适配器到 NoneBot2 Driver

    Args:
        driver: NoneBot2 Driver 实例（通过 nonebot.get_driver() 获取）
        bot_token: Telegram Bot Token（来自 @BotFather）

    Returns:
        True 表示注册成功，False 表示跳过（未配置 Token）

    Raises:
        ImportError: 未安装 nonebot-adapter-telegram
    """
    if not bot_token:
        logger.warning(
            "⚠️  [IM/Telegram] TELEGRAM_BOT_TOKEN 未配置，跳过 Telegram 适配器注册。"
            "如需启用，请在 .env 中设置 TELEGRAM_BOT_TOKEN=<your_bot_token>"
        )
        return False

    try:
        from nonebot.adapters.telegram import Adapter as TelegramAdapter
    except ImportError as e:
        raise ImportError(
            "未安装 nonebot-adapter-telegram，请执行：\n"
            "  pip install nonebot-adapter-telegram"
        ) from e

    driver.register_adapter(TelegramAdapter)
    logger.info(
        "✅ [IM/Telegram] Telegram 适配器已注册。"
        "Bot Token: %s***（已隐藏）",
        bot_token[:8],
    )
    return True
