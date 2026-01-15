from dataclasses import dataclass, field
from typing import Any, List, Optional, Set

@dataclass
class GraphState:
    """
    Shared state object passed through LangGraph.
    Defaults are REQUIRED to avoid runtime crashes.
    """

    # --- Core inputs ---
    user_query: str
    schema_context: str
    schema_entities: Set[str] = field(default_factory=set)

    # --- Execution control ---
    execution_mode: Optional[str] = None

    # --- SQL lifecycle ---
    sql_query: Optional[str] = None
    sql_valid: bool = False
    validation_error: Optional[str] = None
    execution_result: Optional[List[dict[str, Any]]] = None

    # --- Retry policy ---
    retry_count: int = 0
    max_retries: int = 3

    # --- Defaults ---
    default_recent_limit: int = 10
    default_popular_limit: int = 5

    # --- Observability ---
    last_error_type: str | None = None
    last_error_message: str | None = None
    termination_reason: str | None = None
    retry_reason: str | None = None

    schema_fingerprint: str | None = None

    # --- Tool + LLM metadata ---
    invoked_tools: list[dict] = field(default_factory=list)

    llm: Any | None = None   # ✅ ADD THIS

    final_answer: Optional[dict] = None
