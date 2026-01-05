from sqlalchemy import text
from collections import defaultdict

def analyze_schema(engine):
    """
    Introspect the database schema.

    Args:
        engine: SQLAlchemy engine.

    Returns:
        tables: Mapping of table -> columns and primary keys.
        foreign_keys: Mapping of table -> foreign key relationships.
    """
    tables = {}
    foreign_keys = defaultdict(list)

    with engine.connect() as conn:
        table_rows = conn.execute(text("""
            SELECT name
            FROM sqlite_master
            WHERE type='table'
              AND name NOT LIKE 'sqlite_%'
        """)).fetchall()

        for (table_name,) in table_rows:
            tables[table_name.lower()] = {
                "columns": set(),
                "primary_keys": set(),
            }

            cols = conn.execute(
                text(f'PRAGMA table_info("{table_name}")')
            ).fetchall()

            for col in cols:
                col_name = col[1].lower()
                tables[table_name.lower()]["columns"].add(col_name)
                if col[5] == 1:
                    tables[table_name.lower()]["primary_keys"].add(col_name)

            fks = conn.execute(
                text(f'PRAGMA foreign_key_list("{table_name}")')
            ).fetchall()

            for fk in fks:
                foreign_keys[table_name.lower()].append(
                    (fk[3].lower(), fk[2].lower(), fk[4].lower())
                )

    return tables, foreign_keys

def extract_schema_entities(tables: dict) -> set[str]:
    """
    Extract valid schema entities for grouping / grounding.

    Entities include:
    - table names
    - singularized table names
    - human-readable (non-ID) columns
    """
    entities = set()

    for table, meta in tables.items():
        table_lc = table.lower()

        # table name
        entities.add(table_lc)

        # naive singularization: albums -> album
        if table_lc.endswith("s") and len(table_lc) > 1:
            entities.add(table_lc[:-1])

        # column-based entities
        for col in meta.get("columns", []):
            col_lc = col.lower()

            # exclude technical columns
            if col_lc.endswith("id"):
                continue

            entities.add(col_lc)

    return entities

def infer_fact_and_dimension_tables(tables, foreign_keys):
    """
    Infer FACT and DIMENSION tables using foreign key presence.

    Args:
        tables: Table metadata.
        foreign_keys: Foreign key mapping.

    Returns:
        fact_tables: Tables treated as FACT tables.
        dimension_tables: Tables treated as DIMENSION tables.
    """
    fact_tables = set()
    dimension_tables = set()

    for table in tables:
        if foreign_keys.get(table):
            fact_tables.add(table)
        else:
            dimension_tables.add(table)

    return fact_tables, dimension_tables

def build_schema_context(tables: dict, foreign_keys: dict) -> str:
    """
    Build a deterministic schema description string for LLM grounding.
    """

    lines = ["Database schema:"]

    for table, meta in tables.items():
        cols = ", ".join(sorted(meta.get("columns", [])))
        lines.append(f"- {table}({cols})")

    if foreign_keys:
        lines.append("")
        lines.append("Foreign keys:")
        for table, fks in foreign_keys.items():
            for fk_col, ref_table, ref_col in fks:
                lines.append(f"- {table}.{fk_col} -> {ref_table}.{ref_col}")

    return "\n".join(lines)
