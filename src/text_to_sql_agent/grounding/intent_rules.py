def requires_sql(query: str) -> bool:
    q = query.lower()

    explicit_sql_terms = [
        "total", "sum", "count", "average", "avg",
        "maximum", "minimum", "max", "min",
        "list", "show", "give me",
    ]

    implicit_aggregation_terms = [
        "how much",
        "overall",
        "in total",
        "amount",
        "revenue",
        "sales",
    ]

    grouping_terms = [
        " per ",
        " by ",
        " for each ",
    ]

    ranking_terms = [
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
    ]

    temporal_terms = [
        "recent",
        "latest",
        "newest",
        "oldest",
        "earliest",
        "last",
        "past",
        "previous",
        "recently",
    ]

    return any(
        term in q
        for term in (
            explicit_sql_terms
            + implicit_aggregation_terms
            + grouping_terms
            + ranking_terms
            + temporal_terms
        )
    )
