from text_to_sql_agent.sql_tools.sql_parsing import extract_tables
from text_to_sql_agent.runtime_bootstrap import FOREIGN_KEYS
from text_to_sql_agent.sql_validation.join_validator import validate_joins

def sql_static_check(sql: str) -> str:
    if not sql:
        return "INVALID: Empty query."

    normalized = sql.strip().lower()

    if not normalized.startswith(("select", "with")):
        return "INVALID: Only SELECT or WITH queries are allowed."

    if "--" in normalized or "/*" in normalized:
        return "INVALID: SQL comments are not allowed."

    try:
        extract_tables(sql)
    except Exception:
        return "INVALID: Failed to parse SQL."

    try:
        if " join " in normalized and not validate_joins(sql, FOREIGN_KEYS):
            return "INVALID: Join condition does not match schema foreign keys."
    except Exception:
        return "INVALID: Failed to validate join conditions."

    return "VALID"