from text_to_sql_agent.db import engine
from text_to_sql_agent.schema_analysis import (
    analyze_schema,
    infer_fact_and_dimension_tables,
)

TABLES, FOREIGN_KEYS = analyze_schema(engine)
FACT_TABLES, DIM_TABLES = infer_fact_and_dimension_tables(TABLES, FOREIGN_KEYS)