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
def suggest_sql_fixes(
    schema: str,
    question: str,
    invalid_sql: str,
    error_message: str,
) -> str:
    """
    Given a database schema, a natural language question, an invalid SQL query,
    and an error message, suggest fixes to the SQL query.

    Args:
        schema: Database schema as a string.
        question: Natural language question.
        invalid_sql: The invalid SQL query as a string.
        error_message: The error message from the failed SQL execution.

    Returns:
        Suggested fixed SQL query as a string.
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

    Suggest fixes to the SQL query to make it valid and aligned with the question.
    Provide only the corrected SQL query.
    """

    pass

@tools
def explain_why_query_failed(
    schema: str,
    question: str,
    invalid_sql: str,
    error_message: str,
) -> str:
    """
    Given a database schema, a natural language question, an invalid SQL query,
    and an error message, explain why the SQL query failed.

    Args:
        schema: Database schema as a string.
        question: Natural language question.
        invalid_sql: The invalid SQL query as a string.
        error_message: The error message from the failed SQL execution.

    Returns:
        Explanation of why the SQL query failed as a string.
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

    Explain why this SQL query failed.
    """

    pass

@tools
def rewrite_query_for_user(
    schema: str,
    question: str,
    invalid_sql: str,
    error_message: str,
) -> str:
    """
    Given a database schema, a natural language question, an invalid SQL query,
    and an error message, rewrite the SQL query to produce more user-friendly error messages.

    Args:
        schema: Database schema as a string.
        question: Natural language question.
        invalid_sql: The invalid SQL query as a string.
        error_message: The error message from the failed SQL execution.

    Returns:
        Rewritten SQL query as a string.
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

    Rewrite the SQL query to produce more user-friendly error messages.
    Provide only the rewritten SQL query.
    """

    pass

