from text_to_sql_agent.grounding.grouping import (
    has_grouping_intent,
    resolve_grouping_entity,
)

# ============================================================
# Global ranking / popularity enrichment
def ranking_hint(query: str) -> str:
    q = query.lower()
    hints = []

    if "popular" in q:
        hints.append(
            "The term 'popular' means highest frequency of occurrence.\n"
            "You MUST use an aggregate COUNT to measure popularity.\n"
        )

    if "purchased" in q or "sold" in q:
        hints.append(
            "The term 'purchased' or 'sold' means total quantity.\n"
            "You MUST use SUM(quantity) to measure this.\n"
        )

    if "most" in q or "top" in q:
        hints.append(
            "The term 'most' or 'top' means ORDER BY the aggregate in DESCENDING order.\n"
            "You MUST apply ORDER BY ... DESC and LIMIT the result appropriately.\n"
        )

    if "least" in q:
        hints.append(
            "The term 'least' means ORDER BY the aggregate in ASCENDING order.\n"
            "You MUST apply ORDER BY ... ASC.\n"
        )

    if "recent" in q or "latest" in q:
        hints.append(
            "The term 'recent' or 'latest' means most recent by time.\n"
            "You MUST ORDER BY a date or timestamp column in DESCENDING order.\n"
        )

    return "\n".join(hints)

def has_ranking_intent(query: str) -> bool:
    q = query.lower()
    return any(term in q for term in [
        "most",
        "least",
        "top",
        "bottom",
        "highest",
        "lowest",
        "best",
        "worst",
        "popular",
        "unpopular",
    ])

# ============================================================
# Main enrichment function
def enrich_for_sql(
    schema_context: str,
    schema_entities: set[str],
    user_query: str,
    default_recent_limit: int | None = None,
    default_popular_limit: int | None = None,
) -> str:
    grouping_hint = ""

    # ------------------------------------------------------------
    # GROUP BY enrichment
    # ------------------------------------------------------------
    if has_grouping_intent(user_query):
        entity = resolve_grouping_entity(user_query, schema_entities)

        if entity:
            grouping_hint = (
                f"\nThe query requires aggregation grouped by `{entity}`.\n"
                f"You MUST include GROUP BY {entity}.\n"
            )
        else:
            grouping_hint = (
                "\nThe query requests grouped aggregation, "
                "but the grouping target could not be resolved from the schema.\n"
                "Do NOT guess.\n"
            )

    # ------------------------------------------------------------
    # Ranking / popularity enrichment (semantic meaning)
    # ------------------------------------------------------------
    ranking_enrichment = ranking_hint(user_query)

    # ------------------------------------------------------------
    # Temporal / recency enrichment (LIMIT policy)
    # ------------------------------------------------------------
    temporal_enrichment = ""

    if default_recent_limit is not None and has_temporal_intent(user_query):
        temporal_enrichment = (
            "\nThe query requests recent or time-ordered records.\n"
            f"If no explicit limit is specified, you MUST include "
            f"LIMIT {default_recent_limit}.\n"
        )

    # ------------------------------------------------------------
    # Ranking / popularity LIMIT policy (NEW)
    # ------------------------------------------------------------
    ranking_limit_enrichment = ""

    if (
        default_popular_limit is not None
        and has_ranking_intent(user_query)
    ):
        ranking_limit_enrichment = (
            "\nThe query requests ranked results.\n"
            f"If no explicit limit is specified, you MUST include "
            f"LIMIT {default_popular_limit}.\n"
        )

    return f"""
You must generate a SQL query using the schema below.
Only SELECT or WITH queries are allowed.
Do NOT answer in natural language.

{grouping_hint}
{ranking_enrichment}
{temporal_enrichment}
{ranking_limit_enrichment}

Schema:
{schema_context}

Question:
{user_query}
"""

# ============================================================
# Temporal intent detection
def has_temporal_intent(query: str) -> bool:
    q = query.lower()
    return any(term in q for term in [
        "recent",
        "latest",
        "newest",
        "oldest",
        "earliest",
        "last",
    ])
