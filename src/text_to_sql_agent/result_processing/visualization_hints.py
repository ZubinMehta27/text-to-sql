def visualization_hint(output_type: str) -> dict:
    """
    Suggest visualization options.
    """
    if output_type == "scalar":
        return {
            "recommended": ["metric_card"]
        }

    if output_type == "time_series":
        return {
            "recommended": ["line_chart", "area_chart"]
        }

    if output_type == "table":
        return {
            "recommended": ["data_table", "bar_chart"]
        }

    return {}