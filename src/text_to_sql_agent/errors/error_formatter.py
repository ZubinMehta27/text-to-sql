def format_error_message(raw_error: str) -> dict:
    """
    Convert low-level SQL/validation errors into
    clear, user-facing messages.
    """

    if not raw_error:
        return {
            "type": "error",
            "message": "The query could not be processed.",
        }

    msg = raw_error.lower()

    # -----------------------------
    # Schema errors (terminal)
    # -----------------------------
    if "no such table" in msg or "unknown table" in msg:
        return {
            "type": "error",
            "message": "The query refers to a table that does not exist in the database.",
        }

    if "no such column" in msg or "unknown column" in msg:
        return {
            "type": "error",
            "message": "The query refers to a column that does not exist in the database.",
        }

    # -----------------------------
    # Join / relationship errors
    # -----------------------------
    if "join" in msg and "not supported" in msg:
        return {
            "type": "error",
            "message": "The requested tables cannot be joined using the database relationships.",
        }

    # -----------------------------
    # Grouping / aggregation errors
    # -----------------------------
    if "group by" in msg:
        return {
            "type": "error",
            "message": "The query mixes aggregated and non-aggregated fields incorrectly.",
        }

    # -----------------------------
    # Fallback
    # -----------------------------
    return {
        "type": "error",
        "message": "The query could not be answered with the available schema.",
    }
