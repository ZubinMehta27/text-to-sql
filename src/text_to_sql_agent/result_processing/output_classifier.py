from typing import List, Dict, Any

def classify_output(result: List[Any]) -> str:
    """
    Classify SQL result type.

    Returns:
        'scalar' | 'list' | 'table' | 'time_series'
    """

    if not result:
        return "table"

    # ------------------------------------------------------------
    # Scalar: one row, one column
    # ------------------------------------------------------------
    if len(result) == 1 and isinstance(result[0], dict) and len(result[0]) == 1:
        return "scalar"

    first_row = result[0]

    # ------------------------------------------------------------
    # List: multiple rows, exactly one column
    # ------------------------------------------------------------
    if (
        len(result) > 1
        and isinstance(first_row, dict)
        and len(first_row) == 1
    ):
        return "list"

    # ------------------------------------------------------------
    # Time series: exactly two columns, one is date/time
    # ------------------------------------------------------------
    if isinstance(first_row, dict):
        keys = list(first_row.keys())

        if len(keys) == 2 and any("date" in k or "time" in k for k in keys):
            return "time_series"

    # ------------------------------------------------------------
    # Default: table
    # ------------------------------------------------------------
    return "table"
