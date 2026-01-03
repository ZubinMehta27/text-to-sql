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

@tools
def present_query_preview(
    schema: str,
    question: str,
    sql: str,
) -> str:
    """
    Given a database schema, a natural language question, and a SQL query,
    generate a preview description of what the SQL query will return.

    Args:
        schema: Database schema as a string.
        question: Natural language question.
        sql: The SQL query as a string.

    Returns:
        Preview description as a string.
    """
    prompt = f"""
    Given the following database schema:

    {schema}

    And the following natural language question:

    {question}

    The following SQL query is proposed:

    {sql}

    Generate a brief preview description of what this SQL query will return.
    """

    pass

@tools
def approve_or_reject(
    schema: str,
    question: str,
    sql: str,
) -> str:
    """
    Given a database schema, a natural language question, and a SQL query,
    generate an approval or rejection message.

    Args:
        schema: Database schema as a string.
        question: Natural language question.
        sql: The SQL query as a string.

    Returns:
        Approval or rejection message as a string.
    """
    prompt = f"""
    Given the following database schema:

    {schema}

    And the following natural language question:

    {question}

    The following SQL query is proposed:

    {sql}

    Generate an approval or rejection message.
    """

    pass