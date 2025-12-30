import csv
import io
from typing import List, Dict, Any

def export_csv(result: List[Dict[str, Any]]) -> str:
    if not result:
        return ""

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=result[0].keys())
    writer.writeheader()
    writer.writerows(result)

    return output.getvalue()
