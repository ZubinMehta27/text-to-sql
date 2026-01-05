GROUPING_MARKERS = [
    "per ",
    "by ",
    "for each ",
    "grouped by ",
]

def has_grouping_intent(query: str) -> bool:
    q = query.lower()
    return any(marker in q for marker in GROUPING_MARKERS)


def resolve_grouping_entity(
    query: str,
    schema_entities: set[str],
) -> str | None:
    q = query.lower()

    for marker in GROUPING_MARKERS:
        if marker in q:
            fragment = q.split(marker, 1)[1]
            candidate = fragment.split()[0]

            if candidate in schema_entities:
                return candidate

    return None
