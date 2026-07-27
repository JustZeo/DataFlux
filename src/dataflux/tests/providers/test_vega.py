import polars as pl

from dataflux.models.dataset import DatasetInfo
from dataflux.models.search_result import SearchResult
from dataflux.providers.vega_datasets import VegaDatasetsProvider


provider = VegaDatasetsProvider()


# ============================================================================
# Search
# ============================================================================

def test_search():
    results = provider.search("cars")

    assert isinstance(results, list)
    assert len(results) > 0

    result = results[0]

    assert isinstance(result, SearchResult)
    assert result.provider == "vega"
    assert result.id == "cars"
    assert result.name == "Cars"


# ============================================================================
# Info
# ============================================================================

def test_info():
    info = provider.info("cars")

    assert isinstance(info, DatasetInfo)

    assert info.id == "cars"
    assert info.name == "Cars"

    assert info.instances == 406
    assert info.features == 9

    assert info.provider == "vega"


# ============================================================================
# Pull
# ============================================================================

def test_pull():
    df = provider.pull("cars")

    assert isinstance(df, pl.DataFrame)

    assert df.height == 406
    assert df.width == 9


# ============================================================================
# Schema
# ============================================================================

def test_schema():
    df = provider.pull("cars")

    assert "Name" in df.columns
    assert "Miles_per_Gallon" in df.columns
    assert "Origin" in df.columns


# ============================================================================
# Search Ranking
# ============================================================================

def test_search_returns_best_match():
    results = provider.search("cars")

    assert results[0].id == "cars"


# ============================================================================
# Case Insensitive Search
# ============================================================================

def test_case_insensitive_search():
    lower = provider.search("cars")
    upper = provider.search("CARS")

    assert lower == upper