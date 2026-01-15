from fastapi import FastAPI
import logging
import sys

from text_to_sql_agent.schema_analysis import (
    build_schema_context,
    extract_schema_entities,
)
from text_to_sql_agent.runtime_bootstrap import TABLES, FOREIGN_KEYS
from text_to_sql_agent.config import settings
from text_to_sql_agent.models.models import ChatRequest
from text_to_sql_agent.agent import agent
from text_to_sql_agent.graph_build import build_graph
from text_to_sql_agent.state_initializer import build_initial_state
from text_to_sql_agent.runtime.execution_guard import safe_execute_graph

logging.basicConfig(
    level=settings.log_level,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
    force=True,
)

app = FastAPI()
graph = build_graph(agent)


@app.post("/chat")
def chat(request: ChatRequest):
    # ------------------------------------------------------------
    # Schema analysis (single source of truth)
    # ------------------------------------------------------------
    schema_context = build_schema_context(TABLES, FOREIGN_KEYS)

    # Derive schema entities deterministically
    schema_entities = extract_schema_entities(TABLES)

    # ------------------------------------------------------------
    # Proper state initialization (PASS LLM)
    # ------------------------------------------------------------
    state = build_initial_state(
        user_query=request.query,
        schema_context=schema_context,
        schema_entities=schema_entities,
        llm=agent,
    )

    response = safe_execute_graph(graph, state)

    api_response = {
        "answer": response["result"],
        "metadata": response["metadata"],
        "request_id": response["request_id"],
    }

    # --- surface additive fields ---
    if "post_execution_summary" in response:
        api_response["post_execution_summary"] = response["post_execution_summary"]

    if "invoked_tools" in response:
        api_response["invoked_tools"] = response["invoked_tools"]

    return api_response
