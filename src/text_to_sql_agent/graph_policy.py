from text_to_sql_agent.retry.error_classifier import classify_sql_error

def retry_decision(state):
    # SQL valid → execute
    if state.sql_valid:
        return "execute_sql"

    # Retries exhausted → stop
    if state.retry_count >= state.max_retries:
        return "final_response"

    # Always retry otherwise
    return "generate_sql"

