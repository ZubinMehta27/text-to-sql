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
def request_user_clarification(
    schema: str,
    question: str,
    invalid_sql: str,
    error_message: str,
) -> str:
    """
    Given a database schema, a natural language question, an invalid SQL query,
    and an error message, generate a clarification question to ask the user.

    Args:
        schema: Database schema as a string.
        question: Natural language question.
        invalid_sql: The invalid SQL query as a string.
        error_message: The error message from the failed SQL execution.

    Returns:
        Clarification question as a string.
    """
    prompt = f"""
    Given the following database schema:

    {schema}

    And the following natural language question:

    {question}

    The following SQL query is invalid:

    {invalid_sql}

    The error message from executing this SQL is:

    {error_message}

    Generate a clarification question to ask the user to help fix the SQL query.
    """

    pass
