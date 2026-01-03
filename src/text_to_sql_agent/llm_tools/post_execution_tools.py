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

@tools
def detect_value_mismatchs(
    schema: str,
    question: str,
    sql: str,
    result_table: str,
) -> str:
    """
    Given a database schema, a natural language question, a SQL query, and its result table,
    detect if there are any value mismatches between the expected answer and the actual results.

    Args:
        schema: Database schema as a string.
        question: Natural language question.
        sql: SQL query as a string.
        result_table: Result table as a string.

    Returns:
        Description of any detected value mismatches as a string.
    """
    prompt = f"""
    Given the following database schema:

    {schema}

    And the following natural language question:

    {question}

    The executed SQL query is:

    {sql}

    The resulting table is:

    {result_table}

    Detect if there are any value mismatches between the expected answer and the actual results.
    """

    pass

@tools
def format_tabular_response(result_table: str) -> str:
    """
    Given a result table as a string, format it into a well-structured tabular representation.

    Args:
        result_table: Result table as a string.

    Returns:
        Formatted result table as a string.
    """
    prompt = f"""
    Given the following result table:

    {result_table}

    Format it into a well-structured tabular representation.
    """

    pass