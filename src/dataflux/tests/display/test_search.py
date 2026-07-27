from dataflux.display.search import display_search
from dataflux.models.search_result import SearchResult


# ============================================================================
# Empty Results
# ============================================================================

def test_empty_results():
    display_search([], limit=10)


# ============================================================================
# Single Result
# ============================================================================

def test_single_result():
    results = [
        SearchResult(
            id="iris",
            name="Iris",
            provider="sklearn",
            description="Classic iris flower dataset.",
            relevance=100,
        )
    ]

    display_search(results, limit=10)


# ============================================================================
# Multiple Results
# ============================================================================

def test_multiple_results():
    results = [
        SearchResult(
            id=f"dataset_{i}",
            name=f"Dataset {i}",
            provider="sklearn",
            description=f"Description {i}",
            relevance=100 - i,
        )
        for i in range(20)
    ]

    display_search(results, limit=10)


# ============================================================================
# Limit Larger Than Results
# ============================================================================

def test_large_limit():
    results = [
        SearchResult(
            id="iris",
            name="Iris",
            provider="sklearn",
            description="Dataset",
            relevance=100,
        )
    ]

    display_search(results, limit=100)


# ============================================================================
# No Description
# ============================================================================

def test_missing_description():
    results = [
        SearchResult(
            id="iris",
            name="Iris",
            provider="sklearn",
            description=None,
            relevance=100,
        )
    ]

    display_search(results, limit=10)