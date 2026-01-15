def retry_decision(state):
    """
    Decide next step after SQL validation.
    Repair is attempted ONCE before regeneration.
    """

    # SQL valid → execute
    if state.sql_valid:
        return "execute_sql"

    # Retries exhausted → stop
    if state.retry_count >= state.max_retries:
        return "final_response"

    # Attempt repair if SQL exists and validation failed
    if state.sql_query and state.retry_reason == "retryable_sql_error":
        # Only repair once
        if not any(
            t.get("tool") == "repair_sql_query"
            for t in state.invoked_tools
        ):
            return "repair_sql"

    # Otherwise regenerate
    return "generate_sql"