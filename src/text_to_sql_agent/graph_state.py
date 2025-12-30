from dataclasses import dataclass
from typing import List, Optional


@dataclass
class GraphState:
    """
    Shared state object passed through LangGraph.
    Defaults are REQUIRED to avoid runtime crashes.
    """

    # ------------------------------------------------------------
    # Required at entry
    # ------------------------------------------------------------
    user_query: str
    schema_context: str

    # ------------------------------------------------------------
    # SQL generation / validation
    # ------------------------------------------------------------
    sql_query: Optional[str] = None
    sql_valid: bool = False
    validation_error: Optional[str] = None

    # ------------------------------------------------------------
    # Execution
    # ------------------------------------------------------------
    execution_result: Optional[List[dict]] = None

    # ------------------------------------------------------------
    # Retry policy
    # ------------------------------------------------------------
    retry_count: int = 0
    max_retries: int = 3

    # ------------------------------------------------------------
    # Final output
    # ------------------------------------------------------------
    final_answer: Optional[dict] = None
