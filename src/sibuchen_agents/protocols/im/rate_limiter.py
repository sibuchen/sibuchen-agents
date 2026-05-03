"""速率限制器 - 基于滑动时间窗口，按会话 ID 计数

用法：
    limiter = RateLimiter(max_requests=10, window_seconds=60)
    if not limiter.allow(session_id):
        await bot.send(event, "请求过于频繁，请稍后再试。")
        return
"""

import time
from collections import defaultdict, deque
from threading import Lock
from typing import Deque, Dict


class RateLimiter:
    """滑动窗口速率限制器

    线程安全（asyncio 场景中每个协程单线程，但保留 Lock 以备混用场景）。

    Args:
        max_requests: 窗口内最大请求数
        window_seconds: 时间窗口长度（秒），默认 60s
    """

    def __init__(self, max_requests: int = 10, window_seconds: int = 60) -> None:
        self._max_requests = max_requests
        self._window = window_seconds
        # session_id -> deque of timestamps
        self._records: Dict[str, Deque[float]] = defaultdict(deque)
        self._lock = Lock()

    # ------------------------------------------------------------------
    # 公开方法
    # ------------------------------------------------------------------

    def allow(self, session_id: str) -> bool:
        """判断该 session 当前请求是否被允许

        Args:
            session_id: 会话唯一标识（形如 "telegram:123456"）

        Returns:
            True 表示允许，False 表示超出限制
        """
        now = time.monotonic()
        cutoff = now - self._window

        with self._lock:
            q = self._records[session_id]

            # 移除窗口外的旧记录
            while q and q[0] < cutoff:
                q.popleft()

            if len(q) >= self._max_requests:
                return False

            q.append(now)
            return True

    def remaining(self, session_id: str) -> int:
        """返回该 session 在当前窗口内剩余可用请求数

        Args:
            session_id: 会话唯一标识

        Returns:
            剩余可用次数（>= 0）
        """
        now = time.monotonic()
        cutoff = now - self._window

        with self._lock:
            q = self._records[session_id]
            used = sum(1 for ts in q if ts >= cutoff)
            return max(0, self._max_requests - used)

    def reset(self, session_id: str) -> None:
        """手动清除该 session 的限流记录（管理员操作）

        Args:
            session_id: 会话唯一标识
        """
        with self._lock:
            self._records.pop(session_id, None)

    def clear_all(self) -> None:
        """清除所有 session 的限流记录"""
        with self._lock:
            self._records.clear()
