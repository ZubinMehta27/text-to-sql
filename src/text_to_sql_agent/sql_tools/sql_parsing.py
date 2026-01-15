from sqlglot import parse_one, exp

def extract_tables(sql: str) -> set[str]:
    """
    Extract table names from a SQL query.

    Args:
        sql: SQL string.

    Returns:
        Set of table names.
    """
    tree = parse_one(sql, read="sqlite")
    return {t.name.lower() for t in tree.find_all(exp.Table) if t.name}

