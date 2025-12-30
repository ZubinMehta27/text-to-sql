import logging
import sys
from fastapi import FastAPI

from text_to_sql_agent.schema_analysis import build_schema_context
from text_to_sql_agent.runtime_bootstrap import TABLES, FOREIGN_KEYS

from text_to_sql_agent.config import settings
from text_to_sql_agent.models.models import ChatRequest
from text_to_sql_agent.agent import agent
from text_to_sql_agent.execution_graph import build_graph
from text_to_sql_agent.graph_state import GraphState
from text_to_sql_agent.sql_tools import HardTermination

"""
FastAPI entrypoint for the Text-to-SQL service.
"""

logging.basicConfig(
    level=settings.log_level,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
    force=True,
)

app = FastAPI()
graph = build_graph(agent)

@app.get("/")
def index():
    """
    Health check endpoint.
    """
    return {"message": "Welcome to the Text-to-SQL Chatbot!"}

@app.post("/chat")
def chat(request: ChatRequest):
    try:
        # 🔑 BUILD SCHEMA CONTEXT HERE
        schema_context = build_schema_context(TABLES, FOREIGN_KEYS)

        state = GraphState(
            user_query=request.query,
            schema_context=schema_context
        )

        final_state = graph.invoke(state)

        return {
            "answer": final_state.get("final_answer")
        }

    except HardTermination:
        return {
            "answer": "It is not possible to answer this question using the available schema."
        }
