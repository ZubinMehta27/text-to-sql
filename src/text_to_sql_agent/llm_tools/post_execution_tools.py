"""
FUTURE WORK:
- Tool-based schema reasoning
- HITL support
- Query explanation layer

DO NOT IMPORT OR USE YET.
"""

from langchain import tools
from langchain.messages import AIMessage
from langchain_ollama import ChatOllama

@tools
def summarize_result_table(result_table: str) -> str:
    """
    Given a result table as a string, summarize its contents in a user-friendly manner.

    Args:
        result_table: Result table as a string.

    Returns:
        Summary of the result table as a string.
    """
    prompt = f"""
    Given the following result table:

    {result_table}

    Summarize its contents in a user-friendly manner.
    """

    pass