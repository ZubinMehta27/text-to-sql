from langchain_core.runnables import RunnableLambda
from langchain_core.messages import SystemMessage, HumanMessage

from text_to_sql_agent.result_processing.output_classifier import classify_output
from text_to_sql_agent.sql_tools.normalization import normalize_sql
from text_to_sql_agent.tools.hitl_tools import request_user_clarification
from text_to_sql_agent.tools.query_repair_tools import repair_sql_query
from text_to_sql_agent.utils.load_markdown import load_markdown_content

from text_to_sql_agent.sql_tools.sql_tools import (
    sql_check_tool,
    sql_exec_tool,
)

from text_to_sql_agent.sql_tools.sql_tools import HardTermination
from text_to_sql_agent.sql_tools.sql_parsing import extract_tables

from text_to_sql_agent.grounding.query_enricher import enrich_for_sql
from text_to_sql_agent.errors.error_formatter import format_error_message
from text_to_sql_agent.runtime_bootstrap import SCHEMA_FINGERPRINT

from text_to_sql_agent.tools.post_execution_tools import summarize_result_table


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
            SystemMessage(content=f"{SYSTEM_PROMPT}\n\n{grounded_prompt}")
        ]

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

    return {
        "sql_valid": False,
        "validation_error": check,
        "retry_count": state.retry_count + 1,
        "retry_reason": "retryable_sql_error",
    }

# ============================================================
# Repair SQL Node
# ============================================================
def repair_sql_node(state):
    """
    Attempt to repair an invalid SQL query using LLM guidance.
    """

    if not state.validation_error:
        return {}

    if state.retry_count >= state.max_retries:
        return {}

    try:
        original_sql = state.sql_query
        validation_error = state.validation_error

        repair_prompt = repair_sql_query.invoke(
            {
                "context": (
                    f"User query: {state.user_query}\n\n"
                    f"Previous SQL:\n{original_sql}\n\n"
                    f"Validation error:\n{validation_error}\n\n"
                    f"Schema context:\n{state.schema_context}"
                )
            }
        )

        repaired_sql = state.llm.invoke([
            HumanMessage(content=repair_prompt)
        ]).content

        normalized_sql = normalize_sql(repaired_sql)

        # ------------------------------------------------------------
        # RICH OBSERVABILITY FOR QUERY REPAIR
        # ------------------------------------------------------------
        state.invoked_tools.append({
            "tool": "repair_sql_query",
            "success": True,
            "reason": "query_repair",
            "repair_details": {
                "error": validation_error,
                "before_sql": original_sql,
                "after_sql": normalized_sql,
            },
        })

        return {
            "sql_query": normalized_sql,
            "validation_error": None,
        }

    except Exception as e:
        state.invoked_tools.append({
            "tool": "repair_sql_query",
            "success": False,
            "reason": "query_repair",
            "error": str(e),
        })
        return {}

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

    # ------------------------------------------------------------
    # Post-execution safety limit
    # ------------------------------------------------------------
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

# ============================================================
# Final Response Node
# ============================================================

def final_response_node(state):
    """
    Return final API response.
    Deterministically formats output based on execution result shape.
    """

    # ------------------------------------------------------------
    # NON-SQL handling → HITL FIRST, error only as fallback
    # ------------------------------------------------------------
    if state.execution_mode == "NON_SQL_RESPONSE":
        try:
            if not hasattr(state, "llm"):
                raise RuntimeError("LLM not available for HITL")

            clarification_prompt = request_user_clarification.invoke(
                {
                    "context": (
                        f"User query: {state.user_query}\n"
                        f"Validation error: {state.validation_error or 'N/A'}"
                    )
                }
            )

            question = state.llm.invoke([
                HumanMessage(content=clarification_prompt)
            ]).content or ""

            return {
                "final_answer": {
                    "type": "clarification_required",
                    "question": question,
                    "reason": "non_sql_ambiguous",
                },
                "hitl_context": {
                    "original_query": state.user_query,
                    "clarification_reason": "non_sql_ambiguous",
                },
                "invoked_tools": [
                    {
                        "tool": "request_user_clarification",
                        "success": True,
                        "reason": "hitl",
                    }
                ],
            }

        except Exception:
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

        # --------------------------------------------------------
        # LLM-driven post-execution summary (NON-DETERMINISTIC)
        # --------------------------------------------------------
        post_summary = None
        invoked = list(state.invoked_tools)

        try:
            if not hasattr(state, "llm"):
                raise RuntimeError("LLM not available in graph state")

            summary_prompt = summarize_result_table.invoke(
                {"rows": state.execution_result}
            )

            post_summary = state.llm.invoke([
                HumanMessage(content=summary_prompt)
            ]).content or ""

            invoked.append({
                "tool": "summarize_result_table",
                "success": True,
                "reason": "post_execution_summary",
            })

        except Exception as e:
            invoked.append({
                "tool": "summarize_result_table",
                "success": False,
                "reason": "post_execution_summary",
                "error": str(e),
            })

        # --------------------------------------------------------
        # Deterministic output formatting
        # --------------------------------------------------------

        if output_type == "scalar":
            value = list(state.execution_result[0].values())[0]
            return {
                "final_answer": {
                    "type": "scalar",
                    "data": value,
                    "summary": post_summary,
                },
                "invoked_tools": invoked,
            }

        if output_type == "list":
            values = [
                list(row.values())[0]
                for row in state.execution_result
            ]
            return {
                "final_answer": {
                    "type": "list",
                    "data": values,
                    "summary": post_summary,
                },
                "invoked_tools": invoked,
            }

        if output_type == "time_series":
            return {
                "final_answer": {
                    "type": "time_series",
                    "data": state.execution_result,
                    "summary": post_summary,
                },
                "invoked_tools": invoked,
            }

        return {
            "final_answer": {
                "type": "table",
                "data": state.execution_result,
                "summary": post_summary,
            },
            "invoked_tools": invoked,
        }

    # ------------------------------------------------------------
    # Case 2: Other failures → HITL attempt, then error
    # ------------------------------------------------------------
    try:
        if not hasattr(state, "llm"):
            raise RuntimeError("LLM not available for HITL")

        llm_with_tools = state.llm.bind_tools([request_user_clarification])

        tool_response = llm_with_tools.invoke([
            HumanMessage(
                content=(
                    "The system could not answer the user's query safely.\n\n"
                    f"User query: {state.user_query}\n"
                    f"Validation error: {state.validation_error}\n\n"
                    "Ask the user a clarification question."
                )
            )
        ])

        question = (
            tool_response.tool_calls[0].get("output")
            if tool_response.tool_calls
            else tool_response.content
        )

        return {
            "final_answer": {
                "type": "clarification_required",
                "question": question,
                "reason": "ambiguous_query",
            }
        }

    except Exception:
        return {
            "final_answer": format_error_message(state.validation_error)
        }