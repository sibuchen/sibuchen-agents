"""飞书（Lark）适配器初始化封装

负责：
- 验证必要配置（FEISHU_APP_ID、FEISHU_APP_SECRET）
- 将 nonebot-adapter-feishu 注册到 NoneBot2 Driver

飞书 Webhook 模式：飞书服务器将事件 POST 到本机的
    http://<IM_HOST>:<IM_PORT>/feishu/

依赖：
    pip install nonebot-adapter-feishu
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from nonebot import Driver

logger = logging.getLogger(__name__)


def setup_feishu(
    driver: "Driver",
    app_id: str | None,
    app_secret: str | None,
    verification_token: str | None = None,
) -> bool:
    """注册飞书适配器到 NoneBot2 Driver

    Args:
        driver: NoneBot2 Driver 实例（通过 nonebot.get_driver() 获取）
        app_id: 飞书应用 App ID
        app_secret: 飞书应用 App Secret
        verification_token: 飞书 Webhook Verification Token（可选，增强安全）

    Returns:
        True 表示注册成功，False 表示跳过（未完整配置）

    Raises:
        ImportError: 未安装 nonebot-adapter-feishu
    """
    if not app_id or not app_secret:
        logger.warning(
            "⚠️  [IM/Feishu] FEISHU_APP_ID 或 FEISHU_APP_SECRET 未配置，"
            "跳过飞书适配器注册。"
            "如需启用，请在 .env 中设置 FEISHU_APP_ID 和 FEISHU_APP_SECRET。"
        )
        return False

    try:
        from nonebot.adapters.feishu import Adapter as FeishuAdapter
    except ImportError as e:
        raise ImportError(
            "未安装 nonebot-adapter-feishu，请执行：\n"
            "  pip install nonebot-adapter-feishu"
        ) from e

    driver.register_adapter(FeishuAdapter)
    logger.info(
        "✅ [IM/Feishu] 飞书适配器已注册。App ID: %s***（已隐藏）",
        app_id[:4],
    )
    if verification_token:
        logger.info("✅ [IM/Feishu] Verification Token 已配置，启用事件签名验证。")
    else:
        logger.warning(
            "⚠️  [IM/Feishu] FEISHU_VERIFICATION_TOKEN 未配置，"
            "建议在生产环境中设置以防止伪造请求。"
        )
    return True
