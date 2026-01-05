def classify_sql_error(error_msg: str) -> str:
    """
    Classify SQL errors into retryable vs terminal.
    """

    msg = error_msg.lower()

    # -----------------------------
    # TERMINAL (never retry)
    # -----------------------------
    if any(
        phrase in msg
        for phrase in [
            "no such table",
            "no such column",
            "unknown table",
            "unknown column",
            "does not exist",
            "cannot resolve",
        ]
    ):
        return "terminal"

    # -----------------------------
    # RETRYABLE (LLM can fix)
    # -----------------------------
    if any(
        phrase in msg
        for phrase in [
            "syntax error",
            "group by",
            "ambiguous column",
            "misuse of aggregate",
            "invalid sql",
        ]
    ):
        return "retryable"

    # Default: be conservative
    return "terminal"
