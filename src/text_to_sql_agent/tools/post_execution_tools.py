from langchain.tools import tool
import json


@tool
def summarize_result_table(rows: list[dict]) -> str:
    """
    Generate a concise, natural-language insight from a SQL result table.
    Focus on key patterns, extremes, or rankings.
    Do NOT explain the schema.
    Do NOT describe columns.
    Do NOT use placeholders.
    Be brief and factual.
    """

    return (
        "You are a data analyst explaining query results to a business user.\n\n"
        "Given the following SQL query result (as JSON rows), write ONE or TWO sentences "
        "summarizing the most important insight.\n\n"
        "Rules:\n"
        "- Do NOT explain what the columns mean\n"
        "- Do NOT describe rows generically\n"
        "- Do NOT use placeholders or variables\n"
        "- Focus on rankings, highest/lowest values, or notable patterns\n"
        "- Use actual values from the data\n"
        "- Keep it concise and natural\n\n"
        f"SQL Result:\n{json.dumps(rows, indent=2)}"
    )
