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

    # Measurable / value-bearing concepts
    measurable_terms = [
        "price",
        "amount",
        "total",
        "revenue",
        "sales",
        "count",
        "quantity",
        "number",
        "duration",
        "length",
        "time",
    ]

    has_sql_signal = any(
        term in q
        for term in (
            explicit_sql_terms
            + implicit_aggregation_terms
            + grouping_terms
            + temporal_terms
        )
    )

    has_ranking = any(term in q for term in ranking_terms)
    has_measure = any(term in q for term in measurable_terms)

    # Core rule:
    # - SQL if clear aggregation / grouping / temporal intent
    # - OR ranking *with* a measurable concept
    return has_sql_signal or (has_ranking and has_measure)
