from langchain_core.tools import tool
from text_to_sql_agent.sql_tools.sql_parsing import extract_tables
from text_to_sql_agent.sql_tools.sql_static_checks import sql_static_check

@tool
def extract_tables_tool(sql: str) -> list[str]:
    """Extract table names from SQL."""
    return list(extract_tables(sql))

@tool
def sql_static_check_tool(sql: str) -> str:
    """Validate SQL without touching the database."""
    return sql_static_check(sql)
