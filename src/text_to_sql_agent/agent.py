from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage
from text_to_sql_agent.utils.load_markdown import load_markdown_content

from text_to_sql_agent.llm_tools.llm_tools import (
    extract_tables_tool,
    sql_static_check_tool,
)

"""
LLM configuration for SQL generation.
"""

agent = ChatOllama(
    model="llama3.1:latest",
    temperature=0.0,
).bind_tools([
    extract_tables_tool,
    sql_static_check_tool,
])

SYSTEM_PROMPT = load_markdown_content("prompts.md")

def invoke_agent(llm, schema_context, user_query):
    return llm.invoke([
        SystemMessage(content=f"{SYSTEM_PROMPT}\n\n{schema_context}"),
        HumanMessage(content=user_query)
    ])
