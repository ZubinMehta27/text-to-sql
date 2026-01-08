from text_to_sql_agent.retry.error_classifier import classify_sql_error


def retry_decision(state):
    if state.sql_valid:
        state.termination_reason = "sql_valid"
        return "execute_sql"

    if not state.validation_error:
        state.termination_reason = "no_validation_error"
        return "final_response"

    error_type = classify_sql_error(state.validation_error)

    state.last_error_type = error_type
    state.last_error_message = state.validation_error

    if error_type == "terminal":
        state.termination_reason = "terminal_sql_error"
        return "final_response"

    if state.retry_count >= state.max_retries:
        state.termination_reason = "retry_exhausted"
        return "final_response"

    state.retry_reason = "retryable_sql_error"
    return "generate_sql"

