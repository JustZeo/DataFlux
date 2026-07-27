import polars as pl

from dataflux.models.dataset import DatasetInfo
from dataflux.models.search_result import SearchResult
from dataflux.providers.statsmodels import StatsModelsProvider


provider = StatsModelsProvider()


# ============================================================================
# Search
# ============================================================================

def test_search():
    results = provider.search("longley")

    assert isinstance(results, list)
    assert len(results) > 0

    result = results[0]

    assert isinstance(result, SearchResult)
    assert result.provider == "statsmodels"
    assert result.id == "longley"
    assert result.name == "Longley"


# ============================================================================
# Info
# ============================================================================

def test_info():
    info = provider.info("longley")

    assert isinstance(info, DatasetInfo)

    assert info.id == "longley"
    assert info.name == "Longley"

    assert info.instances > 0
    assert info.features > 0

    assert info.provider == "statsmodels"


# ============================================================================
# Pull
# ============================================================================

def test_pull():
    df = provider.pull("longley")

    assert isinstance(df, pl.DataFrame)

    assert df.height > 0
    assert df.width > 0


# ============================================================================
# Schema
# ============================================================================

def test_schema():
    df = provider.pull("longley")

    assert isinstance(df.schema, dict)
    assert len(df.schema) > 0


# ============================================================================
# Search Ranking
# ============================================================================

def test_search_returns_best_match():
    results = provider.search("longley")

    assert results[0].id == "longley"


# ============================================================================
# Case Insensitive Search
# ============================================================================

def test_case_insensitive_search():
    lower = provider.search("longley")
    upper = provider.search("LONGLEY")

    assert lower == upper