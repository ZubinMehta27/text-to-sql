from text_to_sql_agent.graph_state import GraphState

def build_initial_state(
    user_query: str,
    schema_context: str,
    max_retries: int = 3,
) -> GraphState:
    """
    Build the initial graph state.
    This is the ONLY place where defaults are set.
    """

    return {
        "user_query": user_query,
        "schema_context": schema_context,

        "sql_query": None,
        "sql_valid": False,
        "validation_error": None,

        "retry_count": 0,
        "max_retries": max_retries,

        "final_answer": None,
    }
