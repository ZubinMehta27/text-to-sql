from langchain.tools import tool

@tool
def repair_sql_query(context: str) -> str:
    """
    Repair a failed SQL query without changing user intent.

    Rules:
    - Output ONLY a valid SQL query
    - Do NOT explain
    - Do NOT invent tables or columns
    - Preserve original intent
    """

    return (
        "You are a SQL expert fixing a broken query.\n\n"
        "Given the context below, return ONLY a corrected SQL query.\n\n"
        "Rules:\n"
        "- Do not explain\n"
        "- Do not use markdown\n"
        "- Do not invent schema\n"
        "- Preserve the original intent\n"
        "- Start with SELECT or WITH\n\n"
        f"Context:\n{context}"
    )
