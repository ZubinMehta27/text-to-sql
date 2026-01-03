def retry_decision(state):
    """
    Decide next step after SQL validation.
    Pure control-flow logic.
    """

    # Case 1: SQL is valid → execute
    if state.sql_valid:
        return "execute_sql"

    # Case 2: SQL invalid AND retries exhausted → stop
    if state.retry_count >= state.max_retries:
        return "final_response"

    # Case 3: SQL invalid AND retries left → retry
    return "generate_sql"
