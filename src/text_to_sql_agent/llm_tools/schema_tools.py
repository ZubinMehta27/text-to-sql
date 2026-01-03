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
def find_relevant_tables(schema: str, question: str) -> str:
    """
    Given a database schema and a natural language question,
    return a comma-separated list of relevant table names.

    Args:
        schema: Database schema as a string.
        question: Natural language question.

    Returns:
        Comma-separated list of relevant table names.
    """
    prompt = f"""
    Given the following database schema:

    {schema}

    Identify the relevant tables for the following question:

    {question}

    Return a comma-separated list of table names only.
    """

    pass

@tools
def rank_candidate_joins(
    schema: str,
    question: str,
    candidate_joins: list[str],
) -> str:
    """
    Given a database schema, a natural language question, and a list of candidate join conditions,
    rank the join conditions based on their relevance to the question.

    Args:
        schema: Database schema as a string.
        question: Natural language question.
        candidate_joins: List of candidate join conditions as strings.

    Returns:
        Comma-separated list of ranked join conditions.
    """
    prompt = f"""
    Given the following database schema:

    {schema}

    And the following natural language question:

    {question}

    Rank the following candidate join conditions based on their relevance to the question:

    {', '.join(candidate_joins)}

    Return a comma-separated list of join conditions only, ordered from most to least relevant.
    """

    pass

@tools
def explain_schema_mapping(schema: str) -> str:
    """
    Given a database schema, provide a brief explanation of how the tables are related.

    Args:
        schema: Database schema as a string.

    Returns:
        Brief explanation of how the tables are related.
    """
    prompt = f"""
    Given the following database schema:

    {schema}

    Provide a brief explanation of how the tables are related.
    """

    pass