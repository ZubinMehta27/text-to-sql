from dataclasses import dataclass, field
from typing import Any, List, Optional, Set

from text_to_sql_agent import config


@dataclass
class GraphState:
    """
    Shared state object passed through LangGraph.
    Defaults are REQUIRED to avoid runtime crashes.
    """
    user_query: str
    schema_context: str

    schema_entities: Set[str] = field(default_factory=set)

    execution_mode: Optional[str] = None

    sql_query: Optional[str] = None
    sql_valid: bool = False
    validation_error: Optional[str] = None

    execution_result: Optional[List[dict[str, Any]]] = None

    retry_count: int = 0
    max_retries: int = 3

    default_recent_limit: int = 10
    default_popular_limit: int = 5

    # --- Observability ---
    last_error_type: str | None = None
    last_error_message: str | None = None
    termination_reason: str | None = None
    retry_reason: str | None = None

    schema_fingerprint: str | None = None

    final_answer: Optional[dict] = None
