from typing import Any, Callable, Dict

class ToolExecutionError(Exception):
    pass


def execute_tool(
    tool_fn: Callable[..., Any],
    *,
    reason: str,
    **kwargs,
) -> Dict[str, Any]:
    """
    Centralized tool execution wrapper.
    Tools NEVER mutate graph state.
    Tools NEVER raise upstream exceptions.
    """

    try:
        output = tool_fn(**kwargs)

        return {
            "success": True,
            "reason": reason,
            "output": output,
        }

    except Exception as e:
        return {
            "success": False,
            "reason": reason,
            "error": str(e),
        }