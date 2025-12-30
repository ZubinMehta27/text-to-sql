from typing import List, Dict, Any

def format_table(result: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not result:
        return {
            "columns": [],
            "rows": []
        }

    columns = list(result[0].keys())
    rows = [[row[col] for col in columns] for row in result]

    return {
        "columns": columns,
        "rows": rows
    }
