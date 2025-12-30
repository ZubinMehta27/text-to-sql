from langgraph.graph import StateGraph, END
from text_to_sql_agent.graph_state import GraphState
from text_to_sql_agent.graph_nodes import (
    generate_sql_node,
    validate_sql,
    execute_sql,
    final_response_node,
)

def build_graph(agent):
    """
    Build and compile the LangGraph execution graph.
    """
    graph = StateGraph(GraphState)

    graph.add_node("generate_sql", generate_sql_node(agent))
    graph.add_node("validate_sql", validate_sql)
    graph.add_node("execute_sql", execute_sql)
    graph.add_node("final_response", final_response_node)

    graph.set_entry_point("generate_sql")

    graph.add_edge("generate_sql", "validate_sql")
    graph.add_edge("validate_sql", "execute_sql")
    graph.add_edge("execute_sql", "final_response")
    graph.add_edge("final_response", END)

    return graph.compile()