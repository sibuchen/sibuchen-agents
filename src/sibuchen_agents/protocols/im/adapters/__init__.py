"""平台适配器子包

每个子模块封装对应平台 NoneBot2 Adapter 的初始化逻辑。
"""

from .telegram_adapter import setup_telegram
from .feishu_adapter import setup_feishu

__all__ = ["setup_telegram", "setup_feishu"]
