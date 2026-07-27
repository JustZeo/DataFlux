from dataflux.models.search_result import SearchResult


def test_search_result_creation():
    result = SearchResult(
        id="iris",
        name="Iris",
        provider="sklearn",
        description="Classic Iris dataset.",
        relevance=100,
    )

    assert result.id == "iris"
    assert result.name == "Iris"
    assert result.provider == "sklearn"
    assert result.description == "Classic Iris dataset."
    assert result.relevance == 100


def test_search_result_defaults():
    result = SearchResult(
        id="iris",
        name="Iris",
        provider="sklearn",
    )

    assert result.description is None
    assert result.relevance == 0