from text_to_sql_agent.db import engine
from text_to_sql_agent.schema_analysis import (
    analyze_schema,
    infer_fact_and_dimension_tables,
)

import hashlib
import json

TABLES, FOREIGN_KEYS = analyze_schema(engine)
FACT_TABLES, DIM_TABLES = infer_fact_and_dimension_tables(TABLES, FOREIGN_KEYS)

def compute_schema_fingerprint(tables, foreign_keys) -> str:
    payload = {
        "tables": {
            t: sorted(list(meta["columns"]))
            for t, meta in tables.items()
        },
        "foreign_keys": foreign_keys,
    }
    raw = json.dumps(payload, sort_keys=True)
    return hashlib.sha256(raw.encode()).hexdigest()

SCHEMA_FINGERPRINT = compute_schema_fingerprint(TABLES, FOREIGN_KEYS)
