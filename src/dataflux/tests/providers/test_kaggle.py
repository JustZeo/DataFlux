import polars as pl

from dataflux.models.dataset import DatasetInfo
from dataflux.models.search_result import SearchResult
from dataflux.providers.kaggle import KaggleProvider


provider = KaggleProvider()


# ============================================================================
# Search
# ============================================================================

def test_search():
    results = provider.search("iris")

    assert isinstance(results, list)
    assert len(results) > 0

    result = results[0]

    assert isinstance(result, SearchResult)
    assert result.provider == "kaggle"

    assert result.id is not None
    assert result.name is not None


# ============================================================================
# Info
# ============================================================================

def test_info():
    results = provider.search("iris")

    info = provider.info(results[0].id)

    assert isinstance(info, DatasetInfo)

    assert info.provider == "kaggle"
    assert info.id == results[0].id

    assert info.name is not None
    assert info.url.startswith("https://www.kaggle.com/datasets/")


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
# Metadata
# ============================================================================

def test_metadata():
    results = provider.search("iris")

    info = provider.info(results[0].id)

    assert isinstance(info.extra, dict)
    assert len(info.extra) > 0


# ============================================================================
# Search Ranking
# ============================================================================

def test_search_returns_best_match():
    results = provider.search("iris")

    assert results[0].relevance >= results[-1].relevance


# ============================================================================
# Case Insensitive Search
# ============================================================================

def test_case_insensitive_search():
    lower = provider.search("iris")
    upper = provider.search("IRIS")

    assert lower == upper