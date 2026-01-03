def normalize_sql(output) -> str:
    """
    Normalize LLM output into raw SQL suitable for validation.

    This removes transport artifacts without weakening safety.
    """
    if output is None:
        return ""

    # LangChain AIMessage
    if hasattr(output, "content"):
        sql = output.content
    else:
        sql = str(output)

    if not isinstance(sql, str):
        sql = str(sql)

    # Remove invisible junk that breaks validators
    sql = sql.strip()
    sql = sql.lstrip("\ufeff")  # BOM
    sql = sql.lstrip()

    return sql
