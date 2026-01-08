from text_to_sql_agent.graph_state import GraphState
from text_to_sql_agent.runtime_bootstrap import SCHEMA_FINGERPRINT

def build_initial_state(
    user_query: str,
    schema_context: str,
    schema_entities: set[str],
    max_retries: int = GraphState.max_retries,
    default_recent_limit: int = GraphState.default_recent_limit,
    default_popular_limit: int = GraphState.default_popular_limit,
) -> GraphState:
    """
    Build the initial graph state.
    This is the ONLY place where defaults are set.
    """

    return GraphState(
        user_query=user_query,
        schema_context=schema_context,
        schema_entities=schema_entities,

        sql_query=None,
        sql_valid=False,
        validation_error=None,

        retry_count=0,
        max_retries=max_retries,

        default_recent_limit=default_recent_limit,
        default_popular_limit=default_popular_limit,

        # --- observability defaults ---
        last_error_type=None,
        last_error_message=None,
        termination_reason=None,
        retry_reason=None,

        schema_fingerprint=SCHEMA_FINGERPRINT,

        final_answer=None,
    )