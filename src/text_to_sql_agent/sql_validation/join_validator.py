from sqlglot import parse_one, exp
from collections import defaultdict

def extract_joins(sql: str):
    tree = parse_one(sql, read="sqlite")
    alias_map = extract_alias_map(tree)

    joins = []

    for join in tree.find_all(exp.Join):
        on = join.args.get("on")
        if not on or not isinstance(on, exp.EQ):
            continue

        left, right = on.left, on.right

        if isinstance(left, exp.Column) and isinstance(right, exp.Column):
            lt = alias_map.get(left.table.lower())
            rt = alias_map.get(right.table.lower())

            if not lt or not rt:
                continue

            joins.append((
                lt,
                left.name.lower(),
                rt,
                right.name.lower()
            ))

    return joins


# ============================================================
# Join Graph Builder
# ============================================================
def build_join_graph(foreign_keys: dict) -> dict[str, set[str]]:
    """
    Build an undirected table-level join graph.
    """
    graph = defaultdict(set)

    for table, fks in foreign_keys.items():
        for _, ref_table, _ in fks:
            graph[table].add(ref_table)
            graph[ref_table].add(table)

    return graph


# ============================================================
# Join Path Validator
# ===========================================================
def validate_join_paths(sql: str, foreign_keys: dict) -> bool:
    """
    Ensure all joined tables form a single connected path
    in the schema join graph.
    """
    joins = extract_joins(sql)

    if not joins:
        return True  # no joins → OK

    # Collect tables involved in joins
    tables = set()
    for lt, _, rt, _ in joins:
        tables.add(lt)
        tables.add(rt)

    graph = build_join_graph(foreign_keys)

    # Graph connectivity check (DFS)
    visited = set()
    stack = {next(iter(tables))}

    while stack:
        t = stack.pop()
        if t in visited:
            continue
        visited.add(t)
        stack |= graph[t] & tables

    return visited == tables


# ============================================================
# Join Validator
# ============================================================
def validate_joins(sql: str, foreign_keys: dict) -> bool:
    """
    Validate that all joins correspond to real foreign key relationships,
    regardless of direction, AND that they form a valid join path.
    """

    joins = extract_joins(sql)

    if not joins:
        return True  # no joins → nothing to validate

    # Build a bidirectional FK set
    fk_pairs = set()

    for table, fks in foreign_keys.items():
        for fk_col, ref_table, ref_col in fks:
            fk_pairs.add((table, fk_col, ref_table, ref_col))
            fk_pairs.add((ref_table, ref_col, table, fk_col))  # reverse direction

    # Validate each join uses real FK columns
    for lt, lc, rt, rc in joins:
        if (lt, lc, rt, rc) not in fk_pairs:
            return False

    # Validate join connectivity
    if not validate_join_paths(sql, foreign_keys):
        return False

    return True


def extract_alias_map(tree):
    """
    Build alias → table name mapping from FROM and JOIN clauses.
    """
    alias_map = {}

    for table in tree.find_all(exp.Table):
        table_name = table.name.lower()
        alias = table.alias

        if alias:
            alias_map[alias.lower()] = table_name
        else:
            alias_map[table_name] = table_name

    return alias_map
