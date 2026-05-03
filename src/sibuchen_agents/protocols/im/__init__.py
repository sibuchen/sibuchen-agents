"""IM 模块 - 基于 NoneBot2 的多平台即时通讯接入层

支持的平台（MVP）：
- Telegram
- 飞书 (Feishu / Lark)

用法：
    from sibuchen_agents.protocols.im import IMServer, start_im_server
    start_im_server()
"""

from .server import IMServer
from .session_manager import IMSessionManager

__all__ = [
    "IMServer",
    "IMSessionManager",
    "start_im_server",
]


def start_im_server() -> None:
    """启动 IM Bot Server（阻塞）

    从 .env / 环境变量读取配置并启动 NoneBot2 服务。
    这是对外暴露的最简洁入口。

    Raises:
        ImportError: 未安装 nonebot2 时抛出
    """
    server = IMServer()
    server.setup()
    server.start()
