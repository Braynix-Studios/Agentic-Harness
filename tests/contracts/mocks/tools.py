"""Deterministic fake tool provider for contract tests."""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence

from core.contracts.common import JsonObject, JsonValue
from core.contracts.errors import ErrorCode, ErrorInfo, P3Error
from core.contracts.mcp import ToolCallRequest, ToolCallResult, ToolDescriptor

ToolHandler = Callable[[Mapping[str, JsonValue]], JsonValue]


class MockToolProvider:
    def __init__(
        self,
        tools: Sequence[ToolDescriptor] = (),
        handlers: Mapping[str, ToolHandler] | None = None,
    ) -> None:
        self._tools = {tool.name: tool for tool in tools}
        self._handlers = dict(handlers or {})

    async def list_tools(self) -> Sequence[ToolDescriptor]:
        return tuple(self._tools[name] for name in sorted(self._tools))

    async def call_tool(self, request: ToolCallRequest) -> ToolCallResult:
        if request.tool_name not in self._tools or request.tool_name not in self._handlers:
            return ToolCallResult(
                request_id=request.request_id,
                tool_name=request.tool_name,
                error=ErrorInfo(
                    code=ErrorCode.NOT_FOUND,
                    message=f"Tool '{request.tool_name}' is not available in the mock provider",
                ),
            )
        try:
            result = self._handlers[request.tool_name](request.arguments)
        except P3Error as exc:
            return ToolCallResult(
                request_id=request.request_id,
                tool_name=request.tool_name,
                error=exc.to_info(),
            )
        return ToolCallResult(
            request_id=request.request_id,
            tool_name=request.tool_name,
            result=result,
        )


def echo_handler(arguments: Mapping[str, JsonValue]) -> JsonObject:
    """Small reusable handler for examples and smoke tests."""

    return {"echo": dict(arguments)}
