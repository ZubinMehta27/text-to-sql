from dataclasses import dataclass
from typing import Optional, Any


@dataclass
class GraphState:
    """
    Shared state object passed through LangGraph.
    Defaults are REQUIRED to avoid runtime crashes during reloads.
    """

    user_query: str
    schema_context: str = ""  

    sql_query: Optional[str] = None
    result: Optional[Any] = None
    final_answer: Optional[Any] = None
