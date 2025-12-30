from typing import List, Dict, Any

def classify_output(result: List[Any]) -> str:
    """
    Classify SQL result type.

    Returns:
        'scalar' | 'table' | 'time_series'
    """

    if not result:
        return "table"

    # Scalar: one row, one column
    if len(result) == 1 and isinstance(result[0], dict) and len(result[0]) == 1:
        return "scalar"

    # Time series: heuristic
    first_row = result[0]

    if isinstance(first_row, dict):
        keys = list(first_row.keys())

        if any("date" in k or "time" in k for k in keys):
            if len(keys) == 2:
                return "time_series"

    return "table"
