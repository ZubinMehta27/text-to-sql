from langchain_core.runnables import RunnableLambda
from langchain_core.messages import SystemMessage, HumanMessage

from text_to_sql_agent.result_processing.output_classifier import classify_output
from text_to_sql_agent.result_processing.table_formatter import format_table
from text_to_sql_agent.result_processing.csv_exporter import export_csv
from text_to_sql_agent.result_processing.visualization_hints import visualization_hint

from langchain_core.messages import ToolMessage

from text_to_sql_agent.sql_tools.sql_tools import (
    sql_check_tool,
    sql_exec_tool,
    HardTermination,
)

# ============================================================
# Generate SQL Node
# ============================================================

def generate_sql_node(agent):
    """
    Invoke the LLM to generate SQL from schema context + user query.
    Retry-aware and bounded.
    """
    def _node(state):
        messages = [
            SystemMessage(content=state.schema_context),
        ]

        if state.validation_error:
            messages.append(
                SystemMessage(
                    content=(
                        "The previous SQL query was invalid.\n"
                        f"Error: {state.validation_error}\n\n"
                        "Generate a corrected SQL query that fixes this issue."
                    )
                )
            )

        messages.append(
            HumanMessage(content=state.user_query)
        )

        response = agent.invoke(messages)

        sql = response.content.strip() if response and response.content else ""

        return {
            "sql_query": sql,
            "retry_count": state.retry_count + 1,
        }

    return RunnableLambda(_node)


# ============================================================
# Validate SQL Node
# ============================================================

def validate_sql(state):
    """
    Deterministically validate generated SQL.
    Raises HardTermination on failure.
    """
    check = sql_check_tool(state.sql_query)

    if check == "VALID":
        return {}

    raise HardTermination(check)


# ============================================================
# Execute SQL Node
# ============================================================

def execute_sql(state):
    """
    Execute validated SQL, normalize result, classify output,
    and attach visualization metadata.
    """
    raw_result = sql_exec_tool(state.sql_query)

    # --------------------------------------------------------
    # Normalize DB output → JSON-safe (row-level)
    # --------------------------------------------------------
    normalized = []

    if raw_result is not None:
        for row in raw_result:
            if isinstance(row, dict):
                normalized.append(row)
            elif hasattr(row, "_mapping"):
                normalized.append(dict(row._mapping))
            elif isinstance(row, (list, tuple)):
                normalized.append(list(row))
            else:
                normalized.append(str(row))

    # --------------------------------------------------------
    # Output classification
    # --------------------------------------------------------
    output_type = classify_output(normalized)

    # --------------------------------------------------------
    # Build structured response (NO rendering here)
    # --------------------------------------------------------
    response = {
        "type": output_type,
        "data": None,
        "visualization": visualization_hint(output_type),
    }

    if output_type == "scalar":
        # Single value (e.g. COUNT, SUM)
        response["data"] = (
            list(normalized[0].values())[0] if normalized else None
        )

    elif output_type == "table":
        response["data"] = format_table(normalized)
        response["csv"] = export_csv(normalized)

    elif output_type == "time_series":
        # Keep rows as-is; frontend decides charting
        response["data"] = normalized

    return {
        "final_answer": response
    }


# ============================================================
# Final Response Node
# ============================================================

def final_response_node(state):
    """
    Return final API response.
    This node should remain a thin pass-through.
    """
    return {
        "final_answer": state.final_answer
    }
