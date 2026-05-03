"""Wrapper around SibuchenAgents SimpleAgent that records tool calls."""

from __future__ import annotations

import ast
import json
import logging
from collections.abc import Iterator
from typing import Any, Callable, Optional

from .simple_agent import SimpleAgent
from sibuchen_agents.core.message import SibuchenMessage
from tools import ToolRegistry
from sibuchen_agents.tools.response import ToolResponse

logger = logging.getLogger(__name__)


class ToolAwareSimpleAgent(SimpleAgent):
    """SimpleAgent 子类，记录工具调用情况。

    ToolAwareSimpleAgent 扩展了 SimpleAgent，增加了工具调用监听功能。
    这使得外部系统可以追踪和记录智能体的工具调用行为，用于日志记录、
    调试、性能分析等场景。

    主要特性：
    - 工具调用监听：通过回调函数记录每次工具调用的详细信息
    - 增强的工具调用解析：支持复杂的嵌套参数和字符串处理
    - 流式工具调用：在流式输出中支持工具调用
    - 参数清理：自动清理和规范化工具参数

    """

    def __init__(
        self,
        *args: Any,
        tool_call_listener: Optional[Callable[[dict[str, Any]], None]] = None,
        **kwargs: Any,
    ) -> None:
        """初始化 ToolAwareSimpleAgent。

        Args:
            *args: 传递给 SimpleAgent 的位置参数
            tool_call_listener: 工具调用监听器回调函数，接收包含工具调用信息的字典
            **kwargs: 传递给 SimpleAgent 的关键字参数
        """
        super().__init__(*args, **kwargs)
        self._tool_call_listener = tool_call_listener

    def _execute_tool_call(self, tool_name: str, parameters: str) -> str:  # type: ignore[override]
        """执行工具调用并通知监听器。

        Args:
            tool_name: 工具名称
            parameters: 工具参数（字符串格式）

        Returns:
            工具执行结果的格式化字符串
        """
        if not self.tool_registry:
            return "❌ 错误：未配置工具注册表"

        try:
            tool = self.tool_registry.get_tool(tool_name)
            if not tool:
                return f"❌ 错误：未找到工具 '{tool_name}'"

            parsed_parameters = self._parse_tool_parameters(tool_name, parameters)
            parsed_parameters = self._sanitize_parameters(parsed_parameters)

            result = tool.run(parsed_parameters)
            # Extract text content if it's a ToolResponse object
            text_result = result.text if isinstance(result, ToolResponse) else str(result)
            formatted_result = f"🔧 工具 {tool_name} 执行结果：\n{text_result}"
        except Exception as exc:  # pragma: no cover - tool failures回退
            parsed_parameters = {}
            formatted_result = f"❌ 工具调用失败：{exc}"

        # 通知监听器
        if self._tool_call_listener:
            try:
                self._tool_call_listener(
                    {
                        "agent_name": self.name,
                        "tool_name": tool_name,
                        "raw_parameters": parameters,
                        "parsed_parameters": parsed_parameters,
                        "result": formatted_result,
                    }
                )
            except Exception:  # pragma: no cover - 防御性兜底
                logger.exception("Tool call listener failed")

        return formatted_result

    def _parse_tool_calls(self, text: str) -> list:  # type: ignore[override]
        """解析文本中的工具调用。

        支持格式：[TOOL_CALL:tool_name:parameters]

        Args:
            text: 包含工具调用的文本

        Returns:
            工具调用列表，每个元素包含 tool_name、parameters 和 original
        """
        marker = "[TOOL_CALL:"
        calls: list = []
        start = 0

        while True:
            begin = text.find(marker, start)
            if begin == -1:
                break

            tool_start = begin + len(marker)
            colon = text.find(":", tool_start)
            if colon == -1:
                break

            tool_name = text[tool_start:colon].strip()
            body_start = colon + 1
            pos = body_start
            depth = 0
            in_string = False
            string_quote = ""

            while pos < len(text):
                char = text[pos]

                if char in {'"', "'"}:
                    if not in_string:
                        in_string = True
                        string_quote = char
                    elif string_quote == char and text[pos - 1] != "\\":
                        in_string = False

                if not in_string:
                    if char == '[':
                        depth += 1
                    elif char == ']':
                        if depth == 0:
                            body = text[body_start:pos].strip()
                            original = text[begin : pos + 1]
                            calls.append(
                                {
                                    "tool_name": tool_name,
                                    "parameters": body,
                                    "original": original,
                                }
                            )
                            start = pos + 1
                            break
                        else:
                            depth -= 1

                pos += 1
            else:
                break

        return calls

    @staticmethod
    def _find_tool_call_end(text: str, start_index: int) -> int:
        """查找工具调用的结束位置。

        Args:
            text: 文本内容
            start_index: 工具调用的起始位置

        Returns:
            工具调用结束位置的索引，如果未找到返回 -1
        """
        marker = "[TOOL_CALL:"
        tool_start = start_index + len(marker)
        colon = text.find(":", tool_start)
        if colon == -1:
            return -1

        body_start = colon + 1
        pos = body_start
        depth = 0
        in_string = False
        string_quote = ""

        while pos < len(text):
            char = text[pos]

            if char in {'"', "'"}:
                if not in_string:
                    in_string = True
                    string_quote = char
                elif string_quote == char and text[pos - 1] != "\\":
                    in_string = False

            if not in_string:
                if char == '[':
                    depth += 1
                elif char == ']':
                    if depth == 0:
                        return pos
                    depth -= 1

            pos += 1

        return -1

    @staticmethod
    def attach_registry(agent: "ToolAwareSimpleAgent", registry: ToolRegistry | None) -> None:
        """Helper to attach a tool registry if provided.

        Args:
            agent: ToolAwareSimpleAgent 实例
            registry: 工具注册表
        """
        if registry:
            agent.tool_registry = registry
            agent.enable_tool_calling = True

    @staticmethod
    def _sanitize_parameters(parameters: dict[str, Any]) -> dict[str, Any]:
        """清理和规范化工具参数。

        Args:
            parameters: 原始参数字典

        Returns:
            清理后的参数字典
        """
        sanitized: dict[str, Any] = {}
        for key, value in parameters.items():
            if isinstance(value, (int, float, bool, list, dict)):
                sanitized[key] = value
                continue

            if isinstance(value, str):
                normalized = ToolAwareSimpleAgent._normalize_string(value)

                if key == "task_id":
                    try:
                        sanitized[key] = int(normalized)
                        continue
                    except ValueError:
                        pass

                if key == "tags":
                    parsed_tags = ToolAwareSimpleAgent._coerce_sequence(normalized)
                    if isinstance(parsed_tags, list):
                        sanitized[key] = parsed_tags
                        continue
                    if normalized:
                        sanitized[key] = [item.strip() for item in normalized.split(",") if item.strip()]
                        continue

                if key in {"note_type", "action", "title", "content", "note_id"}:
                    sanitized[key] = normalized
                    continue

                sanitized[key] = normalized
                continue

            sanitized[key] = value

        return sanitized

    @staticmethod
    def _normalize_string(value: str) -> str:
        """规范化字符串值，移除多余的引号和括号。

        Args:
            value: 原始字符串

        Returns:
            规范化后的字符串
        """
        trimmed = value.strip()

        if trimmed and trimmed[0] in {'"', "'"} and trimmed.count(trimmed[0]) == 1:
            trimmed = trimmed[1:]
        if trimmed and trimmed[-1] in {'"', "'"} and trimmed.count(trimmed[-1]) == 1:
            trimmed = trimmed[:-1]

        if trimmed and trimmed[0] in {'"', "'"} and trimmed[-1] == trimmed[0]:
            trimmed = trimmed[1:-1]

        if trimmed and trimmed[0] in {'[', '('} and trimmed[-1] not in {']', ')'}:
            closing = ']' if trimmed[0] == '[' else ')'
            trimmed = f"{trimmed}{closing}"

        return trimmed.strip()

    def stream_run(self, input_text: str, max_tool_iterations: int = 3, **kwargs: Any) -> Iterator[str]:  # type: ignore[override]
        """Stream assistant output while supporting tool calls mid-generation.

        流式运行智能体，支持在生成过程中调用工具。

        Args:
            input_text: 用户输入文本
            max_tool_iterations: 最大工具调用迭代次数
            **kwargs: 传递给 LLM 的额外参数

        Yields:
            生成的文本片段
        """
        messages: list[dict[str, Any]] = []
        enhanced_system_prompt = self._get_enhanced_system_prompt()
        messages.append({"role": "system", "content": enhanced_system_prompt})

        for msg in self._history:
            messages.append({"role": msg.role, "content": msg.content})

        messages.append({"role": "user", "content": input_text})

        final_segments: list[str] = []
        final_response_text = ""
        current_iteration = 0

        marker = "[TOOL_CALL:"

        while current_iteration < max_tool_iterations:
            residual = ""
            segments_this_round: list[str] = []
            tool_call_texts: list[str] = []

            def process_residual(final_pass: bool = False) -> Iterator[str]:
                nonlocal residual
                while True:
                    start = residual.find(marker)
                    if start == -1:
                        safe_len = len(residual) if final_pass else max(0, len(residual) - (len(marker) - 1))
                        if safe_len > 0:
                            segment = residual[:safe_len]
                            residual = residual[safe_len:]
                            yield segment
                        break

                    if start > 0:
                        segment = residual[:start]
                        residual = residual[start:]
                        if segment:
                            yield segment
                        continue

                    end = self._find_tool_call_end(residual, 0)
                    if end == -1:
                        break

                    tool_call_texts.append(residual[: end + 1])
                    residual = residual[end + 1 :]

            for chunk in self.llm.stream_invoke(messages, **kwargs):
                if not chunk:
                    continue

                residual += chunk

                for segment in process_residual():
                    if not segment:
                        continue
                    segments_this_round.append(segment)
                    final_segments.append(segment)
                    yield segment

            for segment in process_residual(final_pass=True):
                if not segment:
                    continue
                segments_this_round.append(segment)
                final_segments.append(segment)
                yield segment

            clean_response = "".join(segments_this_round)
            tool_calls: list[dict[str, Any]] = []

            for call_text in tool_call_texts:
                tool_calls.extend(self._parse_tool_calls(call_text))

            if tool_calls:
                messages.append({"role": "assistant", "content": clean_response})

                tool_results = []
                for call in tool_calls:
                    result = self._execute_tool_call(call["tool_name"], call["parameters"])
                    tool_results.append(result)

                tool_results_text = "\n\n".join(tool_results)
                messages.append(
                    {
                        "role": "user",
                        "content": (
                            "工具执行结果：\n"
                            f"{tool_results_text}\n\n"
                            "请基于这些结果给出完整的回答。"
                        ),
                    }
                )

                current_iteration += 1
                continue

            final_response_text = clean_response
            break

        if current_iteration >= max_tool_iterations and not final_response_text:
            fallback_response = self.llm.invoke(messages, **kwargs)
            fallback_content = fallback_response.content if hasattr(fallback_response, "content") else str(fallback_response)
            final_segments.append(fallback_content)
            final_response_text = fallback_content
            yield fallback_content

        stored_response = final_response_text or "".join(final_segments)

        self.add_message(SibuchenMessage("user", input_text))
        self.add_message(SibuchenMessage("assistant", stored_response))

    @staticmethod
    def _coerce_sequence(value: str) -> Any:
        """尝试将字符串转换为列表。

        Args:
            value: 字符串值

        Returns:
            解析后的列表，如果解析失败返回 None
        """
        if not value:
            return None

        candidates = [value]
        if value.startswith("[") and not value.endswith("]"):
            candidates.append(f"{value}]")
        if value.startswith("(") and not value.endswith(")"):
            candidates.append(f"{value})")

        for candidate in candidates:
            for loader in (json.loads, ast.literal_eval):
                try:
                    parsed = loader(candidate)
                except Exception:
                    continue
                if isinstance(parsed, list):
                    return parsed

        return None

    def _parse_tool_parameters(self, tool_name: str, parameters: str) -> dict[str, Any]:
        """将工具参数字符串解析为字典。

        Args:
            tool_name: 工具名称
            parameters: 参数字符串

        Returns:
            解析后的参数字典
        """
        if not parameters:
            return {}

        # 尝试解析为 JSON
        try:
            return json.loads(parameters)
        except json.JSONDecodeError:
            pass

        # 尝试解析为 Python 字面量
        try:
            val = ast.literal_eval(parameters)
            if isinstance(val, dict):
                return val
            return {"input": val}
        except (ValueError, SyntaxError):
            pass

        # 如果都不是，作为普通字符串处理
        return {"input": parameters}

    def _get_enhanced_system_prompt(self) -> str:
        """获取增强的系统提示词，包含工具使用说明。

        Returns:
            增强后的系统提示词字符串
        """
        base_prompt = self.system_prompt or "你是一个有用的 AI 助手。"
        if not self.tool_registry:
            return base_prompt

        tools_desc = self.tool_registry.get_tools_description()

        enhancement = f"""
## 工具使用说明
你可以使用以下工具来协助你回答问题：
{tools_desc}

## 调用格式
当需要调用工具时，请严格遵循以下格式：
[TOOL_CALL:工具名称:参数]

例如：
[TOOL_CALL:web_search:{{"query": "今天的天气"}}]

注意：
1. 参数必须是有效的 JSON 格式（或者简单的字符串，如果工具支持）。
2. 你可以一次调用多个工具，或者在一段话中嵌入工具调用。
3. 工具执行结果会自动提供给你。
"""
        return f"{base_prompt}\n{enhancement}"
