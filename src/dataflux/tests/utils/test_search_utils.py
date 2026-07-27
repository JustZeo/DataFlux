from dataflux.models.search_result import SearchResult
from dataflux.utils.search import (
    PROVIDER_PRIORITY,
    rank,
    search_score,
)


# ============================================================================
# search_score()
# ============================================================================

def test_exact_match():
    assert search_score("iris", "iris") == 2


def test_exact_word_inside_text():
    assert search_score(
        "iris",
        "classic iris dataset",
    ) == 2


def test_partial_match():
    assert search_score(
        "iris",
        "irisdataset",
    ) == 1


def test_no_match():
    assert search_score(
        "iris",
        "wine quality",
    ) == -1


def test_case_insensitive():
    assert (
        search_score("IRIS", "iris")
        == search_score("iris", "IRIS")
        == 2
    )


def test_multiple_texts():
    assert search_score(
        "iris",
        None,
        "",
        "wine",
        "iris dataset",
    ) == 2


# ============================================================================
# rank()
# ============================================================================

def test_rank_exact_match_first():
    results = [
        SearchResult(
            id="1",
            name="Wine",
            provider="uci",
            relevance=1,
        ),
        SearchResult(
            id="2",
            name="Iris",
            provider="sklearn",
            relevance=2,
        ),
    ]

    ranked = rank(results)

    assert ranked[0].name == "Iris"


def test_provider_priority():
    results = [
        SearchResult(
            id="1",
            name="Dataset",
            provider="kaggle",
            relevance=1,
        ),
        SearchResult(
            id="2",
            name="Dataset",
            provider="sklearn",
            relevance=1,
        ),
    ]

    ranked = rank(results)

    assert ranked[0].provider == "sklearn"


def test_documentation_bonus():
    results = [
        SearchResult(
            id="1",
            name="Dataset",
            provider="uci",
            relevance=1,
            description=None,
        ),
        SearchResult(
            id="2",
            name="Dataset",
            provider="uci",
            relevance=1,
            description="A documented dataset.",
        ),
    ]

    ranked = rank(results)

    assert ranked[0].description is not None


def test_name_sorting():
    results = [
        SearchResult(
            id="1",
            name="Zoo",
            provider="uci",
            relevance=1,
        ),
        SearchResult(
            id="2",
            name="Apple",
            provider="uci",
            relevance=1,
        ),
    ]

    ranked = rank(results)

    assert ranked[0].name == "Zoo"


# ============================================================================
# Provider Priority
# ============================================================================

def test_provider_priority_values():
    assert PROVIDER_PRIORITY["sklearn"] > PROVIDER_PRIORITY["kaggle"]
    assert PROVIDER_PRIORITY["uci"] > PROVIDER_PRIORITY["worldbank"]