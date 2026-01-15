from langgraph.graph import StateGraph, END
from text_to_sql_agent.graph_state import GraphState

from text_to_sql_agent.grounding.grounding_router import routing_node
from text_to_sql_agent.graph_nodes import (
    generate_sql_node,
    repair_sql_node,
    validate_sql,
    execute_sql,
    final_response_node,
)
from text_to_sql_agent.graph_policy import retry_decision


def build_graph(agent):
    """
    Build and compile the LangGraph execution graph
    with bounded retry, repair, and HITL logic.
    """

    graph = StateGraph(GraphState)

    # ------------------------------------------------------------
    # Nodes
    # ------------------------------------------------------------
    graph.add_node("route", routing_node())
    graph.add_node("generate_sql", generate_sql_node(agent))
    graph.add_node("validate_sql", validate_sql)
    graph.add_node("repair_sql", repair_sql_node)
    graph.add_node("execute_sql", execute_sql)
    graph.add_node("final_response", final_response_node)

    # ------------------------------------------------------------
    # Entry point
    # ------------------------------------------------------------
    graph.set_entry_point("route")

    # ------------------------------------------------------------
    # Initial routing (SQL vs NON-SQL)
    # ------------------------------------------------------------
    graph.add_conditional_edges(
        "route",
        lambda state: state.execution_mode,
        {
            "SQL_REQUIRED": "generate_sql",
            "NON_SQL_RESPONSE": "final_response",
        },
    )

    # ------------------------------------------------------------
    # SQL generation & validation flow
    # ------------------------------------------------------------
    graph.add_edge("generate_sql", "validate_sql")

    # ------------------------------------------------------------
    # Validation decision (SINGLE authority)
    # ------------------------------------------------------------
    graph.add_conditional_edges(
        "validate_sql",
        retry_decision,
        {
            "execute_sql": "execute_sql",
            "repair_sql": "repair_sql",
            "generate_sql": "generate_sql",
            "final_response": "final_response",
        },
    )

    # ------------------------------------------------------------
    # Repair loop
    # ------------------------------------------------------------
    graph.add_edge("repair_sql", "validate_sql")

    # ------------------------------------------------------------
    # Terminal paths
    # ------------------------------------------------------------
    graph.add_edge("execute_sql", "final_response")
    graph.add_edge("final_response", END)

    return graph.compile()


__all__ = ["build_graph"]
