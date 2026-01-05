from text_to_sql_agent.retry.error_classifier import classify_sql_error


def retry_decision(state):
    """
    Decide next step after SQL validation.
    Pure control-flow logic.
    """

    # ------------------------------------------------------------
    # Case 1: SQL is valid → execute
    # ------------------------------------------------------------
    if state.sql_valid:
        return "execute_sql"

    # ------------------------------------------------------------
    # Case 2: SQL invalid but no error info → stop
    # ------------------------------------------------------------
    if not state.validation_error:
        return "final_response"

    error_type = classify_sql_error(state.validation_error)

    # ------------------------------------------------------------
    # Case 3: Terminal error → stop immediately (NO retries)
    # ------------------------------------------------------------
    if error_type == "terminal":
        return "final_response"

    # ------------------------------------------------------------
    # Case 4: Retryable error but retries exhausted → stop
    # ------------------------------------------------------------
    if state.retry_count >= state.max_retries:
        return "final_response"

    # ------------------------------------------------------------
    # Case 5: Retryable error and retries left → retry
    # ------------------------------------------------------------
    return "generate_sql"
