import time
import uuid
from typing import Any, Dict

from text_to_sql_agent.sql_tools.sql_tools import HardTermination


def safe_execute_graph(
    graph,
    state,
) -> Dict[str, Any]:
    """
    Production-safe execution wrapper.
    This is the ONLY place where graph.invoke() should be called.
    """

    request_id = str(uuid.uuid4())
    start_time = time.time()

    final_state: Dict[str, Any] = {}

    try:
        final_state = graph.invoke(state) or {}

        latency_ms = int((time.time() - start_time) * 1000)

        response = {
            "version": "v1",
            "request_id": request_id,
            "success": True,
            "result": final_state.get("final_answer"),
            "metadata": {
                "latency_ms": latency_ms,
                "retry_count": final_state.get("retry_count"),
                "execution_mode": final_state.get("execution_mode"),
                "retry_reason": final_state.get("retry_reason"),
                "termination_reason": final_state.get("termination_reason"),
                "last_error_type": final_state.get("last_error_type"),
            },
        }

        # --- additive, non-breaking fields ---
        if "post_execution_summary" in final_state:
            response["post_execution_summary"] = final_state["post_execution_summary"]

        if "invoked_tools" in final_state:
            response["invoked_tools"] = final_state["invoked_tools"]

        return response

    except HardTermination as e:
        latency_ms = int((time.time() - start_time) * 1000)

        return {
            "version": "v1",
            "request_id": request_id,
            "success": False,
            "result": {
                "type": "error",
                "message": str(e),
            },
            "metadata": {
                "latency_ms": latency_ms,
                "retry_count": final_state.get("retry_count"),
                "execution_mode": final_state.get("execution_mode"),
                "retry_reason": final_state.get("retry_reason"),
                "termination_reason": final_state.get("termination_reason"),
                "last_error_type": final_state.get("last_error_type"),
            },
        }

    except Exception:
        latency_ms = int((time.time() - start_time) * 1000)

        return {
            "version": "v1",
            "request_id": request_id,
            "success": False,
            "result": {
                "type": "error",
                "message": "An internal error occurred while processing the query.",
            },
            "metadata": {
                "latency_ms": latency_ms,
                "retry_count": final_state.get("retry_count"),
                "execution_mode": final_state.get("execution_mode"),
                "retry_reason": final_state.get("retry_reason"),
                "termination_reason": final_state.get("termination_reason"),
                "last_error_type": final_state.get("last_error_type"),
            },
        }
