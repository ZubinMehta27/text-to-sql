from langchain_core.runnables import RunnableLambda
from langchain_core.messages import SystemMessage, HumanMessage

from text_to_sql_agent.result_processing.output_classifier import classify_output
from text_to_sql_agent.result_processing.table_formatter import format_table
from text_to_sql_agent.result_processing.csv_exporter import export_csv
from text_to_sql_agent.result_processing.visualization_hints import visualization_hint

from text_to_sql_agent.sql_tools.normalization import normalize_sql
from text_to_sql_agent.utils.load_markdown import load_markdown_content

from text_to_sql_agent.sql_tools.sql_tools import (
    sql_check_tool,
    sql_exec_tool,
)

from text_to_sql_agent.grounding.query_enricher import enrich_for_sql

from text_to_sql_agent.errors.error_formatter import format_error_message

from text_to_sql_agent.runtime_bootstrap import SCHEMA_FINGERPRINT

from text_to_sql_agent.retry.error_classifier import classify_sql_error

SYSTEM_PROMPT = load_markdown_content("prompts.md")

# ============================================================
# Generate SQL Node
# ============================================================


def generate_sql_node(agent):
    """
    Invoke the LLM to generate SQL from schema context + user query.
    Retry-aware, bounded, and deterministically grounded.
    """

    def _node(state):

        # ------------------------------------------------------------
        # HARD GATE: detect schema drift
        # ------------------------------------------------------------
        if state.schema_fingerprint != SCHEMA_FINGERPRINT:
            state.termination_reason = "schema_drift_detected"
            state.last_error_type = "terminal"
            state.last_error_message = "Database schema has changed since startup."
            return {}
        
        # ------------------------------------------------------------
        # HARD GATE: only run if router decided SQL is required
        # ------------------------------------------------------------
        if state.execution_mode != "SQL_REQUIRED":
            return {}

        # ------------------------------------------------------------
        # Ground the query deterministically
        # ------------------------------------------------------------
        grounded_prompt = enrich_for_sql(
            schema_context=state.schema_context,
            user_query=state.user_query,
            schema_entities=state.schema_entities,
            default_recent_limit=state.default_recent_limit,
            default_popular_limit=state.default_popular_limit,
        )

        messages = [
            # Strict SQL contract + grounded schema + query
            SystemMessage(
                content=f"{SYSTEM_PROMPT}\n\n{grounded_prompt}"
            )
        ]

        # ------------------------------------------------------------
        # Retry correction path (unchanged, but now grounded)
        # ------------------------------------------------------------
        if state.validation_error:
            messages.append(
                SystemMessage(
                    content=(
                        "The previous SQL query was invalid.\n"
                        f"Error: {state.validation_error}\n\n"
                        "Output ONLY a corrected SQL query starting with SELECT or WITH."
                    )
                )
            )

        # IMPORTANT: no raw user query anymore
        # messages.append(HumanMessage(content=state.user_query))

        response = agent.invoke(messages)

        sql = normalize_sql(response)

        return {
            "sql_query": sql,
            "validation_error": state.validation_error,
        }

    return RunnableLambda(_node)

# ============================================================
# Validate SQL Node
# ============================================================

def validate_sql(state):
    check = sql_check_tool(state.sql_query)

    if check == "VALID":
        return {
            "sql_valid": True,
            "validation_error": None,
        }

    # INVALID SQL → this is a retry attempt
    return {
        "sql_valid": False,
        "validation_error": check,
        "retry_count": state.retry_count + 1,
        "retry_reason": "retryable_sql_error",
    }



# ============================================================
# Execute SQL Node
# ============================================================

def execute_sql(state):
    """
    Execute validated SQL and return normalized execution result.
    NO formatting. NO visualization. NO final_answer.
    """

    raw_result = sql_exec_tool(state.sql_query)

    normalized = []

    if raw_result is not None:
        for row in raw_result:
            if isinstance(row, dict):
                normalized.append(row)
            elif hasattr(row, "_mapping"):
                normalized.append(dict(row._mapping))
            elif isinstance(row, (list, tuple)):
                normalized.append(dict(enumerate(row)))
            else:
                normalized.append({"value": str(row)})

    # --- Post-execution safety limit ---
    MAX_ROWS = 1000

    if len(normalized) > MAX_ROWS:
        state.termination_reason = "result_size_exceeded"
        state.last_error_type = "terminal"
        state.last_error_message = (
            f"Query returned more than {MAX_ROWS} rows."
        )
        return {
            "execution_result": None,
            "termination_reason": "result_size_exceeded",
            "last_error_type": "terminal",
            "last_error_message": f"Query returned more than {MAX_ROWS} rows.",
        }

    return {
        "execution_result": normalized
    }

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
        response["data"] = (
            list(normalized[0].values())[0] if normalized else None
        )

    elif output_type == "table":
        response["data"] = format_table(normalized)
        response["csv"] = export_csv(normalized)

    elif output_type == "time_series":
        response["data"] = normalized

    return {
        "final_answer": response,
    }


# ============================================================
# Final Response Node
# ============================================================

def final_response_node(state):
    """
    Return final API response.
    Deterministically formats output based on execution result shape.
    """
    # Explicit NON-SQL handling
    if state.execution_mode == "NON_SQL_RESPONSE":
        return {
            "final_answer": {
                "type": "error",
                "message": (
                    "This question cannot be answered using the available database schema. "
                    "Please rephrase the question using measurable concepts like sales, revenue, or counts."
                )
            }
        }

    # ------------------------------------------------------------
    # Case 1: Successful execution
    # ------------------------------------------------------------
    if state.sql_valid and state.execution_result is not None:
        output_type = classify_output(state.execution_result)

        # Scalar
        if output_type == "scalar":
            value = list(state.execution_result[0].values())[0]
            return {
                "final_answer": {
                    "type": "scalar",
                    "data": value,
                }
            }

        # List
        if output_type == "list":
            values = [
                list(row.values())[0]
                for row in state.execution_result
            ]
            return {
                "final_answer": {
                    "type": "list",
                    "data": values,
                }
            }

        # Time series
        if output_type == "time_series":
            return {
                "final_answer": {
                    "type": "time_series",
                    "data": state.execution_result,
                }
            }

        # Table (default)
        return {
            "final_answer": {
                "type": "table",
                "data": state.execution_result,
            }
        }

    # ------------------------------------------------------------
    # Case 2: Failure → formatted, user-facing error (UPDATED)
    # ------------------------------------------------------------
    return {
        "final_answer": format_error_message(state.validation_error)
    }

# --- Post-execution tool hook (disabled by default) ---
# Example:
# state.invoked_tools.append({
#     "tool": "summarize_result_table",
#     "status": "skipped",
#     "reason": "not enabled"
# })
