import polars as pl

from dataflux.models.dataset import DatasetInfo
from dataflux.models.search_result import SearchResult
from dataflux.providers.uci import UCIProvider


provider = UCIProvider()


# ============================================================================
# Search
# ============================================================================

def test_search():
    results = provider.search("iris")

    assert isinstance(results, list)
    assert len(results) > 0

    result = results[0]

    assert isinstance(result, SearchResult)
    assert result.provider == "uci"
    assert result.name == "Iris"


# ============================================================================
# Info
# ============================================================================

def test_info():
    results = provider.search("iris")

    info = provider.info(results[0].id)

    assert isinstance(info, DatasetInfo)

    assert info.provider == "uci"
    assert info.name == "Iris"

    assert info.instances > 0
    assert info.features > 0


# ============================================================================
# Pull
# ============================================================================

def test_pull():
    results = provider.search("iris")

    df = provider.pull(results[0].id)

    assert isinstance(df, pl.DataFrame)

    assert df.height > 0
    assert df.width > 0


# ============================================================================
# Schema
# ============================================================================

def test_schema():
    results = provider.search("iris")

    df = provider.pull(results[0].id)

    assert isinstance(df.schema, dict)
    assert len(df.schema) > 0


# ============================================================================
# Search Ranking
# ============================================================================

def test_search_returns_best_match():
    results = provider.search("iris")

    assert results[0].name.lower() == "iris"


# ============================================================================
# Case Insensitive Search
# ============================================================================

def test_case_insensitive_search():
    lower = provider.search("iris")
    upper = provider.search("IRIS")

    assert lower == upper