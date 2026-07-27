import polars as pl

from dataflux.models.dataset import DatasetInfo
from dataflux.models.search_result import SearchResult
from dataflux.providers.huggingface import HuggingFaceProvider


provider = HuggingFaceProvider()


# ============================================================================
# Search
# ============================================================================

def test_search():
    results = provider.search("iris")

    assert isinstance(results, list)
    assert len(results) > 0

    result = results[0]

    assert isinstance(result, SearchResult)
    assert result.provider == "huggingface"
    assert result.id is not None
    assert result.name is not None


# ============================================================================
# Info
# ============================================================================

def test_info():
    results = provider.search("iris")

    info = provider.info(results[0].id)

    assert isinstance(info, DatasetInfo)

    assert info.provider == "huggingface"
    assert info.id == results[0].id
    assert info.name is not None
    assert info.url.startswith("https://huggingface.co/datasets/")


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

    assert "downloads" in info.extra
    assert "likes" in info.extra
    assert "author" in info.extra


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